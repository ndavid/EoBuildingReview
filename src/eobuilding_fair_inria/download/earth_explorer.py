import time
import json
import zipfile

from pathlib import Path
from tqdm import tqdm

from usgs import api as usgs_api
from eobuilding_fair_inria.download.utils import convert_size, download_url


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
 
 
def usgs_download_results(search_results, out_root_path, usgs_dataset, retry = [2, 10], retry_wait=10): 

    tot_download = len(search_results)

    for download_retry in retry :
        for i, result in enumerate(search_results, start=1) :
            entity_id = result["entityId"]
            local_path = out_root_path/f"{entity_id}.zip"
            if local_path.exists():
                print(f" donwload file {i}/{tot_download} : {entity_id} of dataset {usgs_dataset} already downloaded on path {local_path}")
                continue

            download_options = usgs_api.download_options(usgs_dataset, entity_id)
            product_idx = [ option["id"] for option in download_options['data'] if option['available'] == True]
            product_id = product_idx[0]
            download_option =  [ option for option in download_options['data'] if option['id'] == product_id][0]
            file_size = (download_option['filesize'])
            file_size_str = convert_size(file_size)
            
            print(f" download file {i}/{tot_download} : {entity_id} of dataset {usgs_dataset} with product_id {product_id} and file_size {file_size_str}")

            # test if product already asked by previous request / api call
            labels = [product_id]
            download_request = usgs_api.download_request(usgs_dataset, entity_id, product_id)
            print(download_request)
            if 'duplicateProducts' in download_request['data'] :
                duplicates = download_request['data']['duplicateProducts']
                if duplicates :
                    for product in duplicates.values():
                        if product not in labels:
                            labels.append(product)

            download_meta = {}
            for label in labels:
                download_search = usgs_download_search(label)
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
                    download_request_updated = usgs_download_retrieve(label)
                    for download_update in download_request_updated["data"]['available'] :
                        download_id = download_update['downloadId']
                        display_id = download_meta[download_id]['displayId']
                        url = download_update['url']
                        print(f"data available at url : {url}")
                        print(f"display_idd : {display_id}")
                        
                        download_url(url, local_path)
                        download_meta[download_id].update({'url': url, 'local_path': local_path})
                        is_downloaded = True
                if not is_downloaded and count < download_retry :
                    print(f'M2M.retrieveScenes - download are not available. Waiting {retry_wait} seconds...')
                    time.sleep(retry_wait)


def extract_img_from_ee_zip(zip_file, out_root_dir, exts = ["tif", "tfw"] ):
    # zip file handler  
    zip = zipfile.ZipFile(zip_file)
    # list available files in the container
    zip_files = zip.namelist()
    zip_extracts = [ file for file in zip_files if file[-3:] in exts]
    print(zip_extracts)
    for file_extract in zip_extracts:
        zip_path = Path(file_extract)
        # extract a specific file from the zip container
        f = zip.open(file_extract)
        # save the extraced file 
        content = f.read()
        f = open(out_root_dir/zip_path.name, 'wb')
        f.write(content)
        f.close()