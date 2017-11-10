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
import math
import json
import csv
import itertools
#import copy
from StringIO import StringIO
from datetime import date, datetime, timedelta
from collections import defaultdict, OrderedDict
#import types
import sys
print sys.path
#import zmq
#print "pyzmq version: ", zmq.pyzmq_version(), " zmq version: ", zmq.zmq_version()

from netCDF4 import Dataset
import numpy as np

def main():

    config = {
        "path-to-data": "C:/Users/berg.ZALF-AD/Desktop/"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv

    ds = Dataset(config["path-to-data"] + "tas_bced_1960_1999_ipsl-cm5a-lr_hist_1971-1980.nc")
    lats = np.copy(ds.variables["lat"])
    lons = np.copy(ds.variables["lon"])
    temps = np.copy(ds.variables["tasAdjust"][0])

    lat_lon_grid_file = open("lat-lon.grid", "w")
    data_no_data_grid_file = open("data-no-data.grid", "w")
    lat_lon_json_file = open("lat-lon.json", "w")

    lat_lon_grid_file.write("NCOLS 720\n")
    lat_lon_grid_file.write("NROWS 360\n")
    data_no_data_grid_file.write("NCOLS 720\n")
    data_no_data_grid_file.write("NROWS 360\n")
    json_data = {"latlon-to-rowcol": [], "rowcol-to-latlon": []}
  
    for row in range(0, 360):
        ll_line = []
        dnd_line = []
        for col in range(0, 720):
            lat = round(lats[row], 2)
            lon = round(lons[col], 2)
            ll_line.append(str(lat) + "|" + str(lon))

            is_nodata = temps[row, col] > 1000 or temps[row, col] < -1000
            dnd_line.append("-" if is_nodata else "x")
            if is_nodata:
                json_data["latlon-to-rowcol"].append([[lat, lon], [row, col]])
                json_data["rowcol-to-latlon"].append([[row, col], [lat, lon]])
        lat_lon_grid_file.write(" ".join(ll_line))
        data_no_data_grid_file.write(" ".join(dnd_line))
        if row < 359:
            lat_lon_grid_file.write("\n")
            data_no_data_grid_file.write("\n")

        if row % 10 == 0:
            print "wrote line", row
    
    json.dump(json_data, lat_lon_json_file)#, indent=2)

    lat_lon_grid_file.close()
    data_no_data_grid_file.close()
    lat_lon_json_file.close()
    ds.close()

main()