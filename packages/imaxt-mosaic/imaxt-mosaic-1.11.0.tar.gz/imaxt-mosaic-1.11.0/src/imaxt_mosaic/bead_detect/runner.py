import dask.array as da
import xarray as xr
from dask import delayed
from owl_dev.logging import logger

from ..settings import Settings
from ..utils import trim_memory_workers
from .bead_detector import bead_detect_worker, create_mask, plot_beads


def bead_detect(output_path, overwrite=False, fig=True):
    """Detect beads in a given image."""
    mod_input_path = output_path / "mos"
    (output_path / "bead").mkdir(exist_ok=True)

    ds = xr.open_zarr(mod_input_path)
    ds16 = xr.open_zarr(mod_input_path, group="l.16")
    sections = list(ds)
    if Settings.sections:
        sections = [sections[i - 1] for i in Settings.sections]

    logger.info(f"{len(sections)} section(s) to proceed with")

    # TODO: support multiple z planes
    for sect in sections:
        output_bead = output_path / "bead" / f"{sect}.parquet"
        if output_bead.exists() and not overwrite:
            logger.info(f"Skipping section {sect}")
            continue
        logger.debug(f"Processing section {sect}")
        mean_data_org = ds[sect].sel(z=0).data.mean(axis=0)
        mean_data_l16 = ds16[sect].sel(z=0).data.mean(axis=0)

        # create a mask from the scaled image
        mask_image_d = delayed(create_mask)(
            mean_data_l16,
            cl_morph_parm=10,
            c_min_area=0.01,
            c_count_max=15,
            output_size=mean_data_org.shape[::-1],
        )

        mask_image = da.from_delayed(
            mask_image_d, shape=mean_data_org.shape, dtype="uint8"
        ).rechunk(mean_data_org.chunksize)

        beads_df = bead_detect_worker(mean_data_org, mask_image, overlap_size=200)
        beads_df["z"] = 0
        beads_df["section"] = str(sect)

        beads_df.to_parquet(output_bead)

        if fig:
            plot_beads(
                mean_data_org,
                mask_image,
                beads_df,
                fig_fname=output_path / "bead" / f"{sect}_bead.png",
            )
        del mask_image
        del mean_data_org
        del mean_data_l16
        trim_memory_workers()


# TODO: write as script
# if __name__ == "__main__":

#     input_path = Path(
#         "/Users/alireza/IMAXT/PyHPT/PyHPT_data/raw/stpt/20220728_CM_BalbC_D2A1_zsg_spleen_50x20um"
#     )
#     output_path = Path(
#         "/Users/alireza/IMAXT/PyHPT/PyHPT_results/processed/stpt/20220728_CM_BalbC_D2A1_zsg_spleen_50x20um"
#     )
#     bead_detect(input_path, output_path, overwrite=False, fig=True)
