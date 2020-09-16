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

    config = {
        "path_to_data": "/beegfs/common/data/climate/isimip/AgMIP.input/phase3/picontrol/UKESM1-0-LL",
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv
    print("config:", config)

    # sort files in dir
    path = config["path_to_data"]
    faulty = []
    for file in os.listdir(path):
        print(file)
        if file[-3:] != ".nc":
            continue
        try:
            ds = Dataset(path + "/" + file)
            ds.close()
        except:
            faulty.append(file)

    print("------------------------------")
    for file in faulty:
        print(file)


if __name__ == "__main__":
    main()