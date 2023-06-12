import argparse
import math
import time
import json

import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

from usgs import api as usgs_api


def usgs_download_search(label, api_key=None):
    payload = { "label": label }
    api_key = usgs_api._get_api_key(api_key)
    with usgs_api._create_session(api_key) as session:
        url = '{}/download-search'.format(usgs_api.USGS_API)
        r = session.post(url, json.dumps(payload))
    response = r.json()
    usgs_api._check_for_usgs_error(response)
    return response


def usgs_download_retrieve(label, api_key=None):
    payload = { "label": label }
    api_key = usgs_api._get_api_key(api_key)
    with usgs_api._create_session(api_key) as session:
        url = '{}/download-retrieve'.format(usgs_api.USGS_API)
        r = session.post(url, json.dumps(payload))
    response = r.json()
    usgs_api._check_for_usgs_error(response)
    return response


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return f"{s} { size_name[i]}"


def download_url(url: str, fname: Path, chunk_size=1024):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname.name,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)



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
    }
}

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

        # search image with usgd API
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
        tot_download = len(res_image_search['data']["results"])
        for download_retry in [2, 10] :
            for i, result in enumerate(res_image_search['data']["results"], start=1) :
                entity_id = result["entityId"]
                download_options = usgs_api.download_options(img_dataset, entity_id)
                product_idx = [ option["id"] for option in download_options['data'] if option['available'] == True]
                product_id = product_idx[0]
                download_option =  [ option for option in download_options['data'] if option['id'] == product_id][0]
                file_size = (download_option['filesize'])
                file_size_str = convert_size(file_size)
                local_path = out_raw_img/f"{entity_id}.zip"
                if local_path.exists():
                    print(f" donwload file {i}/{tot_download} : {entity_id} of dataset {img_dataset} already downloaded on path {local_path}")
                    continue
                
                print(f" download file {i}/{tot_download} : {entity_id} of dataset {img_dataset} with product_id {product_id} and file_size {file_size_str}")
                download_request = usgs_api.download_request(img_dataset, entity_id, product_id)
                print(download_request)
                
                # test if product already asked by previous request / api call
                labels = [product_id]
                if 'duplicateProducts' in download_request['data'] :
                    duplicates = download_request['data']['duplicateProducts']
                    if duplicates :
                        for product in duplicates.values():
                            if product not in labels:
                                # print(product)
                                labels.append(product)
                # print(labels)
                download_meta = {}
                for label in labels:
                    download_search = usgs_download_search(label)
                    # print(f" download_search label={label} : {download_search}")
                    if download_search['data'] is not None:
                        for ds in download_search['data']:
                            download_meta.update({ds['downloadId']: ds})
                print(f" download_meta : {download_meta}")

                # download
                is_downloaded = False
                count = 0
                while not is_downloaded and count < download_retry:
                    count +=1 
                    for label in labels:
                        # print(f"label {label}")
                        download_request_updated = usgs_download_retrieve(label)
                        # print(download_request_updated)
                        for download_update in download_request_updated["data"]['available'] :
                            download_id = download_update['downloadId']
                            display_id = download_meta[download_id]['displayId']
                            url = download_update['url']
                            print(f"data available at url : {url}")
                            print(f"display_idd : {display_id}")

                            # TODO real download
                            
                            download_url(url, local_path)
                            
                            download_meta[download_id].update({'url': url, 'local_path': local_path})
                            is_downloaded = True
                    if not is_downloaded and count < download_retry :
                        print('M2M.retrieveScenes - download are not available. Waiting 10 seconds...')
                        time.sleep(10)

        # extract raw data
        raw_img_list = [child for child in out_raw_img.iterdir() if child.is_file() and child.suffix == '.zip']
        for raw_img in raw_img_list:
            print(raw_img)

            # zip file handler  
            zip = zipfile.ZipFile(raw_img)
            # list available files in the container
            zip_files = zip.namelist()
            zip_extracts = [ file for file in zip_files if file[-3:] in ["tif", "tfw"]]
            print(zip_extracts)
            for file_extract in zip_extracts:
                zip_path = Path(file_extract)
                # extract a specific file from the zip container
                f = zip.open(file_extract)
                # save the extraced file 
                content = f.read()
                f = open(out_raw_img/zip_path.name, 'wb')
                f.write(content)
                f.close()


if __name__ == "__main__":
    main()
