import os
import re
import glob
import shutil
import json
import math
from datetime import datetime
import logging

# Internal dependencies imports
from coastseg import exceptions

from coastsat import SDS_tools
from tqdm.auto import tqdm
import requests
from area import area
import geopandas as gpd
from shapely import geometry
import numpy as np
import geojson
from skimage.io import imread
from leafmap import check_file_path
from pyproj import Proj, transform
import pandas as pd

logger = logging.getLogger(__name__)


def save_to_geojson_file(out_file: str, geojson: dict, **kwargs) -> None:
    """save_to_geojson_file Saves given geojson to a geojson file at outfile
    Args:
        out_file (str): The output file path
        geojson (dict): geojson dict containing FeatureCollection for all geojson objects in selected_set
    """
    # Save the geojson to a file
    out_file = check_file_path(out_file)
    ext = os.path.splitext(out_file)[1].lower()
    if ext == ".geojson":
        out_geojson = out_file
    else:
        out_geojson = os.path.splitext(out_file)[1] + ".geojson"
    with open(out_geojson, "w") as f:
        json.dump(geojson, f, **kwargs)


def download_url(url: str, save_path: str, filename: str = None, chunk_size: int = 128):
    """Downloads the data from the given url to the save_path location.
    Args:
        url (str): url to data to download
        save_path (str): directory to save data
        chunk_size (int, optional):  Defaults to 128.
    """
    with requests.get(url, stream=True) as r:
        if r.status_code == 404:
            logger.error(f"DownloadError: {save_path}")
            raise exceptions.DownloadError(os.path.basename(save_path))
        # check header to get content length, in bytes
        total_length = int(r.headers.get("Content-Length"))
        with open(save_path, "wb") as fd:
            with tqdm(
                total=total_length,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Downloading {filename}",
                initial=0,
                ascii=True,
            ) as pbar:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    fd.write(chunk)
                    pbar.update(len(chunk))


def combine_inputs(roi: dict, attributes: dict) -> dict:
    """Adds the roi's coordinates and roi_id to attributes
    Args:
        roi (dict): geojson of roi
        attributes (dict): download settings
    Returns:
        dict: dictionary containing attributes and
        new keys 'polygon':roi coordinates and 'roi_id':roi's id
    """
    polygon = roi["geometry"]["coordinates"]
    polygon = SDS_tools.smallest_rectangle(polygon)
    inputs = {"polygon": polygon, "roi_id": str(roi["properties"]["id"]), **attributes}
    return inputs


def get_inputs_list(
    roi_geojson: dict, dates: list, sat_list: list, collection: str
) -> list:
    """get_inputs_list Returns a list of all download settings each of ROI.
        Sample download settings:
        {'polygon': roi["geometry"]["coordinates"],
        'roi_id':roi['properties']['id'],
        'dates': dates,
        'sat_list': sat_list,
        'sitename' : 'ID02022-10-04__21_hr_39_min03sec',(ex folder name)
        'filepath': filepath,
        'landsat_collection': collection}
    Args:
        selected_roi_geojson:dict
            A geojson dictionary containing all the ROIs selected by the user
        dates: list
            A list of length two that contains a valid start and end date
        collection : str
        whether to use LandSat Collection 1 (`C01`) or Collection 2 (`C02`).
        sat_list: list
            A list of strings containing the names of the satellite
    Returns:
        list[dict]: list of all download settings each of ROI
    """
    date_str = generate_datestring()
    # filepath: directory where data will be saved
    filepath = os.path.join(os.getcwd(), "data")

    # for each site create dictionary with download settings eg. dates,sitename
    inputs_list = []
    for roi in roi_geojson["features"]:
        # get the id from ROI's properties
        roi_id = str(roi["properties"]["id"])
        polygon = roi["geometry"]["coordinates"]
        sitename = "ID_" + str(roi_id) + "_datetime" + date_str
        inputs = {
            "dates": dates,
            "sat_list": sat_list,
            "sitename": sitename,
            "filepath": filepath,
            "roi_id": roi_id,
            "polygon": polygon,
            "landsat_collection": collection,
        }

        # add inputs dictionary to inputs list
        inputs_list.append(inputs)

    logger.info(f"inputs_list: {inputs_list}")
    if inputs_list == []:
        logger.error(
            "Error: No ROIs were selected. Please click a valid ROI on the map"
        )
        raise Exception(
            "Error: No ROIs were selected. Please click a valid ROI on the map\n"
        )
    return inputs_list


