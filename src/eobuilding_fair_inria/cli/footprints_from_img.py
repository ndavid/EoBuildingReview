import argparse
from pathlib import Path
import glob
import numpy as np

import rasterio
import fiona
from fiona import Feature, Geometry
from shapely.geometry import mapping, shape
from shapely import Polygon

# from fiona.crs import from_epsg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_name', help='name of output footprints shapefiles')
    parser.add_argument('--in_img', help='path to input images with regex')
    parser.add_argument('--out_dir', help='path for output footprints')

    args = parser.parse_args()

    in_img_template = args.in_img
    in_img_list = glob.glob(in_img_template)
    in_footprints_dict = {}
    in_footprints_crs = []
    for img_name in in_img_list : 
        img_path = Path(img_name)
        with rasterio.open(img_path) as img_ds :
            # print(f"{img_path.name} {img_ds.bounds}")
            # print(f"{**(img_ds.bounds)}")
            (xmin, ymin, xmax, ymax) = img_ds.bounds
            in_footprints_dict[img_path.stem] = Polygon.from_bounds(xmin, ymin, xmax, ymax)
            in_footprints_crs.append(img_ds.crs)

    # print(in_footprints_crs[0])
    out_name = args.out_name
    out_dir = Path(args.out_dir)
    out_shp_name = out_dir/f"{out_name}.shp"
    
    profile = dict()
    profile["schema"] = {
        "geometry" : "Polygon",
        "properties" : {
            "name" : 'str'}
        }
    profile["driver"] = 'Shapefile'
    profile["crs"] = in_footprints_crs[0]

    with fiona.open(out_shp_name, "w", **profile) as dst:
        for name, poly in in_footprints_dict.items() :
                elem = {}
                geojson = mapping(poly)
                geojson['coordinates'] = np.round(np.array(geojson['coordinates']), 4)
                elem['geometry'] =geojson
                elem['properties'] = {"name" : name}
                dst.write(elem)



