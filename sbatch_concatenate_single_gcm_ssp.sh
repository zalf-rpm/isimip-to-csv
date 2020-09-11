#!/bin/bash -x
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --job-name=concatenate_climate_files
#SBATCH --time=7-00:00:00

BASE_PATH=$1
GCM=$2
SSP=$3

PYTHON=~/.conda/envs/nc_to_csv/bin/python

$PYTHON concatenate_climate_files.py base_path=$BASE_PATH gcm=$GCM ssp=$SSP