def get_center_rectangle(coords: list) -> tuple:
    """returns the center point of rectangle specified by points coords
    Args:
        coords list[tuple(float,float)]: lat,lon coordinates
    Returns:
        tuple[float]: (center x coordinate, center y coordinate)
    """
    x1, y1 = coords[0][0], coords[0][1]
    x2, y2 = coords[2][0], coords[2][1]
    center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
    return center_x, center_y


def is_shoreline_present(extracted_shorelines: dict, roi_id: int) -> bool:
    """Returns true if shoreline array exists for roi_id
    Args:
        extracted_shorelines (dict): dictionary of extracted shorelines in form of :
            {   roi_id : {dates: [datetime.datetime,datetime.datetime],
                shorelines: [array(),array()]}  }
        roi_id (int): id of the roi
    Returns:
        bool: false if shoreline does not exist at roi_id
    """
    logger.info(
        f"is_shoreline_present() : extracted_shorelines[roi_id]['shorelines']: {extracted_shorelines[roi_id]['shorelines']}"
    )
    for shoreline in extracted_shorelines[roi_id]["shorelines"]:
        if shoreline.size != 0:
            return True
    return False


def convert_espg(
    input_epsg: int, output_epsg: int, coastsat_array: np.ndarray
) -> np.ndarray:
    """Convert the coastsat_array espg to the output_espg
    Args:
        input_epsg (int): input espg
        output_epsg (int): output espg
        coastsat_array (np.ndarray): array of coordiinates as [[lat,lon],[lat,lon]....]
    Returns:
        np.ndarray: array with output espg in the form [[[lat,lon,0.]]]
    """
    if input_epsg is None:
        input_epsg = 4326
    inProj = Proj(init="epsg:" + str(input_epsg))
    outProj = Proj(init="epsg:" + str(output_epsg))
    s_proj = []
    logger.info(f"convert_espg: coastsat_array {coastsat_array}")
    # Convert all the lat,ln coords to new espg (operation takes some time....)
    for coord in coastsat_array:
        x2, y2 = transform(inProj, outProj, coord[0], coord[1])
        s_proj.append([x2, y2, 0.0])
    return np.array(s_proj)


def convert_wgs_to_utm(lon: float, lat: float) -> str:
    """return most accurate utm epsg-code based on lat and lng
    convert_wgs_to_utm function, see https://stackoverflow.com/a/40140326/4556479
    Args:
        lon (float): longitude
        lat (float): latitude
    Returns:
        str: new espg code
    """
    utm_band = str((math.floor((lon + 180) / 6) % 60) + 1)
    if len(utm_band) == "1":
        utm_band = "0" + utm_band
    if lat >= 0:
        epsg_code = "326" + utm_band  # North
        return epsg_code
    epsg_code = "327" + utm_band  # South
    return epsg_code


def extract_roi_by_id(gdf: gpd.geodataframe, roi_id: int) -> gpd.geodataframe:
    """Returns geodataframe with a single ROI whose id matches roi_id.
       If roi_id is None returns gdf

    Args:
        gdf (gpd.geodataframe): ROI geodataframe to extract ROI with roi_id from
        roi_id (int): id of the ROI to extract
    Raises:
        exceptions.Id_Not_Found: if id doesn't exist in ROI's geodataframe or self.rois.gdf is empty
    Returns:
        gpd.geodataframe: ROI with id matching roi_id
    """
    if roi_id is None:
        single_roi = gdf
    else:
        # Select a single roi by id
        single_roi = gdf[gdf["id"].astype(str) == str(roi_id)]
        # if the id was not found in the geodataframe raise an exception
    if single_roi.empty:
        logger.error(f"Id: {id} was not found in {gdf}")
        raise exceptions.Id_Not_Found(id)
    logger.info(f"extract_roi_by_id:: single_roi: {single_roi}")
    return single_roi


