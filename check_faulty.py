#!/usr/bin/python
# -*- coding: UTF-8
import sys
import netCDF4
ds = netCDF4.Dataset(sys.argv[1])
ds.close()
sys.exit(0)
