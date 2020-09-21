#!/usr/bin/python
# -*- coding: UTF-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */

# Authors:
# Tommaso Stella <tommaso.stella@zalf.de>
# Michael Berg-Mohnicke <michael.berg@zalf.de>
#
# Maintainers:
# Currently maintained by the authors.
#
# This file has been created at the Institute of
# Landscape Systems Analysis at the ZALF.
# Copyright (C: Leibniz Centre for Agricultural Landscape Research (ZALF)

#remote debugging via commandline
#-m ptvsd --host 0.0.0.0 --port 14000 --wait

import gzip
from os import listdir, makedirs
from os.path import isfile, join, dirname, abspath, isdir, exists
import sys

def remove_units_row():

    config = {
        "base_path": "/beegfs/common/data/climate/isimip/AgMIP.input_csvs",
        "out_path": "/beegfs/common/data/climate/isimip/AgMIP.input_csvs/concatenated",
        "gcm": "UKESM1-0-LL", #GFDL-ESM4 | IPSL-CM6A-LR | MPI-ESM1-2-HR | MRI-ESM2-0 | UKESM1-0-LL
        "scen": "picontrol" # ssp126 | ssp585 | historical | picontrol
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv
    print("config:", config)

    base_path = config["base_path"]
    out_path = config["out_path"]
    gcm = config["gcm"]
    scen = config["scen"]

    #input paths
    scen_path = base_path + "/" + gcm + "/" + scen
    out_scen_path = out_path + "/" + gcm + "/" + scen

    all_rows = [d for d in listdir(scen_path) if isdir(join(scen_path, d))]

    print("processing rows ...", flush=True)
    for row in all_rows:
        print(row, end=" ", flush=True)
        row_scen_path = join(scen_path, row)

        #output path
        out_row_scen_path = join(out_scen_path, row)

        if not exists(out_row_scen_path):
            makedirs(out_row_scen_path)

        all_cols = [f for f in listdir(row_scen_path) if isfile(join(row_scen_path, f))]

        for col in all_cols:
            fout = gzip.open(out_row_scen_path + "/" + col, 'wt')
            with gzip.open(row_scen_path + "/" + col, 'rt') as fin:
                #read header and skip units line
                header = next(fin)
                next(fin) 
                #write header and all data              
                fout.write(header)
                fout.write(fin.read())
            fout.close()

    print("finished!")

if __name__ == "__main__":
    remove_units_row()

