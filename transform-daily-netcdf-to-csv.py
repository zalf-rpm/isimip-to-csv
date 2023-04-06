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

from collections import defaultdict
import csv
from datetime import date, timedelta
import sys
from netCDF4 import Dataset
import numpy as np
import os
import time

LOCAL_RUN = True


def main():
    # ilats = set()
    # ilons = set()
    # with open("working_resolution_to_climate_lat_lon_indices.json") as _:
    #    l = json.load(_)
    #    for i in xrange(0, len(l), 2):
    #        ilats.add(l[i+1][0])
    #        ilons.add(l[i+1][1])
    # print("min-lat:", min(ilats), "max-lat:", max(ilats))
    # print("min-lon:", min(ilons), "max-lons:", max(ilons))

    config = {
        "path_to_data": "/run/user/1000/gvfs/sftp:host=login01.cluster.zalf.de,user=rpm/beegfs/common/data/climate/isimip/grids/daily/" \
            if LOCAL_RUN else "/beegfs/common/data/climate/isimip/grids/daily/",
        "path_to_output": "out/" if LOCAL_RUN else "/beegfs/common/data/climate/isimip/csvs/",
        "start-y": "70",  # "75", #"1",
        "end-y": "87",  # "360",
        "start-x": "371",  # "372", #"1",
        "end-x": "393",  # "379", #"720",
        "start-year": None,  # "1971", #"2006",  # "1971",
        "end-year": None,  # "2005", #"2099",  # "2005",
        "start-doy": "1",
        "end-plus-doys": "366",  # "30",
        "model": "ipsl-cm5a-lr",  # "ipsl-cm5a-lr",  # "hadgem2-es"
        "rcp": "hist",  # "rcp4p5",
        "region": "nigeria"  # "germany"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            k, v = arg.split("=")
            if k in config:
                config[k] = v.lower() == "true" if v.lower() in ["true", "false"] else v

    if config["region"] == "nigeria":
        config["start-y"] = "151"
        config["end-y"] = "174"
        config["start-x"] = "364"
        config["end-x"] = "393"
    elif config["region"] == "germany":
        config["start-y"] = "70"
        config["end-y"] = "87"
        config["start-x"] = "371"
        config["end-x"] = "393"
    elif config["region"] == "earth":
        config["start-y"] = "1"
        config["end-y"] = "360"
        config["start-x"] = "1"
        config["end-x"] = "720"

    model_to_year_range = {
        "gfdl-esm2m": {"his": (1950, 2005), "rcp": (2006, 2099)},
        "hadgem2-es": {"his": (1950, 2004), "rcp": (2005, 2099)},
        "ipsl-cm5a-lr": {"his": (1971, 2005), "rcp": (2006, 2099)},
        "miroc-esm-chem": {"his": (1950, 2005), "rcp": (2006, 2099)},
        "noresm1-m": {"his": (1950, 2005), "rcp": (2006, 2099)},
    }

    if config["start-year"] is None:
        config["start-year"] = model_to_year_range[config["model"]][config["rcp"][:3]][0]
    if config["end-year"] is None:
        config["end-year"] = model_to_year_range[config["model"]][config["rcp"][:3]][1]

    elem_to_varname = {
        "tmin": {"prefix": "tasmin_bced_1960_1999", "var": "tasminAdjust", "folder": "tmin/"},
        "tavg": {"prefix": "tas_bced_1960_1999", "var": "tasAdjust", "folder": "tavg/"},
        "tmax": {"prefix": "tasmax_bced_1960_1999", "var": "tasmaxAdjust", "folder": "tmax/"},
        "precip": {"prefix": "pr_bced_1960_1999", "var": "prAdjust", "folder": "precip/"},
        "relhumid": {"prefix": "hurs", "var": "hurs", "folder": "relhumid/"},
        "globrad": {"prefix": "rsds_bced_1960_1999", "var": "rsdsAdjust", "folder": "short_rad/"},
        "wind": {"prefix": "wind_bced_1960_1999", "var": "windAdjust", "folder": "wind/"}
    }

    model_to_dir_name = {
        "gfdl-esm2m": "GFDL-ESM2M",
        "hadgem2-es": "HadGEM2-ES",
        "ipsl-cm5a-lr": "IPSL-CM5A-LR",
        "miroc-esm-chem": "MIROC-ESM-CHEM",
        "noresm1-m": "NorESM1-M"
    }

    rcp_to_dir_name = {"hist": "historical"}

    config["path_to_output"] += \
        config["region"] + "/" + \
        model_to_dir_name.get(config["model"], config["model"]) + "/" + \
        rcp_to_dir_name.get(config["rcp"], config["rcp"]) + "/" + \
        "r1i1p1/"

    files = defaultdict(lambda: defaultdict(dict))
    start_year = int(config["start-year"])
    end_year = int(config["end-year"])
    if config["rcp"] == "hist":
        if config["model"] != "ipsl-cm5a-lr":
            start_year = start_year + 1
        year_ranges = [[year, year + 9] for year in range(start_year, 2001, 10)] + [[2001, end_year]]
        if config["model"] != "ipsl-cm5a-lr":
            year_ranges = [[1950, 1950]] + year_ranges
    else:
        year_ranges = [[start_year, 2010]] + [[year, year + 9] for year in range(2011, 2091, 10)] + [[2091, end_year]]

    for start_year, end_year in year_ranges:
        for elem, dic in elem_to_varname.items():
            files[(start_year, end_year)][elem] = \
                config["path_to_data"] + dic["folder"] + config["rcp"] + "/" + dic["prefix"] + "_" + config["model"] + \
                "_" + config["rcp"] + "_" + str(start_year) + (
                    "-" + str(end_year) if start_year != end_year else "") + ".nc"

    def write_files(cache):
        no_of_files = len(cache)
        count = 0
        for (y, x), rows in cache.items():
            path_to_outdir = config["path_to_output"] + "row-" + str(y) + "/"
            if not os.path.isdir(path_to_outdir):
                os.makedirs(path_to_outdir)

            path_to_outfile = path_to_outdir + "col-" + str(x) + ".csv"
            if not os.path.isfile(path_to_outfile):
                with open(path_to_outfile, "wt") as _:
                    writer = csv.writer(_, delimiter=",")
                    writer.writerow(["iso-date", "tmin", "tavg", "tmax", "precip", "relhumid", "globrad", "windspeed"])
                    writer.writerow(["[]", "[°C]", "[°C]", "[°C]", "[mm]", "[%]", "[MJ m-2]", "[m s-1]"])

            with open(path_to_outfile, "at") as _:
                writer = csv.writer(_, delimiter=",")
                writer.writerows(rows)

            count = count + 1
            if count % 1000 == 0:
                print(count, "/", no_of_files, "written")

    write_files_threshold = 50  # ys

    for (start_year, end_year) in sorted(files.keys()):

        elem_to_file = files[(start_year, end_year)]

        if end_year < int(config["start-year"]):
            continue
        if int(config["end-year"]) < start_year:
            continue

        datasets = {}
        for elem, filepath in elem_to_file.items():
            datasets[elem] = Dataset(filepath, mode="r", format="NETCDF4")

        sum_days = 0
        for year in range(start_year, end_year + 1):

            clock_start_year = time.perf_counter()
            days_in_year = date(year, 12, 31).timetuple().tm_yday

            if year < int(config["start-year"]):
                sum_days = sum_days + days_in_year
                continue
            if year > int(config["end-year"]):
                break

            print("year:", year, "sum-days:", sum_days, "doy_i:",
                  (int(config["start-doy"]) + int(config["end-plus-doys"])), "ys ->", end=" ")

            days_per_loop = 31
            for doy_i in range(int(config["start-doy"]) - 1,
                               min(int(config["start-doy"]) + int(config["end-plus-doys"]), days_in_year),
                               days_per_loop):

                end_i = doy_i + days_per_loop if doy_i + days_per_loop < days_in_year else days_in_year
                data = {}
                for elem, ds in datasets.items():
                    data[elem] = np.copy(ds.variables[elem_to_varname[elem]["var"]][sum_days + doy_i: sum_days + end_i])

                ref_data = data["tavg"]
                no_of_days = ref_data.shape[0]
                cache = defaultdict(list)

                for y in range(int(config["start-y"]) - 1,
                               ref_data.shape[1] if int(config["end-y"]) < 0 else int(config["end-y"])):

                    # for x in range(ref_data.shape[2]):
                    for x in range(int(config["start-x"]) - 1,
                                   ref_data.shape[2] if int(config["end-x"]) < 0 else int(config["end-x"])):

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
                            cache[(y + 1, x + 1)].append(row)

                    print(y, end=" ")

                    if y > int(config["start-y"]) and (y - int(config["start-y"])) % write_files_threshold == 0:
                        print("")
                        s = time.perf_counter()
                        write_files(cache)
                        cache = defaultdict(list)
                        e = time.perf_counter()
                        print("wrote", write_files_threshold, "ys in", (e - s), "seconds")

                print("year:", year, "@ doy:", doy_i)

                # write remaining cache items
                write_files(cache)

            clock_end_year = time.perf_counter()
            print("running year", year, "took", (clock_end_year - clock_start_year), "seconds")

            sum_days = sum_days + days_in_year

        for _ in datasets.values():
            _.close()


if __name__ == "__main__":
    main()
