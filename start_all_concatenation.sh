#!/bin/sh

#ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs GFDL-ESM4 ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs IPSL-CM6A-LR ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs MPI-ESM1-2-HR ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs MRI-ESM2-0 ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs UKESM1-0-LL ssp126

#ssp585
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs GFDL-ESM4 ssp585
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs IPSL-CM6A-LR ssp585
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs MPI-ESM1-2-HR ssp585
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs MRI-ESM2-0 ssp585
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/common/data/climate/isimip/AgMIP.input_csvs UKESM1-0-LL ssp585
