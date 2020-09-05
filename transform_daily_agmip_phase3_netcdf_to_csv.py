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

from collections import defaultdict, OrderedDict
import csv
from datetime import date, datetime, timedelta
import gzip
#import itertools
import json
import math
import os
#from StringIO import StringIO
import sys
import time

from netCDF4 import Dataset
import numpy as np

#remote debugging via commandline
#-m ptvsd --host 0.0.0.0 --port 14000 --wait

#------------------------------------------------------------------------------

def main():

    #ilats = set()
    #ilons = set()
    #with open("working_resolution_to_climate_lat_lon_indices.json") as _:
    #    l = json.load(_)
    #    for i in xrange(0, len(l), 2):
    #        ilats.add(l[i+1][0])
    #        ilons.add(l[i+1][1])
    #print "min-lat:", min(ilats), "max-lat:", max(ilats)
    #print "min-lon:", min(ilons), "max-lons:", max(ilons)


    config = {
        "path_to_data": "/beegfs/common/data/climate/isimip/AgMIP.input/phase3",
        "path_to_output": "/beegfs/common/data/climate/isimip/AgMIP.input_csvs",
        "start_y": "1", #"75", #"1",
        "end_y": None, #"360", 
        "start_x": "1", #"372", #"1",
        "end_x": None, #"379", #"720",
        "start_year": None,
        "end_year": None,
        "start_doy": "1",
        "end_plus_doys": "366", #"30",
        "gcm": "GFDL-ESM4", #"GFDL-ESM4 | IPSL-CM6A-LR | MPI-ESM1-2-HR | MRI-ESM2-0 | UKESM1-0-LL"
        "scen": "historical", #"historical | picontrol | ssp126 | ssp585"
        "write_files_threshold": "50",
        "days_per_loop": "31"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv
    print("config:", config)

    elem_to_var = {
        "tmin": "tasmin",
        "tavg": "tas",
        "tmax": "tasmax",
        "precip": "pr",
        "relhumid": "hurs",
        "globrad": "rsds",
        "wind": "sfcwind"
    }
    var_to_elem = {v : k for k, v in elem_to_var.items()}

    files = defaultdict(dict)
    
    # sort files in dir
    path = config["path_to_data"] + "/" + config["scen"] + "/" + config["gcm"]
    for file in os.listdir(path):
        if file[-3:] != ".nc":
            continue
        _gcm, _1, _2, _scen, var, _global, _daily, from_year_str, to_year_str_nc = file.split("_")
        from_year = int(from_year_str)
        to_year = int(to_year_str_nc[:-3])

        # store the paths we are interested in    
        if var in var_to_elem:
            files[(from_year, to_year)][var_to_elem[var]] = path + "/" + file 
        else:
            continue


    def write_files(cache):
        no_of_files = len(cache)
        count = 0
        for (y, x), rows in cache.items():
            path_to_outdir = config["path_to_output"] + "/row-" + str(y)
            if not os.path.isdir(path_to_outdir):
                os.makedirs(path_to_outdir)

            path_to_outfile = path_to_outdir + "/col-" + str(x) + ".csv.gz"
            if not os.path.isfile(path_to_outfile):
                with gzip.open(path_to_outfile, "wt") as _:
                    writer = csv.writer(_, delimiter=",")
                    writer.writerow(["iso-date", "tmin", "tavg", "tmax", "precip", "relhumid", "globrad", "windspeed"])
                    writer.writerow(["[]", "[°C]", "[°C]", "[°C]", "[mm]", "[%]", "[MJ m-2]", "[m s-1]"])

            with gzip.open(path_to_outfile, "at") as _:
                writer = csv.writer(_, delimiter=",")
                for row in rows:
                    writer.writerow(row)

            count = count + 1
            if count % 1000 == 0:
                print(count, "/", no_of_files, "written")


    write_files_threshold = int(config["write_files_threshold"]) #50 #ys

    for start_year, end_year in sorted(files.keys()):

        elem_to_file = files[(start_year, end_year)]

        if config["start_year"] and end_year < int(config["start_year"]):
            continue
        if config["end_year"] and int(config["end_year"]) < start_year:
            continue

        datasets = {}
        for elem, filepath in elem_to_file.items():
            datasets[elem] = Dataset(filepath) 

        sum_days = 0
        for year in range(start_year, end_year + 1):

            clock_start_year = time.time()
            days_in_year = date(year, 12, 31).timetuple().tm_yday

            if config["start_year"] and year < int(config["start_year"]):
                sum_days = sum_days + days_in_year
                continue
            if config["end_year"] and year > int(config["end_year"]):
                break

            print("year:", year, "sum-days:", sum_days, "ys ->", flush=True)

            days_per_loop = int(config["days_per_loop"]) #31
            for doy_i in range(int(config["start_doy"]) - 1, min(int(config["start_doy"]) + int(config["end_plus_doys"]), days_in_year), days_per_loop):

                end_i = doy_i + days_per_loop if doy_i + days_per_loop < days_in_year else days_in_year
                data = {} 
                for elem, ds in datasets.items():
                    data[elem] = np.copy(ds.variables[elem_to_var[elem]][sum_days + doy_i : sum_days + end_i])

                ref_data = data["tavg"]
                no_of_days = ref_data.shape[0] 
                cache = defaultdict(list)

                for y in range(int(config["start_y"]) - 1, ref_data.shape[1] if not config["end_y"] else int(config["end_y"])):

                    #for x in range(ref_data.shape[2]):
                    for x in range(int(config["start_x"]) - 1, ref_data.shape[2] if not config["end_x"] else int(config["end_x"])):

                        if int(ref_data[0, y, x]) > 1.0E19:
                            continue

                        for i in range(no_of_days):
                            row = [
                                (date(year, 1, 1) + timedelta(days=doy_i + i)).strftime("%Y-%m-%d"),
                                str(round(data["tmin"][i, y, x] - 273.15, 2)),
                                str(round(data["tavg"][i, y, x] - 273.15, 2)),
                                str(round(data["tmax"][i, y, x] - 273.15, 2)),
                                str(round(data["precip"][i, y, x] * 60 * 60 * 24, 2)),
                                str(round(data["relhumid"][i, y, x], 2)),
                                str(round(data["globrad"][i, y, x] * 60 * 60 * 24 / 1000000, 4)),
                                str(round(data["wind"][i, y, x], 2))
                            ]
                            cache[(y,x)].append(row)

                    print(y, end=" ", flush=True) 

                    if y > int(config["start_y"]) and (y - int(config["start_y"])) % write_files_threshold == 0:
                        print()
                        s = time.time()
                        write_files(cache)
                        cache = defaultdict(list)
                        e = time.time()
                        print("wrote", write_files_threshold, "ys in", (e-s), "seconds")

                print()

                #write remaining cache items
                write_files(cache)

                clock_end_year = time.time()
                print("running year", year, "took", (clock_end_year - clock_start_year), "seconds")

            sum_days = sum_days + days_in_year

        for _ in datasets.values():
            _.close()


if __name__ == "__main__":
    main()