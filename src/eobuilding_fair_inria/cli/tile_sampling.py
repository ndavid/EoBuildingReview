import argparse
from pathlib import Path
from math import floor
import numpy as np
import itertools
import random

import fiona


# from fiona.crs import from_epsg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_tiles', help='input tiles file (shp)')
    parser.add_argument('--out_tiles', help='input tiles file (shp)', default=None)
    parser.add_argument('--n_samples', help='number of samples', type=int, default=None)
    parser.add_argument('--n_sam_gr', help='number of sample by group', type=int, default=None)
    parser.add_argument('--group_field', help='name of field used for tile grouping', default='id_field')
    parser.add_argument('--sample_field', help='name of field used for sampling result', default='sample')
    parser.add_argument('--seed', help='seed to use for random sampling', type=int, default=2023)

    args = parser.parse_args()
    in_tiles_path  = Path(args.in_tiles)
    
    # load tile
    with fiona.open(in_tiles_path) as tile_colx:
        tiles = [row for row in tile_colx]
        tile_profile = tile_colx.profile

    # check if group field exist.
    group = False
    group_field = args.group_field
    if group_field in tile_profile["schema"]["properties"] : 
        group = True

    # check sampling option
    n_samples = args.n_samples
    n_samples_group = args.n_sam_gr
    if n_samples and n_samples_group :
        print("options--n_samples and --n_sam_gr could not be used together, choose only one of them")
        return
    if n_samples_group and not group:
        print(f"options --n_sam_gr used but group field {group_field} not exist in input file")
        return

    # group tile if needed    
    if group :
        group_tiles = {}
        for idx, tile in enumerate(tiles) :        
            group_id = tile['properties'][group_field]
            if group_id in group_tiles:
                group_tiles[group_id].append(idx)
            else: 
                group_tiles[group_id] = [idx,]

    # sample tiles
    random.seed(args.seed)
    sample_idx = []
    if n_samples :
        idx = range(0, len(tiles))
        sample_idx = random.choices(idx, k=n_samples)

    if n_samples_group and group :
        for gr_id, gr_tiles in group_tiles.items() :
            gr_sample_idx = random.choices(gr_tiles, k=n_samples_group)
            sample_idx.extend(gr_sample_idx)

    # update sample field
    sample_field = args.sample_field
    tile_profile["schema"]["properties"][sample_field] = 'int'
    for tile in tiles :
        tile["properties"][sample_field] = 0

    for idx in sample_idx:
        tiles[idx]["properties"][sample_field] = 1

    if args.out_tiles :
        out_tiles_path = Path(args.out_tiles)
    else:
        out_tiles_path = in_tiles_path

    # update/wrtie result
    with fiona.open(out_tiles_path, "w", **tile_profile) as dst:
        for tile in tiles :
            dst.write(tile)