def convert_gdf_to_polygon(gdf: gpd.geodataframe, id: int = None) -> geometry.Polygon:
    """Returns the roi with given id as Shapely.geometry.Polygon
    Args:
        gdf (gpd.geodataframe): geodataframe consisting of rois or a bbox
        id (str): roi_id
    Returns:
        geometry.Polygon: roi with the id converted to Shapely.geometry.Polygon
    """
    single_roi = extract_roi_by_id(gdf, id)
    single_roi = single_roi["geometry"].to_json()
    single_roi = json.loads(single_roi)
    polygon = geometry.Polygon(single_roi["features"][0]["geometry"]["coordinates"][0])
    return polygon


def get_area(polygon: dict):
    "Calculates the area of the geojson polygon using the same method as geojson.io"
    return round(area(polygon), 3)


def read_json_file(filename: str):
    logger.info(f"read_json_file {filename}")
    with open(filename, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)
    return data


def find_config_json(dir_path):
    logger.info(f"searching directory for config.json: {dir_path}")

    def use_regex(input_text):
        pattern = re.compile(r"config.*\.json", re.IGNORECASE)
        if pattern.match(input_text) is not None:
            return True
        return False

    for item in os.listdir(dir_path):
        if use_regex(item):
            logger.info(f"{item} matched regex")
            return item


def check_filepaths_exist(roi_ids: list, inputs_dict: dict) -> bool:
    """Returns True if a 'filepath' key and location exists in inputs dict for each roi id in roi_ids.
    False means a 'filepath' key or location did not exist for an id in roi_ids
    Args:
        roi_ids (list[str]): ids of each roi
        inputs_dict (dict): input settings for each roi.
    Returns:
        bool: True if all filepaths existed in inputs_dict for each id in roi_ids
    """
    # by default assume 'filepath's exist for all rois
    all_filepaths_exist = True
    for id in roi_ids:
        if "filepath" in inputs_dict[id]:
            logger.info(f"filepath in inputs_dict[id]: {inputs_dict[id]['filepath']}")
            if not os.path.exists(inputs_dict[id]["filepath"]):
                print(f"Did not find filepath location for ROI: {id}")
                logger.info(f"Did not find filepath location for ROI: {id}")
                all_filepaths_exist = False
        elif "filepath" not in inputs_dict[id]:
            print(f"Did not find filepath for ROI: {id}")
            logger.info(f"Did not find filepath for ROI: {id}")
            all_filepaths_exist = False
    return all_filepaths_exist


def make_coastsat_compatible(shoreline_in_roi: gpd.geodataframe) -> np.ndarray:
    """Return the shoreline_in_roi as an np.array in the form:
        array([[lat,lon,0],[lat,lon,0],[lat,lon,0]....])
    Args:
        shoreline_in_roi (gpd.geodataframe): clipped portion of shoreline within a roi
    Returns:
        np.ndarray: shorelines in the form:
            array([[lat,lon,0],[lat,lon,0],[lat,lon,0]....])
    """
    # Then convert the shoreline to lat,lon tuples for CoastSat
    shorelines = []
    # Use explode to break multilinestrings in linestrings
    shoreline_in_roi_exploded = shoreline_in_roi.explode()
    for k in shoreline_in_roi_exploded["geometry"].keys():
        # For each linestring portion of shoreline convert to lat,lon tuples
        shorelines.append(
            tuple(np.array(shoreline_in_roi_exploded["geometry"][k]).tolist())
        )
    # shorelines = [([lat,lon],[lat,lon],[lat,lon]),([lat,lon],[lat,lon],[lat,lon])...]
    # Stack all the tuples into a single list of n rows X 2 columns
    shorelines = np.vstack(shorelines)
    # Add third column of 0s to represent mean sea level
    shorelines = np.insert(shorelines, 2, np.zeros(len(shorelines)), axis=1)
    # shorelines = array([[lat,lon,0],[lat,lon,0],[lat,lon,0]....])
    return shorelines


