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

import gzip
from os import listdir, makedirs
from os.path import isfile, join, dirname, abspath, isdir, exists
import sys

base_path = dirname(abspath(__file__))
target_GCM = "GCMxy"
target_ssp = "ssp126"

print(target_GCM + " " + target_ssp)

def concatenate():

    config = {
        "base_path": "/beegfs/common/data/climate/isimip/AgMIP.input_csvs",
        "gcm": "GFDL-ESM4 ", #GFDL-ESM4 | IPSL-CM6A-LR | MPI-ESM1-2-HR | MRI-ESM2-0 | UKESM1-0-LL
        "ssp": "ssp126" #historical | picontrol | ssp126 | ssp585
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv
    print("config:", config)

    #input paths

    base_path = config["base_path"]
    gcm = config["gcm"]
    ssp = config["ssp"]

    historical_path = base_path + "/" + gcm + "/historical"
    ssp_path = base_path + "/" + gcm + "/" + ssp

    all_rows = [d for d in listdir(historical_path) if isdir(join(historical_path, d))]

    print("processing rows ...", flush=True)
    for row in all_rows:
        print(row, end=" ", flush=True)
        row_historical_path = join(historical_path, row)
        row_ssp_path = join(ssp_path, row)

        #output path
        out_ssp_path = join(base_path + "/concatenated/" + gcm + "/" + ssp, row)

        if not exists(out_ssp_path):
            makedirs(out_ssp_path)

        all_cols = [f for f in listdir(row_historical_path) if isfile(join(row_historical_path, f))]

        for col in all_cols:
            fout = gzip.open(out_ssp_path + "/" + col, 'wt')
            with gzip.open(row_historical_path + "/" + col, 'rt') as fin:
                #read header and skip units line
                header = next(fin)
                next(fin) 
                #write header and all data              
                fout.write(header)
                fout.write(fin.read())
            with gzip.open(row_ssp_path + "/" + col, 'rt') as fin:
                #read header and skip units line
                header = next(fin)
                next(fin)
                #write all data
                fout.write(fin.read())
            fout.close()

print("finished!")

if __name__ == "__main__":
    concatenate()

