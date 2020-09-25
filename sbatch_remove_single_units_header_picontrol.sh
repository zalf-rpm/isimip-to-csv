#!/bin/bash -x
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=compute
#SBATCH --job-name=concatenate_climate_files
#SBATCH --time=7-00:00:00

BASE_PATH=$1
GCM=$2
SCEN=$3

PYTHON=~/.conda/envs/nc_to_csv/bin/python

$PYTHON remove_units_header.py base_path=$BASE_PATH gcm=$GCM scen=$SCEN