def create_json_config(master_config: dict, inputs: dict, settings: dict) -> dict:
    """returns master config dictionary with the settings, currently selected_roi ids, and
    each of the inputs specified by roi id.
    sample master_config:
    {
        'roi_ids': ['17','20']
        'settings':{ 'dates': ['2018-12-01', '2019-03-01'],
                    'cloud_thresh': 0.5,
                    'dist_clouds': 300,
                    'output_epsg': 3857,}
        '17':{
            'sat_list': ['L8'],
            'collection': 'C01',
            'dates': ['2018-12-01', '2019-03-01'],
            'sitename':'roi_17',
            'filepath':'C:\\Home'
        }
        '20':{
            'sat_list': ['L8'],
            'collection': 'C01',
            'dates': ['2018-12-01', '2019-03-01'],
            'sitename':'roi_20',
            'filepath':'C:\\Home'
        }
    }

    Args:
        master_config (dict): json style dictionary containing settings, rois, and inputs
        inputs (dict): json style dictionary with roi ids at the keys with inputs as values
        settings (dict):  json style dictionary containing map settings

    Returns:
        dict: json style dictionary, master_config
    """
    roi_ids = list(inputs.keys())
    master_config = {**inputs}
    master_config["roi_ids"] = roi_ids
    master_config["settings"] = settings

    return master_config


def does_filepath_exist(dictionary: dict):
    if "filepath" not in dictionary:
        logger.error(
            f"Cannot extract shorelines because filepath key did not exist in {dictionary}"
        )
        raise Exception(
            f"Cannot extract shorelines because filepath key did not exist in {dictionary}"
        )
    elif not os.path.exists(dictionary["filepath"]):
        logger.error(
            f"Cannot extract shorelines because location doesn't exist. Download the data first.\n{dictionary['filepath']} "
        )
        raise FileNotFoundError(
            f"Cannot extract shorelines because location doesn't exist. Download the data first.\n{dictionary['filepath']} "
        )


def create_config_gdf(
    rois: gpd.GeoDataFrame,
    shorelines_gdf: gpd.GeoDataFrame = None,
    transects_gdf: gpd.GeoDataFrame = None,
    bbox_gdf: gpd.GeoDataFrame = None,
) -> gpd.GeoDataFrame():
    if shorelines_gdf is None:
        shorelines_gdf = gpd.GeoDataFrame()
    if transects_gdf is None:
        transects_gdf = gpd.GeoDataFrame()
    if bbox_gdf is None:
        bbox_gdf = gpd.GeoDataFrame()
    # create new column 'type' to indicate object type
    rois["type"] = "roi"
    shorelines_gdf["type"] = "shoreline"
    transects_gdf["type"] = "transect"
    bbox_gdf["type"] = "bbox"
    new_gdf = gpd.GeoDataFrame(pd.concat([rois, shorelines_gdf], ignore_index=True))
    new_gdf = gpd.GeoDataFrame(pd.concat([new_gdf, transects_gdf], ignore_index=True))
    new_gdf = gpd.GeoDataFrame(pd.concat([new_gdf, bbox_gdf], ignore_index=True))
    return new_gdf


def write_to_json(filepath: str, settings: dict):
    """ "Write the  settings dictionary to json file"""
    with open(filepath, "w", encoding="utf-8") as output_file:
        json.dump(settings, output_file)


def read_geojson_file(geojson_file: str) -> dict:
    """Returns the geojson of the selected ROIs from the file specified by geojson_file"""
    with open(geojson_file) as f:
        data = geojson.load(f)
    return data


def read_gpd_file(filename: str) -> gpd.GeoDataFrame:
    """
    Returns geodataframe from geopandas geodataframe file
    """
    if os.path.exists(filename):
        logger.info(f"Opening \n {filename}")
        with open(filename, "r") as f:
            gpd_data = gpd.read_file(f)
    else:
        logger.error(f"Geodataframe file does not exist \n {filename}")
        print(
            "File does not exist. Please download the coastline_vector necessary here: https://geodata.lib.berkeley.edu/catalog/stanford-xv279yj9196 "
        )
        raise FileNotFoundError
    return gpd_data


