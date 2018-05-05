#!/bin/bash

hkl=(0 1 0)
uvw=(1 0 0)
mode_list=("I" "II" "III")
#slip_systems_list=("b4" "b2" "b5" "d4" "d1" "d6" "a2" "a6" "a3" "c5" "c3" "c1")
slip_systems_list=("b4" "b2")

PBS_file=Launch_Cluster_By_Slip_System.sh
for slip_suffix in ${slip_systems_list[@]}
do
	for mode in ${mode_list[@]}
	do
		PBS_file_New=Launch_Cluster_${slip_suffix}_${mode}
		cp ${PBS_file} ${PBS_file_New}
		### set hkl
		to_find=#hkl_value#
		replace_by=${hkl[@]}
		sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}
		### set uvw
		to_find=#uvw_value#
		replace_by=${uvw[@]}
		sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}
		### set slip system
		to_find=#slip_suffix_value#
		replace_by=${slip_suffix}
		sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}
		### set mode
		to_find=#mode_value#
		replace_by=${mode}
		sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}		
		### launch computation
		qsub ${PBS_file_New}
		#rm ${PBS_file_New}
	done
done

