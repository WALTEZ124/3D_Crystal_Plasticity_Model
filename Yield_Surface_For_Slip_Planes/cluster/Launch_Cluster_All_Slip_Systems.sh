#!/bin/bash

hkl=(0 1 0)
uvw=(1 0 0)
modes_plane_list=("I_II" "I_III" "II_III")

#slip_systems_list=("b4" "b2" "b5" "d4" "d1" "d6" "a2" "a6" "a3" "c5" "c3" "c1")
slip_systems_list=("a3" "c5")

PBS_file=Yield_Surface_Init_Star.sh
for slip_suffix in ${slip_systems_list[@]}
do
	for modes_plane in ${modes_plane_list[@]}
	do
		PBS_file_New=Yield_Surface_Init_Star_${slip_suffix}_${modes_plane}
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
		### set modes plane
		to_find=#modes_plane_value#
		replace_by=${modes_plane}
		sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}		
		### launch computation
		qsub ${PBS_file_New}
	done
done

