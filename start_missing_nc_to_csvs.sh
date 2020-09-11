#!/bin/sh

#ssp585
#sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 ssp585 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/ssp585 1 360

#picontrol row 1-90
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 1 90

#picontrol row 91-180
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 91 180

#picontrol row 181-270
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 181 270

#picontrol row 271-360
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 271 360