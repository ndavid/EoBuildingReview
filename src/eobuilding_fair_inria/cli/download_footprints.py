import argparse

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

def  download_austin_footprint(out_dir):

    url = "https://data.austintexas.gov/api/geospatial/3qcc-8uhz?accessType=DOWNLOAD&method=export&format=Shapefile"
    out_name = "Austin_Building_Footprints_2013.zip"
    out_path= Path(out_dir)/out_name

    # download(url, out_path)
    r = requests.get(url, allow_redirects=True)
    open(out_path, 'wb').write(r.content)
    
    with zipfile.ZipFile(out_path,"r") as zip_ref:
        zip_ref.extractall(Path(out_dir))
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_dir', help='output copy dir')
    args = parser.parse_args()

    download_austin_footprint(args.out_dir)
    
    # rename shapefile
    out_path= Path(args.out_dir)
    shp_files = [ f for f in out_path.listdir() if f.suffix in ["shp", "shx", "prj", "dbf"]]
    for s_file in shp_files :
        ext = s_file.suffix
        new_name = out_path/f"Austin_Building_Footprints_2013.{ext}"
        s_file.rename(new_name)

if __name__ == "__main__":
    main()
