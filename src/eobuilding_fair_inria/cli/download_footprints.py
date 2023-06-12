import argparse
import shutil
from pathlib import Path
import requests
import zipfile
from tqdm import tqdm


def download(url, fname):
    resp = requests.get(url, stream=True, allow_redirects=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
  
       
area_metadata_dict = {
    "austin" : {
        "source_type" : "url_download",
        "url" : "https://data.austintexas.gov/api/geospatial/3qcc-8uhz?accessType=DOWNLOAD&method=export&format=Shapefile",
        "out_name" : "Austin_Building_Footprints_2013.zip",
        "in_prefix" : "geo_export_",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "bellingham" : {
        "source_type" : "url_download",
        "url" : "https://data.cob.org/data/gis/SHP_Files/COB_struc_shps.zip",
        "in_subdir" : "COB_Shps",
        "in_prefix" : "COB_struc_Buildings",
        "out_name" : "Bellingham_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    }
} 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_dir', help='output copy dir')
    parser.add_argument('--area', help='geographical area name')
    args = parser.parse_args()

    out_root_dir = Path(args.out_dir)
    
    # get area meta data
    area = args.area.lower()
    area_availables = list(area_metadata_dict.keys())
    area_availables.sort()
    if not area in area_availables :
        print(f"area should be a name in available area list : {area_availables}")
        return
    area_meta = area_metadata_dict[area]
    source_type = area_meta["source_type"]
    
    # create out dir
    out_raw_footprints = out_root_dir/area/"FOOTPRINT_RAW"
    out_raw_footprints.mkdir(parents=True, exist_ok=True)

    # download data
    if source_type == "url_download" :
        url = area_meta["url"]
        out_name =  area_meta["out_name"]
        out_path= out_raw_footprints/out_name

        # download(url, out_path)
        r = requests.get(url, allow_redirects=True)
        open(out_path, 'wb').write(r.content)
    else :
        print(f"source type {source_type} is not supported yet")
        return
     
    # extract data if zip
    if area_meta["unzip"] :
        with zipfile.ZipFile(out_path,"r") as zip_ref:
            zip_ref.extractall(out_raw_footprints)
    
    # rename file
    renames_files = []
    if "in_subdir" in area_meta:
        out_init_dir = out_raw_footprints/area_meta["in_subdir"]
    else:
        out_init_dir = out_raw_footprints
    if area_meta["file_type"] == "SHP" :
        renames_files = [ child for child in out_init_dir.iterdir() 
                         if child.is_file() 
                         and area_meta["in_prefix"] in child.stem
                         and child.suffix in [".shp", ".shx", ".prj", ".dbf", ".shx", ".sbn"]]
    for s_file in renames_files :
        ext = s_file.suffix
        new_name = out_raw_footprints/f"{out_name}{ext}"
        s_file.rename(new_name)

    # remove extract dirs if needed
    if area_meta["unzip"] :
        with zipfile.ZipFile(out_path,"r") as zip_ref:
            relativepaths = [child for child in zipfile.Path(zip_ref).iterdir() if child.is_dir()]
        if relativepaths :
            for relativepath in relativepaths:
                print(relativepath.name)
                extract_root_dir = out_raw_footprints/relativepath.name
                try:
                    shutil.rmtree(extract_root_dir)
                except OSError as o:
                    print(f"Error, {o.strerror}: {extract_root_dir}")
                
if __name__ == "__main__":
    main()
