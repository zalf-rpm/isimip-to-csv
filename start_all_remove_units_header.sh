#!/bin/sh

#picontrol
sbatch sbatch_remove_single_units_header_picontrol.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs GFDL-ESM4 picontrol
sbatch sbatch_remove_single_units_header_picontrol.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs IPSL-CM6A-LR picontrol
sbatch sbatch_remove_single_units_header_picontrol.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs MPI-ESM1-2-HR picontrol
sbatch sbatch_remove_single_units_header_picontrol.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs MRI-ESM2-0 picontrol
