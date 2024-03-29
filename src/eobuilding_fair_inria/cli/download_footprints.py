import argparse
from operator import truediv
import shutil
from pathlib import Path
import requests
import zipfile
from zipfile import BadZipfile
from tqdm import tqdm
import time

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
    },
    "bloomington_recent" : {
        "source_type" : "url_download",
        "url" : "https://data.bloomington.in.gov/api/geospatial/vjpj-6g5i?accessType=DOWNLOAD&method=export&format=Shapefile",
        "in_prefix" : "geo_export_",
        "out_name" : "Bloomington_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "chicago" : {
        "source_type" : "url_download",
        "url" : "https://data.cityofchicago.org/api/geospatial/hz9b-7nh8?method=export&format=Shapefile",
        "in_prefix" : "Buildings",
        "out_name" : "Chicago_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "kitsap" : {
        "source_type" : "url_download",
        "url" : "https://ftp.co.kitsap.wa.us/data/gis/datacd/arcview/library/parcel.zip",
        "in_prefix" : "footprints",
        "out_name" : "Kitsap_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "sfo" : {
        "source_type" : "url_download",
        "url" : "https://geodata.mit.edu/mit_download/mit-dqtbhcmu3fmjk",
        "in_prefix" : "",
        "out_name" : "SanFrancisco_Building_Footprints_2011.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "innsbruck" : {
        "source_type" : "url_download",
        "url" : "https://opendata.arcgis.com/api/v3/datasets/9fa2f10f991c46739d51e77dbbd39534_0/downloads/data?format=shp&spatialRefId=31254&where=1%3D1",
        "in_prefix" : "Gebaeude",
        "out_name" : "Tyrol_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "tyrol-e" : {
        "source_type" : "url_download",
        "url" : "https://opendata.arcgis.com/api/v3/datasets/9fa2f10f991c46739d51e77dbbd39534_0/downloads/data?format=shp&spatialRefId=31254&where=1%3D1",
        "in_prefix" : "Gebaeude",
        "out_name" : "Tyrol_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "tyrol_w" : {
        "source_type" : "url_download",
        "url" : "https://opendata.arcgis.com/api/v3/datasets/9fa2f10f991c46739d51e77dbbd39534_0/downloads/data?format=shp&spatialRefId=31254&where=1%3D1",
        "in_prefix" : "Gebaeude",
        "out_name" : "Tyrol_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "vienna" : {
        "source_type" : "url_download",
        "url" : "https://data.wien.gv.at/daten/geo?service=WFS&version=1.0.0&request=GetFeature&typeName=ogdwien:FMZKGEBOGD&outputFormat=shape-zip&SRS=EPSG:31256&BBOX=-2237,335400,6828,344450",
        "in_prefix" : "FMZKGEBOGDPolygon",
        "out_name" : "Vienna_Building_Footprints.zip",
        "unzip" : True,
        "file_type" : "SHP"
    },
    "vienna_all" : {
        "source_type" : "wfs",
        "url" : "https://data.wien.gv.at/daten/geo?service=WFS&version=1.0.0&request=GetFeature&typeName=ogdwien:FMZKGEBOGD&outputFormat=shape-zip&SRS=EPSG:31256",
        "in_prefix" : "FMZKGEBOGDPolygon",
        "bbox" : [-20000, 325000, 25000, 365000],
        "step" : 5000,
        "out_name" : "Vienna_Building_Footprints_all",
        "unzip" : True,
        "file_type" : "SHP"
    }
} 

# https://data.world/city-of-bloomington/522d7f69-8951-46f6-8cb4-30cad69878ca
# https://data.sfgov.org/Geographic-Locations-and-Boundaries/Building-Footprints/ynuv-fyni

# dataworld API : https://download.data.world/datapackage/city-of-bloomington/522d7f69-8951-46f6-8cb4-30cad69878ca
# need token header

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
    if  source_type not in ["url_download", "wfs"] :
        print(f"source type {source_type} is not supported yet")
        return

    if source_type == "url_download" :
        url = area_meta["url"]
        out_name =  area_meta["out_name"]
        out_path= out_raw_footprints/out_name

        # download(url, out_path)
        r = requests.get(url, allow_redirects=True)
        open(out_path, 'wb').write(r.content)
        download_paths = [out_path]
        extract_dir = out_raw_footprints
    
    if source_type == "wfs" :
        url = area_meta["url"]
        out_name =  area_meta["out_name"]
        out_dir_path= out_raw_footprints/out_name
        out_dir_path.mkdir(parents=True, exist_ok=True)

        xmin, ymin, xmax, ymax =  area_meta["bbox"]
        step =  area_meta["step"]

        download_paths = []
        extract_dir = out_dir_path
        for x in range(xmin, xmax, step) :
            for y in  range(ymin, ymax, step) :
                out_bbox_path = out_dir_path/f"{x}_{y}.zip"
                download_paths.append(out_bbox_path)

                wfs_query = f"{url}&BBOX={x},{y},{x+step},{y+step}"
                print(wfs_query)
                # download(url, out_path)
                if not out_bbox_path.exists():
                    r = requests.get(wfs_query, allow_redirects=True)
                    open(out_bbox_path, 'wb').write(r.content)
                    time.sleep(10)
                else:
                    print(f"{out_bbox_path} already downloaded")
                    time.sleep(2)


    add_count_suffix = False
    if len(download_paths) > 1 :
        add_count_suffix = True

    for i, download_path in enumerate(download_paths):

        # extract data if zip
        if area_meta["unzip"] :
            try :
                with zipfile.ZipFile(download_path,"r") as zip_ref:
                    zip_ref.extractall(extract_dir)
            except BadZipfile:
                print(f"{download_path} is not a valid zip archive, skip and pass to next")
                continue 
                
        # rename file
        renames_files = []
        out_prefix = download_path.stem
        if add_count_suffix:
            out_prefix = f"{out_prefix}_{i:04d}"
        shp_suffix = [".shp", ".shx", ".prj", ".dbf", ".shx", ".sbn", ".sbx", ".cst", ".xml"]
        if "in_subdir" in area_meta:
            out_init_dir = extract_dir/area_meta["in_subdir"]
        else:
            out_init_dir = extract_dir
        if area_meta["file_type"] == "SHP" :
            renames_files = [ child for child in out_init_dir.iterdir() 
                            if child.is_file() 
                            and area_meta["in_prefix"] in child.stem
                            and child.suffix in shp_suffix]
        for s_file in renames_files :
            ext = s_file.suffix
            new_name = extract_dir/f"{out_prefix}{ext}"
            s_file.rename(new_name)

        # remove extract dirs if needed
        if area_meta["unzip"] :
            with zipfile.ZipFile(download_path,"r") as zip_ref:
                relativepaths = [child for child in zipfile.Path(zip_ref).iterdir() if child.is_dir()]
            if relativepaths :
                for relativepath in relativepaths:
                    print(relativepath.name)
                    extract_root_dir = extract_dir/relativepath.name
                    try:
                        shutil.rmtree(extract_root_dir)
                    except OSError as o:
                        print(f"Error, {o.strerror}: {extract_root_dir}")

                
if __name__ == "__main__":
    main()
