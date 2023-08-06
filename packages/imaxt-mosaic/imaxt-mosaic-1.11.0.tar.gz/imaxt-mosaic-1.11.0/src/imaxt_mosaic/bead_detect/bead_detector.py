import itertools
import sys
import traceback

import cv2
import dask
import dask.array as da
import numpy as np
import pandas as pd
import scipy.ndimage as ndi
import sep
from dask import delayed
from owl_dev.logging import logger


def create_mask(
    image,
    cl_morph_parm=10,
    c_min_area=0.01,
    c_count_max=15,
    output_size=None,
):

    """Create mask from the scaled image

    Parameters
    ----------
    image
        input image (better to be an scaled image)
    cl_morph_parm
        cv2.MORPH_ELLIPSE parameter for the Morphological closing
    c_min_area
        min area (relative to the full field area) for a contour to be considered as mask
    c_count_max
        Maximum number of contours to be checked for being mask
    output_size
        output image size

    Returns
    -------
    output
        Mask image with mask values set to 1 and background values set to 0
    """

    # TODO: why not (image - image.min()) / (image.max() - image.min()) * 255
    image = (image - image.min()) / image.max() * 255
    image = image.astype(np.uint8)

    # apply close morphology to get rid of small structures and make the big blog bolder
    outer = cv2.morphologyEx(
        image,
        cv2.MORPH_CLOSE,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cl_morph_parm, cl_morph_parm)),
    )

    # remove noise by filtering the most frequent element from the image
    ret, th1 = cv2.threshold(image, np.median(outer) + 1, 255, cv2.THRESH_BINARY)

    # binaries the image and fill the holes
    image_fill_holes = ndi.binary_fill_holes(th1).astype(np.uint8)

    cnts, _ = cv2.findContours(
        image_fill_holes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    # create an empty mask image
    mask = np.zeros(image.shape, np.uint8)

    # assuming the min area for tissue is (e.g. 0.01 = 0.1x * 0.1y)
    min_blob_area = c_min_area * image.shape[1] * image.shape[0]
    blob_counter = 0

    # sort contours by area (large to small) and then loop over them and select those with specific characteristics
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for cnt in cnts[: np.min([int(c_count_max), len(cnts) - 1])]:
        if cv2.contourArea(cnt) > min_blob_area:
            blob_counter += 1
            cv2.drawContours(mask, [cnt], -1, 255, cv2.FILLED)
            mask = cv2.bitwise_and(image_fill_holes, mask)

    mask = cv2.resize(mask, dsize=output_size, interpolation=cv2.INTER_LINEAR)

    return mask


def run_sep(
    indx,
    im,
    mask,
    overlap_size=200.0,
    chunk_loc=None,
    bw=128,
    bh=128,
    minarea=900,
    deblend_nthresh=2,
    circularity=0.9,
):

    if chunk_loc is None:
        chunk_loc = [[np.nan, np.nan], [np.nan, np.nan]]

    logger.debug("Running SEP on the chunk index = %s", indx)

    im = np.array(im)
    mask = np.array(mask).astype(bool)

    try:
        extc_bkg = sep.Background(im, mask=mask, bw=bw, bh=bh)

        logger.debug("Global Background: %f", extc_bkg.globalback)
        logger.debug("Global RMS: %f", extc_bkg.globalrms)

        # get a "global" mean and noise of the image background:
        extc_bkg.back()

        # subtract the background
        reduced_data = im - extc_bkg

        # detect objects
        objects = sep.extract(
            reduced_data,
            8.0,
            minarea=minarea,
            deblend_nthresh=deblend_nthresh,
            err=extc_bkg.globalrms,
            mask=mask,
            segmentation_map=False,
        )

        objects_df = pd.DataFrame(objects)

        objects_df = objects_df[
            (objects_df["flag"] == 0)
            & (objects_df["b"] / objects_df["a"] > circularity)
        ]

        # add indx and x(y)_range of each chunk to the dataframe
        df_len = len(objects_df)
        objects_df.insert(0, "indx_0", indx[0])
        objects_df.insert(1, "indx_1", indx[1])
        objects_df.insert(2, "X_RANGE_i", chunk_loc[1][0])
        objects_df.insert(3, "X_RANGE_f", chunk_loc[1][1])
        objects_df.insert(4, "Y_RANGE_i", chunk_loc[0][0])
        objects_df.insert(5, "Y_RANGE_f", chunk_loc[0][1])

        # estimate absolute coordinates of the peaks and keep them as new columns
        # called XC and YC (also corrected for overlapping)
        # Here we use (2 * index +1) * overlap_size factor to convert coordinates
        # from overlapped to the original (non-overlapped)
        if df_len > 0:
            objects_df["XC"] = objects_df.apply(
                lambda row: row.X_RANGE_i
                + row.x
                - (2.0 * row.indx_1 + 1) * overlap_size,
                axis=1,
            )
            objects_df["YC"] = objects_df.apply(
                lambda row: row.Y_RANGE_i
                + row.y
                - (2.0 * row.indx_0 + 1) * overlap_size,
                axis=1,
            )
        else:
            objects_df["XC"] = []
            objects_df["YC"] = []

        logger.debug("Number of detected objects: %s", df_len)

        return objects_df

    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        logger.debug("".join(lines))
        return None


def bead_detect_worker(image, mask, overlap_size=0.0):

    if overlap_size > 0.0:
        # add overlap to data and mask (for mask, we refill the boundary with 1 [equivalent to mask=True])
        image = da.overlap.overlap(image, overlap_size, {0: 1, 1: 1})
        mask = da.overlap.overlap(mask, overlap_size, {0: 1, 1: 1})

    beads_df = []
    for indx in itertools.product(*map(range, image.blocks.shape)):

        # extract the location of each chunk (overlapped) and later,
        # pass it to the run_sep function to be included in the results
        i, j = indx[-2:]
        chunk_loc_indx = [
            [sum(image.chunks[-2][:i]), sum(image.chunks[-2][: i + 1])],
            [sum(image.chunks[-1][:j]), sum(image.chunks[-1][: j + 1])],
        ]

        circ_chunk_i = delayed(run_sep)(
            indx,
            image.blocks[indx],
            mask.blocks[indx],
            overlap_size=overlap_size,
            chunk_loc=chunk_loc_indx,
        )

        if circ_chunk_i is not None:
            beads_df.append(circ_chunk_i)

    final_beads = dask.compute(beads_df)[0]
    final_beads = pd.concat(final_beads, ignore_index=True)

    return final_beads


def plot_beads(image, mask, beads_df, fig_fname=None):
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Ellipse
    except ModuleNotFoundError:
        logger.warning("matplotlib not found, cannot plot beads")
        return

    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.imshow(np.array(mask), cmap="gray")
    ax1.set_title("Mask image")

    ax2 = fig.add_subplot(1, 2, 2)
    image = np.array(image)

    m, s = np.mean(image), np.std(image)
    ax2.imshow(image, interpolation="nearest", cmap="gray", vmin=m - s, vmax=m + s)
    ax2.set_title("Detected Beads")
    # plot an ellipse for each object
    for i in range(len(beads_df)):
        try:
            # plot boarder or each ellipse
            e = Ellipse(
                xy=(beads_df["XC"][i], beads_df["YC"][i]),
                width=6 * beads_df["a"][i],
                height=6 * beads_df["b"][i],
                angle=beads_df["theta"][i] * 180.0 / np.pi,
            )
            e.set_facecolor("none")
            e.set_edgecolor("red")
            ax2.add_artist(e)

            # mark the centre of each ellipse
            e_cent = Ellipse(
                xy=(beads_df["XC"][i], beads_df["YC"][i]),
                width=0.5 * beads_df["a"][i],
                height=0.5 * beads_df["b"][i],
                angle=beads_df["theta"][i] * 180.0 / np.pi,
            )
            e_cent.set_facecolor("none")
            e_cent.set_edgecolor("blue")
            ax2.add_artist(e_cent)

        except Exception:
            pass

    if fig_fname is not None:
        plt.tight_layout()
        plt.savefig(fig_fname)
        plt.close()

    else:
        plt.show()


# TODO: write as script
# if __name__ == "__main__":

#     # read image from zarr to xarray
#     input_file = "/Users/alireza/IMAXT/PyHPT/PyHPT_data/stpt/20220608_DI_PDX_SA535_Tum_5223_04280_100x15um/mos"

#     mean_data_org = read_infile(
#         input_file, sname="S001", group="", stat="mean", debug=True
#     )
#     mean_data_l16 = read_infile(
#         input_file, sname="S001", group="l.16", stat="mean", debug=True
#     )

#     # create a mask from the scaled image
#     mask_image = create_mask(
#         mean_data_l16,
#         cl_morph_parm=10,
#         c_min_area=0.01,
#         c_count_max=15,
#         output_size=mean_data_org.shape[::-1],
#         debug=True,
#     )

#     beads_pd = bead_detect_worker(
#         mean_data_org, mask_image, debug=True, overlap_size=200
#     )
#     beads_pd["z"] = 0
#     beads_pd["section"] = "S001"

#     beads_pd.to_parquet("S001.parquet")

#     plot_beads(mean_data_org, mask_image, beads_pd, fig_fname="S001.png")