def clip_to_bbox(
    gdf_to_clip: gpd.GeoDataFrame, bbox_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """Clip gdf_to_clip to bbox_gdf. Only data within bbox will be kept.
    Args:
        gdf_to_clip (geopandas.geodataframe.GeoDataFrame): geodataframe to be clipped to bbox
        bbox_gdf (geopandas.geodataframe.GeoDataFrame): drawn bbox
    Returns:
        geopandas.geodataframe.GeoDataFrame: clipped geodata within bbox
    """
    shapes_in_bbox = gpd.clip(gdf_to_clip, bbox_gdf)
    shapes_in_bbox = shapes_in_bbox.to_crs("EPSG:4326")
    return shapes_in_bbox


def get_jpgs_from_data(file_ext: str = "RGB") -> str:
    """Returns the folder where all jpgs were copied from the data folder in coastseg.
    This is where the model will save the computed segmentations."""
    # Data folder location
    src_path = os.path.abspath(os.getcwd() + os.sep + "data")
    if os.path.exists(src_path):
        rename_jpgs(src_path)
        # Create a new folder to hold all the data
        location = os.getcwd()
        name = "segmentation_data"
        new_folder = mk_new_dir(name, location)
        if file_ext == "RGB":
            glob_str = (
                src_path
                + str(os.sep + "**" + os.sep) * 2
                + "preprocessed"
                + os.sep
                + "RGB"
                + os.sep
                + "*.jpg"
            )
            copy_files_to_dst(src_path, new_folder, glob_str)
        elif file_ext == "MNDWI":
            glob_str = (
                src_path
                + str(os.sep + "**" + os.sep) * 2
                + "preprocessed"
                + os.sep
                + "RGB"
                + os.sep
                + "*RGB*.jpg"
            )
            RGB_path = os.path.join(new_folder, "RGB")
            if not os.path.exists(RGB_path):
                os.mkdir(RGB_path)
            copy_files_to_dst(src_path, RGB_path, glob_str)
            # Copy the NIR images to the destination
            glob_str = (
                src_path
                + str(os.sep + "**" + os.sep) * 2
                + "preprocessed"
                + os.sep
                + "NIR"
                + os.sep
                + "*NIR*.jpg"
            )
            NIR_path = os.path.join(new_folder, "NIR")
            if not os.path.exists(NIR_path):
                os.mkdir(NIR_path)
            copy_files_to_dst(src_path, NIR_path, glob_str)
        elif file_ext is None:
            glob_str = (
                src_path
                + str(os.sep + "**" + os.sep) * 2
                + "preprocessed"
                + os.sep
                + "*.jpg"
            )
            copy_files_to_dst(src_path, new_folder, glob_str)
        return new_folder
    else:
        print("ERROR: Cannot find the data directory in coastseg")
        raise Exception("ERROR: Cannot find the data directory in coastseg")


def rename_jpgs(src_path: str) -> None:
    """Renames all the jpgs in the data directory in coastseg
    Args:
        src_path (str): full path to the data directory in coastseg
    """
    files_renamed = False
    for folder in os.listdir(src_path):
        folder_path = src_path + os.sep + folder
        # Split the folder name at the first _
        folder_id = folder.split("_")[0]
        folder_path = folder_path + os.sep + "jpg_files" + os.sep + "preprocessed"
        jpgs = glob.glob1(folder_path + os.sep, "*jpg")
        # Append folder id to basename of jpg if not already there
        for jpg in jpgs:
            if folder_id not in jpg:
                # print(jpg)
                files_renamed = True
                base, ext = os.path.splitext(jpg)
                new_name = folder_path + os.sep + base + "_" + folder_id + ext
                old_name = folder_path + os.sep + jpg
                os.rename(old_name, new_name)
        if files_renamed:
            print(f"Renamed files in {src_path} ")


def generate_datestring() -> str:
    """Returns a datetime string in the following format %m-%d-%y__%I_%M_%S
    EX: "ID_0__01-31-22_12_19_45"""
    date = datetime.now()
    return date.strftime("%m-%d-%y__%I_%M_%S")


def mk_new_dir(name: str, location: str):
    """Create new folder with  datetime stamp at location
    Args:
        name (str): name of folder to create
        location (str): location to create folder
    """
    if os.path.exists(location):
        new_folder = location + os.sep + name + "_" + generate_datestring()
        os.mkdir(new_folder)
        return new_folder
    else:
        raise Exception("Location provided does not exist.")


def copy_files_to_dst(src_path: str, dst_path: str, glob_str: str) -> None:
    """Copies all files from src_path to dest_path
    Args:
        src_path (str): full path to the data directory in coastseg
        dst_path (str): full path to the images directory in Sniffer
    """
    if not os.path.exists(dst_path):
        print(f"dst_path: {dst_path} doesn't exist.")
    elif not os.path.exists(src_path):
        print(f"src_path: {src_path} doesn't exist.")
    else:
        for file in glob.glob(glob_str):
            shutil.copy(file, dst_path)
        print(f"\nCopied files that matched {glob_str}  \nto {dst_path}")


def RGB_to_MNDWI(RGB_dir_path: str, NIR_dir_path: str, output_path: str) -> None:
    """Converts two directories of RGB and NIR imagery to MNDWI imagery in a directory named
     'MNDWI_outputs'.
    Args:
        RGB_dir_path (str): full path to directory containing RGB images
        NIR_dir_path (str): full path to directory containing NIR images

    Original Code from doodleverse_utils by Daniel Buscombe
    source: https://github.com/Doodleverse/doodleverse_utils
    """
    paths = [RGB_dir_path, NIR_dir_path]
    files = []
    for data_path in paths:
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"{data_path} not found")
        f = sorted(glob(data_path + os.sep + "*.jpg"))
        if len(f) < 1:
            f = sorted(glob(data_path + os.sep + "images" + os.sep + "*.jpg"))
        files.append(f)
    # creates matrix:  bands(RGB) x number of samples(NIR)
    # files=[['full_RGB_path.jpg','full_NIR_path.jpg'],
    # ['full_jpg_path.jpg','full_NIR_path.jpg']....]
    files = np.vstack(files).T
    # output_path: directory to store MNDWI outputs
    output_path += os.sep + "MNDWI_outputs"
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # Create subfolder to hold MNDWI ouputs in
    output_path = mk_new_dir("MNDWI_ouputs", output_path)

    for counter, f in enumerate(files):
        datadict = {}
        # Read green band from RGB image and cast to float
        green_band = imread(f[0])[:, :, 1].astype("float")
        # Read SWIR and cast to float
        swir = imread(f[1]).astype("float")
        # Transform 0 to np.NAN
        green_band[green_band == 0] = np.nan
        swir[swir == 0] = np.nan
        # Mask out the NaNs
        green_band = np.ma.filled(green_band)
        swir = np.ma.filled(swir)

        # MNDWI imagery formula (Green + SWIR) / (Green + SWIR)
        mndwi = np.divide(swir - green_band, swir + green_band)
        # Convert the NaNs to -1
        mndwi[np.isnan(mndwi)] = -1
        # Rescale to be between 0 - 255
        mndwi = rescale_array(mndwi, 0, 255)
        # Save meta data for savez_compressed()
        datadict["arr_0"] = mndwi.astype(np.uint8)
        datadict["num_bands"] = 1
        datadict["files"] = [fi.split(os.sep)[-1] for fi in f]
        # Remove the file extension from the name
        ROOT_STRING = f[0].split(os.sep)[-1].split(".")[0]
        # save MNDWI as .npz file
        segfile = (
            output_path
            + os.sep
            + ROOT_STRING
            + "_noaug_nd_data_000000"
            + str(counter)
            + ".npz"
        )
        np.savez_compressed(segfile, **datadict)
        del datadict, mndwi, green_band, swir

        return output_path


def rescale_array(self, dat, mn, mx):
    """
    rescales an input dat between mn and mx
    Code from doodleverse_utils by Daniel Buscombe
    source: https://github.com/Doodleverse/doodleverse_utils
    """
    m = min(dat.flatten())
    M = max(dat.flatten())
    return (mx - mn) * (dat - m) / (M - m) + mn
