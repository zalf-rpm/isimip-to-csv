#!/usr/bin/python
# -*- coding: UTF-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */

# Authors:
# Michael Berg-Mohnicke <michael.berg@zalf.de>
#
# Maintainers:
# Currently maintained by the authors.
#
# This file has been created at the Institute of
# Landscape Systems Analysis at the ZALF.
# Copyright (C: Leibniz Centre for Agricultural Landscape Research (ZALF)

import time
import os
import json
import sys

from netCDF4 import Dataset
import numpy as np

def main():

    config = {
        "path_to_file": "/run/user/1000/gvfs/sftp:host=login01.cluster.zalf.de,user=rpm/beegfs/common/data/climate/isimip/3b_v1.1_CMIP6/download/gfdl-esm4_r1i1p1f1_w5e5_historical_hurs_global_daily_1850_1850.nc",
        "var_name": "hurs",
        "lat_var_name": "lat",
        "lon_var_name": "lon"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            k, v = arg.split("=")
            if k in config:
                config[k] = v

    ds = Dataset(config["path_to_file"])
    lats = np.copy(ds.variables[config["lat_var_name"]])
    lons = np.copy(ds.variables[config["lon_var_name"]])
    ref_data = np.copy(ds.variables[config["var_name"]][0])

    lat_lon_grid_file = open("lat-lon.grid", "w")
    data_no_data_grid_file = open("data-no-data.grid", "w")
    latlon_to_rowcol_json_file = open("latlon-to-rowcol.json", "w")
    rowcol_to_latlon_json_file = open("rowcol-to-latlon.json", "w")

    lat_lon_grid_file.write("ncols 720\nnrows 360\nnodata_value --------------\n")
    data_no_data_grid_file.write("ncols 720\nnrows 360\nnodata_value 0\n")
    ll_to_rc_json_data = []
    rc_to_ll_json_data = []
  
    for row in range(0, 360):
        ll_line = []
        dnd_line = []
        for col in range(0, 720):
            lat = round(lats[row], 2)
            lon = round(lons[col], 2)

            is_data = int(ref_data[row, col]) < 1.0E19
            dnd_line.append("1" if is_data else "0")
            ll_to_rc_json_data.append([[lat, lon], [row + 1, col + 1]])
            rc_to_ll_json_data.append([[row + 1, col + 1], [lat, lon]])
            if is_data:
                ll_line.append("{:+06.2f}|{:+07.2f}".format(lat, lon))
            else:
                ll_line.append("--------------")

        lat_lon_grid_file.write(" ".join(ll_line))
        data_no_data_grid_file.write(" ".join(dnd_line))
        if row < 359:
            lat_lon_grid_file.write("\n")
            data_no_data_grid_file.write("\n")

        if row % 10 == 0:
            print("wrote line", row+1)
    
    json.dump(ll_to_rc_json_data, latlon_to_rowcol_json_file)#, indent=2)
    json.dump(rc_to_ll_json_data, rowcol_to_latlon_json_file)#, indent=2)

    lat_lon_grid_file.close()
    data_no_data_grid_file.close()
    latlon_to_rowcol_json_file.close()
    rowcol_to_latlon_json_file.close()
    ds.close()

main()