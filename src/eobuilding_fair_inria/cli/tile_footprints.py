import argparse
from pathlib import Path
from math import floor
import glob
import numpy as np
import itertools

import fiona
from fiona import Feature, Geometry
from shapely.geometry import mapping, shape
from shapely import Polygon

# from fiona.crs import from_epsg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_fp', help='input footprint file (shp)')
    parser.add_argument('--size_m', help='size of tile in meters', type=float)
    parser.add_argument('--id_field', help='name for intiale id')
    parser.add_argument('--out_tiles', help='output tiles/windows vector files (shp)')

    args = parser.parse_args()
    in_footprints_path  = Path(args.in_fp)
    
    with fiona.open(in_footprints_path) as fp_colx:
        footprints = [row for row in fp_colx]
        profile = fp_colx.profile

    out_shp_name = Path(f"{args.out_tiles}.shp")
    ini_id_field = args.id_field
    size_m = args.size_m

    profile["schema"] = {
        "geometry" : "Polygon",
        "properties" : {
            "id_field" : 'str',
            "name" : 'str'}
        }
    profile["driver"] = 'Shapefile'

    with fiona.open(out_shp_name, "w", **profile) as dst:
        for footprints_dict in footprints :
            (xf_min, yf_min, xf_max, yf_max) = shape(footprints_dict["geometry"]).bounds
            x_num = floor((xf_max - xf_min) / size_m)
            y_num = floor((yf_max - yf_min) / size_m)
            print(f"{xf_min} {yf_min} {xf_max} {yf_max}")
            print(f"{x_num} {y_num} ")

            id_field = footprints_dict['properties'][ini_id_field]
            for i, j in itertools.product(range(0, x_num), range(0, y_num) ):
                print(f"{i} {j} ")

                xt_min = xf_min + i*size_m
                yt_min = yf_min + j*size_m
                xt_max = xt_min + size_m
                yt_max = yt_min + size_m
                tile_geom = Polygon.from_bounds(xt_min, yt_min, xt_max, yt_max)
                
                elem = {}
                geojson = mapping(tile_geom)
                geojson['coordinates'] = np.round(np.array(geojson['coordinates']), 4)
                elem['geometry'] = geojson
                elem['properties'] = {
                    "name" : f"{id_field}_{i:02d}-{j:02d}",
                    "id_field" : id_field }
                dst.write(elem)