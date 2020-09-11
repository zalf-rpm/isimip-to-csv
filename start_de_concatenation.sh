#!/bin/sh

#ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/rpm/projects/R/stella/copy_climate_subset GFDL-ESM4 ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/rpm/projects/R/stella/copy_climate_subset IPSL-CM6A-LR ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/rpm/projects/R/stella/copy_climate_subset MPI-ESM1-2-HR ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/rpm/projects/R/stella/copy_climate_subset MRI-ESM2-0 ssp126
sbatch sbatch_concatenate_single_gcm_ssp.sh /beegfs/rpm/projects/R/stella/copy_climate_subset UKESM1-0-LL ssp126
