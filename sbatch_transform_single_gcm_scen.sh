#!/bin/bash -x
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --job-name=transform_daily_agmip_phase3_netcdf_to_csv
#SBATCH --time=7-00:00:00

GCM=$1
SCEN=$2
SCRATCH=$3
OUT=$4
START_ROW=$5
END_ROW=$6

PYTHON=~/.conda/envs/nc_to_csv/bin/python

$PYTHON transform_daily_agmip_phase3_netcdf_to_csv.py path_to_scratch=$SCRATCH path_to_output=$OUT gcm=$GCM scen=$SCEN start_y=$START_ROW end_y=$END_ROW

