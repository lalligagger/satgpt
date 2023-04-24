import json
import fire
import pystac
import rasterio as rio
import stackstac
from dask.diagnostics import ProgressBar
from geogif import dgif
from rasterio.session import AWSSession
import warnings

warnings.simplefilter("ignore", category=RuntimeWarning)

def read_json_file(file_path):
    """
    Reads a JSON file and returns its contents as a string.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        str: The contents of the JSON file as a string.
    """
    with open(file_path, "r") as f:
        return f.read()

def promote_s3(items):
    """
    Updates URLs to use s3.

    Args:
        items (list): A list of STAC items.

    Returns:
        list: The updated list of STAC items.
    """
    print("promoting s3 to primary href")
    for item in items:
        for a in item["assets"]:
            if (
                "alternate" in item["assets"][a]
                and "s3" in item["assets"][a]["alternate"]
            ):
                item["assets"][a]["href"] = item["assets"][a]["alternate"]["s3"]["href"]
            item["assets"][a]["href"] = item["assets"][a]["href"].replace(
                "usgs-landsat-ard", "usgs-landsat"
            )
    return items

class Stacker:
    """
    A class for stacking STAC items and creating GIF animations.

    Attributes:
        stack (xarray.Dataset): The stacked STAC items.
        qa_mask (xarray.DataArray): The QA mask for the stacked STAC items.
    """

    def __init__(self, path, *, use_s3=True, **kwargs):
        """
        Initializes the Stacker class.

        Args:
            path (str): The path to the JSON file containing the STAC items.
            use_s3 (bool): Whether to use s3 URLs. Defaults to True.
            **kwargs: Additional keyword arguments to pass to stackstac.stack().
        """
        self.load_stack(path, use_s3=use_s3, kwargs=kwargs)

    def load_stack(self, path, use_s3=True, kwargs={}):
        """
        Loads and stacks STAC items.

        Args:
            path (str): The path to the JSON file containing the STAC items.
            use_s3 (bool): Whether to use s3 URLs. Defaults to True.
            kwargs (dict): Additional keyword arguments to pass to stackstac.stack().

        Returns:
            Stacker: The Stacker object.
        """
        try:
            search = json.loads(read_json_file(path))["features"]
        except:
            # hack to accept raw json
            search = json.loads(path)["features"]

        if use_s3:
            search = promote_s3(search)

        items = pystac.ItemCollection(search)
        self.stack = stackstac.stack(
            items,
            **kwargs,
        )

        self.stack = self.stack.assign_coords(
            band=self.stack.common_name.fillna(self.stack.band).rename("band")
        )

        return self

    def make_qa_mask(self):
        """
        Creates a QA mask for the stacked STAC items.

        Returns:
            Stacker: The Stacker object.
        """
        platform = "sentinel"

        if platform == "landsat":
            mask_bitfields = [1, 2, 3, 4]  # dilated cloud, cirrus, cloud, cloud shadow
            qa = self.stack.sel(band="qa_pixel").astype("uint16")

        if platform == "sentinel":
            mask_bitfields = [
                1,
                3,
                8,
                9,
                10,
            ]  # defective/ saturated, cloud shadow, cloud med, cloud high, cirrus
            qa = self.stack.sel(band="SCL").astype("uint16")

        bitmask = 0
        for field in mask_bitfields:
            bitmask |= 1 << field

        bin(bitmask)
        self.qa_mask = qa & bitmask

        return self

    def to_gif(
        self, 
        to="./data/animation.gif", 
        *,
        apply_mask=True,
        resample="2W",
        fill=True,
        **kwargs):
        """
        Creates a GIF animation from the stacked STAC items.

        Args:
            to (str): The path to save the GIF animation. Defaults to "./data/animation.gif".
            apply_mask (bool): Whether to apply the QA mask. Defaults to True.
            resample (str): The resampling frequency. Defaults to "2W".
            fill (bool): Whether to fill missing values. Defaults to True.
            **kwargs: Additional keyword arguments to pass to geogif.dgif().

        Returns:
            None
        """
        sr = self.stack.sel(
            {"band": ["red", "green", "blue"]}
        )

        if apply_mask:
            self.make_qa_mask()
            sr = sr.where(self.qa_mask == 0)

        if resample:
            sr = sr.resample(time=resample).median("time")

        if fill:
            sr = sr.ffill("time")[1:]

        aws_session = AWSSession(requester_pays=True)
        with rio.Env(aws_session):
            with ProgressBar():
                gif_bytes = dgif(sr, date_format="Date: %d-%m-%Y", bytes=True, **kwargs).compute()

        with open(to, "wb") as f:
            f.write(gif_bytes)

    def q(self):
        """
        Placeholder method.
        """
        pass

if __name__ == "__main__":
    stacker = fire.Fire(Stacker)
