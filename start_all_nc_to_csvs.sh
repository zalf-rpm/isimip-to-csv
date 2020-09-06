#!/bin/sh

#historical
sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 historical /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/historical 1 360
sbatch sbatch_transform_single_gcm_scen.sh IPSL-CM6A-LR historical /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/IPSL-CM6A-LR/historical 1 360
sbatch sbatch_transform_single_gcm_scen.sh MPI-ESM1-2-HR historical /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MPI-ESM1-2-HR/historical 1 360
sbatch sbatch_transform_single_gcm_scen.sh MRI-ESM2-0 historical /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MRI-ESM2-0/historical 1 360
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL historical /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/historical 1 360

#ssp126
sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 ssp126 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/ssp126 1 360
sbatch sbatch_transform_single_gcm_scen.sh IPSL-CM6A-LR ssp126 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/IPSL-CM6A-LR/ssp126 1 360
sbatch sbatch_transform_single_gcm_scen.sh MPI-ESM1-2-HR ssp126 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MPI-ESM1-2-HR/ssp126 1 360
sbatch sbatch_transform_single_gcm_scen.sh MRI-ESM2-0 ssp126 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MRI-ESM2-0/ssp126 1 360
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL ssp126 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/ssp126 1 360

#ssp585
sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 ssp585 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/ssp585 1 360
sbatch sbatch_transform_single_gcm_scen.sh IPSL-CM6A-LR ssp585 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/IPSL-CM6A-LR/ssp585 1 360
sbatch sbatch_transform_single_gcm_scen.sh MPI-ESM1-2-HR ssp585 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MPI-ESM1-2-HR/ssp585 1 360
sbatch sbatch_transform_single_gcm_scen.sh MRI-ESM2-0 ssp585 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MRI-ESM2-0/ssp585 1 360
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL ssp585 /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/ssp585 1 360

#picontrol row 1-90
sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/picontrol 1 90
sbatch sbatch_transform_single_gcm_scen.sh IPSL-CM6A-LR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/IPSL-CM6A-LR/picontrol 1 90
sbatch sbatch_transform_single_gcm_scen.sh MPI-ESM1-2-HR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MPI-ESM1-2-HR/picontrol 1 90
sbatch sbatch_transform_single_gcm_scen.sh MRI-ESM2-0 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MRI-ESM2-0/picontrol 1 90
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 1 90

#picontrol row 91-180
sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/picontrol 91 180
sbatch sbatch_transform_single_gcm_scen.sh IPSL-CM6A-LR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/IPSL-CM6A-LR/picontrol 91 180
sbatch sbatch_transform_single_gcm_scen.sh MPI-ESM1-2-HR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MPI-ESM1-2-HR/picontrol 91 180
sbatch sbatch_transform_single_gcm_scen.sh MRI-ESM2-0 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MRI-ESM2-0/picontrol 91 180
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 91 180

#picontrol row 181-270
sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/picontrol 181 270
sbatch sbatch_transform_single_gcm_scen.sh IPSL-CM6A-LR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/IPSL-CM6A-LR/picontrol 181 270
sbatch sbatch_transform_single_gcm_scen.sh MPI-ESM1-2-HR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MPI-ESM1-2-HR/picontrol 181 270
sbatch sbatch_transform_single_gcm_scen.sh MRI-ESM2-0 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MRI-ESM2-0/picontrol 181 270
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 181 270

#picontrol row 271-360
sbatch sbatch_transform_single_gcm_scen.sh GFDL-ESM4 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/GFDL-ESM4/picontrol 271 360
sbatch sbatch_transform_single_gcm_scen.sh IPSL-CM6A-LR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/IPSL-CM6A-LR/picontrol 271 360
sbatch sbatch_transform_single_gcm_scen.sh MPI-ESM1-2-HR picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MPI-ESM1-2-HR/picontrol 271 360
sbatch sbatch_transform_single_gcm_scen.sh MRI-ESM2-0 picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/MRI-ESM2-0/picontrol 271 360
sbatch sbatch_transform_single_gcm_scen.sh UKESM1-0-LL picontrol /scratch/csvs /beegfs/common/data/climate/isimip/AgMIP.input_csvs/UKESM1-0-LL/picontrol 271 360
