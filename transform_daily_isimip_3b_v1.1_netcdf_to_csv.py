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
import shutil
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
        "path_to_data": "/beegfs/common/data/climate/isimip/3b_CMIP6/download/",
        #"path_to_data": "/run/user/1000/gvfs/sftp:host=login01.cluster.zalf.de,user=rpm/beegfs/common/data/climate/isimip/3b_CMIP6/download/",
        "path_to_scratch": "/scratch/isimip_3b_csvs/",
        #"path_to_scratch": "scratch/isimip_3b_csvs/",
        "path_to_output": "/beegfs/common/data/climate/isimip/3b_CMIP6/csvs/",
        #"path_to_output": "/run/user/1000/gvfs/sftp:host=login01.cluster.zalf.de,user=rpm/beegfs/common/data/climate/isimip/3b_CMIP6/csvs/",
        "start_y": "1", #"75", #"1",
        "end_y": None, #"360", 
        "start_x": "1", #"372", #"1",
        "end_x": None, #"379", #"720",
        "start_year": None,
        "end_year": None,
        "start_doy": "1",
        "end_plus_doys": "366", #"30",
        "gcm": "GFDL-ESM4", #GFDL-ESM4 | IPSL-CM6A-LR | MPI-ESM1-2-HR | MRI-ESM2-0 | UKESM1-0-LL
        "scen": "historical", #historical | picontrol | ssp126 | ssp370 | ssp585
        "write_files_threshold": "365", #"50",
        "days_per_loop": "31"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            k, v = arg.split("=")
            if k in config:
                config[k] = v.lower() == "true" if v.lower() in ["true", "false"] else v
    print("config:", config)

    #print("deleting previous scratch files from", config["path_to_scratch"])
    #shutil.rmtree(config["path_to_scratch"], ignore_errors=True)
    #print("done deleting scratch files")

    if os.path.exists("/scratch"):
        print("deleting * in scratch folder")
        for entry in os.scandir("/scratch"):
            if entry.is_dir():
                print(entry.path)
                #shutil.rmtree(entry.path, ignore_errors=True)
            elif entry.is_file():
                print(entry.path)
                #os.remove(entry.path)
        print("done deleting * in scratch folder")

    elem_to_var = {
        "tmin": "tasmin",
        "tavg": "tas",
        "tmax": "tasmax",
        "precip": "pr",
        "relhumid": "hurs",
        "specificHumidity": "huss",
        "globrad": "rsds",
        "wind": "sfcwind",
        "snowfallFlux": "prsn",
        "airpress": "ps",
        "surfaceDownwellingLongwaveRadiation": "rlds",
    }
    var_to_elem = {v : k for k, v in elem_to_var.items()}

    files = defaultdict(dict)

    ensmem_set = set()
    # sort files in dir
    path = config["path_to_data"] 
    for file in os.listdir(path):
        if file[-3:] != ".nc":
            continue
        split = file.split("_")
        if len(split) == 9: 
            gcm, ensmem, _input_dataset_name, scen, var, _global, _daily, from_year_str, to_year_str_nc = split
            if config["scen"].lower() != scen.lower() or config["gcm"].lower() != gcm.lower():
                #print("skipping file", file, "because of scen or gcm mismatch")
                continue
            ensmem_set.add(ensmem)
        else:
            print("Error: File ", file, " has unknown filename structure!")
            exit(1)
        from_year = int(from_year_str)
        to_year = int(to_year_str_nc[:-3])

        # store the paths we are interested in    
        if var in var_to_elem:
            files[(from_year, to_year)][var_to_elem[var]] = path + "/" + file 
        else:
            continue

    ensmem = ensmem_set.pop()

    def vaporpress(Tmean, RH):
        #Tmean °C
        #RH %
        eos = 6.11 # hPa
        Lv = 2.5e6 # J/kg
        To = 273.16 # K
        Rv = 461 # J/K/kg
        #eps = 0.622 # = (Mv/Md)

        #Saturation vapor pressure (es):
        es = eos * np.exp(Lv/Rv*(1/To - 1/(Tmean + To)))

        # Actual vapor pressure (e):
        e = es*RH/100.0 #hPa
        return e #hPa
        #return e/10.0 #kPa
        #return (es - e)/10.0 #kPa #VPD
        

    def write_files(cache):
        no_of_files = len(cache)
        count = 0
        for (y, x), rows in cache.items():
            path_to_outdir = config["path_to_scratch"] + "/row-" + str(y+1)
            if not os.path.isdir(path_to_outdir):
                os.makedirs(path_to_outdir)

            path_to_outfile = path_to_outdir + "/col-" + str(x+1) + ".csv.gz"
            if not os.path.isfile(path_to_outfile):
                with gzip.open(path_to_outfile, "wt") as _:
                    writer = csv.writer(_, delimiter=",")
                    writer.writerow(["iso-date", "year", "month", "day", "doy", "tmin", "tavg", "tmax", "precip", "relhumid", "globrad", "wind", "airpress", "specificHumidity", "snowfallFlux", "surfaceDownwellingLongwaveRadiation"])
                    writer.writerow(["[]", "[]", "[]", "[]", "[]", "[°C]", "[°C]", "[°C]", "[mm]", "[%]", "[MJ m-2]", "[m s-1]", "[hPa]", "[g kg-1]", "[mm]", "[MJ m-2]"])

            with gzip.open(path_to_outfile, "at") as _:
                writer = csv.writer(_, delimiter=",")
                for row in rows:
                    writer.writerow(row)

            count = count + 1
            if count % 50000 == 0:
                print(count, "/", no_of_files, "files written")
        print(no_of_files, "files written")


    write_files_threshold = int(config["write_files_threshold"]) #50 #ys

    for start_year, end_year in sorted(files.keys()):

        elem_to_file = files[(start_year, end_year)]

        if config["start_year"] and end_year < int(config["start_year"]):
            continue
        if config["end_year"] and int(config["end_year"]) < start_year:
            continue

        datasets = {}
        for elem, filepath in elem_to_file.items():
            print("opening", filepath)
            datasets[elem] = Dataset(filepath) 

        sum_days = 0
        for year in range(start_year, end_year + 1):

            clock_start_year = time.perf_counter()
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
                            secs_per_day = 60 * 60 * 24
                            MJ_to_J = 1.0E6
                            W_per_m2_per_s_to_MJ_per_m2_per_day = secs_per_day / MJ_to_J
                            #vp = vaporpress(tavg, rh)
                            row = [
                                (date(year, 1, 1) + timedelta(days=doy_i + i)).strftime("%Y-%m-%d"), # iso-date
                                str(year), # year
                                str((date(year, 1, 1) + timedelta(days=doy_i + i)).month), # month
                                str((date(year, 1, 1) + timedelta(days=doy_i + i)).day), # day
                                str(doy_i + i + 1), # doy
                                str(round(data["tmin"][i, y, x] - 273.15, 2)), # K -> [°C]
                                str(round(data["tavg"][i, y, x] - 273.15, 2)), # K -> [°C]
                                str(round(data["tmax"][i, y, x] - 273.15, 2)), # K -> [°C]
                                str(round(data["precip"][i, y, x] * secs_per_day, 2)), # kg m-2 -> [mm] = 100mm*100mm*100mm (1L=1kg) / 1000mm*1000mm (1m*1m) = 1
                                str(round(data["relhumid"][i, y, x], 2)), # [%]
                                str(round(data["globrad"][i, y, x] * W_per_m2_per_s_to_MJ_per_m2_per_day, 4)), # [MJ m-2] 1 W s = 1 J 
                                str(round(data["wind"][i, y, x], 2)), # [m s-1]
                                str(round(data["airpress"][i, y, x] / 100.0, 2)), # [hPa]
                                str(round(data["specificHumidity"][i, y, x] * 1000.0, 2)), #kg kg-1 -> [g kg-1]
                                str(round(data["snowfallFlux"][i, y, x] * secs_per_day, 2)), # [kg m-2] -> [mm] = 100mm*100mm*100mm (1L=1kg) / 1000mm*1000mm (1m*1m) = 1
                                str(round(data["surfaceDownwellingLongwaveRadiation"][i, y, x] * W_per_m2_per_s_to_MJ_per_m2_per_day, 4)), # [MJ m-2] 1 W s = 1 J
                                #str(round(vp, 2))
                            ]
                            cache[(y,x)].append(row)

                    print(y, end=" ", flush=True) 

                    if y > int(config["start_y"]) and (y - int(config["start_y"])) % write_files_threshold == 0:
                        print()
                        s = time.perf_counter()
                        write_files(cache)
                        cache = defaultdict(list)
                        e = time.perf_counter()
                        print("wrote", write_files_threshold, "ys in", (e-s), "seconds")

                print()

                #write remaining cache items
                write_files(cache)
                cache = defaultdict(list)

                clock_end_year = time.perf_counter()
                print("running year", year, "(doy currently:", doy_i, ") took", (clock_end_year - clock_start_year), "seconds so far")

            sum_days = sum_days + days_in_year

        for _ in datasets.values():
            _.close()


    # copy files from scratch to final output
    copy_to_path = config["path_to_output"] + config["gcm"] + "/" + config["scen"] + "/" + str(ensmem) + "/"
    print("copying files from", config["path_to_scratch"], "to", copy_to_path)
    shutil.copytree(config["path_to_scratch"], copy_to_path, dirs_exist_ok=True)
    print("done copying")
    print("deleting scratch files from", config["path_to_scratch"])
    shutil.rmtree(config["path_to_scratch"], ignore_errors=True)
    print("done deleting scratch files")


if __name__ == "__main__":
    main()