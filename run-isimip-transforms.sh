#!/bin/bash

python=~/.conda/envs/py38/bin/python

region=earth #nigeria

for model in "gfdl-esm2m" "hadgem2-es" "ipsl-cm5a-lr" "miroc-esm-chem" "noresm1-m"
do
	for rcp in "hist" "rcp2p6" "rcp4p5" "rcp6p0" "rcp8p5"
	do
		echo $region $model $rcp
		srun -l --job-name=${model:0:3}_${rcp:2:2}_${region:0:2} $python transform-daily-netcdf-to-csv.py path_to_output=csvs/ model=$model rcp=$rcp region=$region > ${region}_${model}_${rcp} 2> e_${region}_${model}_${rcp} &
	done
done
