import argparse
import time
import json

import zipfile
from pathlib import Path
from tqdm import tqdm

from usgs import api as usgs_api
from eobuilding_fair_inria.download.earth_explorer import usgs_download_results, extract_img_from_ee_zip

# bbox =  ll_lat , ll_long, ur_lat, ur_long,
area_metadata_dict = {
    "austin" : {
        "raw_source" : "earth_explorer",
        "dataset" : "high_res_ortho",
        "bbox_wgs84" :  (30.216,  -97.790, 30.299,  -97.6947),
        "dates_interval" : ("2011-01-01", "2013-01-01")
    },
    "bellingham" : {
        "raw_source" : "earth_explorer",
        "dataset" : "high_res_ortho",
        "bbox_wgs84" :  (48.6976, -122.518, 48.7925, -122.374),
        "dates_interval" : ("2009-01-01", "2010-01-01")
    },
    "bloomington" : {
        "raw_source" : "earth_explorer",
        "dataset" : "high_res_ortho",
        "bbox_wgs84" :  (39.122,  -86.607, 39.2041,  -86.4673),
        "dates_interval" : ("2010-01-01", "2012-01-01")
    },
    "chicago" : {
        "raw_source" : "earth_explorer",
        "dataset" : "high_res_ortho",
        "bbox_wgs84" :  (41.824,  -87.7298, 41.9059,  -87.6200),
        "dates_interval" : ("2011-01-01", "2013-01-01")
    },
    "kitsap" : {
        "raw_source" : "earth_explorer",
        "dataset" : "high_res_ortho",
        "bbox_wgs84" : (47.4566,  -122.7082, 47.5788, -122.5880),
        "dates_interval" : ("2009-01-01", "2010-01-01")
    },
    "sfo" : {
        "raw_source" : "earth_explorer",
        "dataset" : "high_res_ortho",
        "bbox_wgs84" :  (37.7161,  -122.4952, 37.7979, -122.3921),
        "dates_interval" : ("2010-01-01", "2012-01-01")
    }
}

#https://github.com/j-be/wien-geodatenviewer-exporter

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_dir', help='output copy dir')
    parser.add_argument('--area', help='geographical area name')
    parser.add_argument('--credential', help='path to earth explorer credential path')
    args = parser.parse_args()

    out_root_dir = Path(args.out_dir)
    # get area meta data
    area = args.area.lower()
    area_availables = list(area_metadata_dict.keys())
    area_availables.sort()
    if not area in area_availables :
        print(f"area should be a name in available area list : {area_availables}")
        return
    
    out_raw_img = out_root_dir/area/"IMG_RAW"
    area_meta = area_metadata_dict[area]
    raw_source = area_meta["raw_source"]
    img_dataset = area_meta["dataset"]
    bbox_wgs84 =  area_meta["bbox_wgs84"]
    dates_interval = area_meta["dates_interval"]    

    out_raw_img.mkdir(parents=True, exist_ok=True)

    if raw_source == "earth_explorer" :
        # log to earh explorer api
        cred_path = args.credential
        with open(cred_path) as ee_credentials :
            cred_dict = json.load(ee_credentials) 
            ee_user = cred_dict["user"]
            ee_psw = cred_dict["password"]
        usgs_api.logout()
        usgs_api.login(ee_user, ee_psw, save=True)

        # search image with usgs API
        res_image_search = usgs_api.scene_search(
            dataset=img_dataset, 
            ll= {"latitude": bbox_wgs84[0], "longitude": bbox_wgs84[1]}, 
            ur={"latitude": bbox_wgs84[2], "longitude": bbox_wgs84[3]}, 
            start_date=dates_interval[0], end_date=dates_interval[1])

        # print search result
        id_names = [ res_dict["entityId"] for res_dict in res_image_search['data']["results"]]
        print(f"found {len(id_names)} images")
        print(f"products names :\n{id_names}")

        # donwload data with retry 
        usgs_download_results(
            res_image_search['data']["results"], 
            out_root_path = out_raw_img, 
            usgs_dataset = img_dataset, 
            retry = [2, 10], 
            retry_wait=10)

        # extract raw data
        raw_img_list = [child for child in out_raw_img.iterdir() if child.is_file() and child.suffix == '.zip']
        for raw_img in raw_img_list:
            print(raw_img)
            extract_img_from_ee_zip(
                zip_file= raw_img, 
                out_root_dir = out_raw_img, 
                exts = ["tif", "tfw"] )



if __name__ == "__main__":
    main()
