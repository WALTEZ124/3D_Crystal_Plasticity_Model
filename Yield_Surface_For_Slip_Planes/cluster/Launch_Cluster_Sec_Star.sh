#!/bin/bash

hkl=(0 1 0)
uvw=(1 0 0)

suffix=${hkl[0]}${hkl[1]}${hkl[2]}_${uvw[0]}${uvw[1]}${uvw[2]}

#slip_systems_list=("b4" "b2" "b5" "d4" "d1" "d6" "a2" "a6" "a3" "c5" "c3" "c1")
slip_systems_list=("b5")

modes_plane_list=("I_II")

PBS_file=Yield_Surface_Sec_Star.sh
for slip_suffix in ${slip_systems_list[@]}
do
	for modes_plane in ${modes_plane_list[@]}
	do
		inp_folder=inp_files_${suffix}
		in_folder=/u/tezeghdanti/3D_Model_Crystal_Plasticity/Yield_Surface_For_Slip_Planes/${inp_folder}/${slip_suffix}
		job_file_name=${in_folder}/Star_job_details_${modes_plane}.txt
		# Read job details file
		nbr_lines=$(wc -l < ${job_file_name})
		InitJobName=$(sed -n 1p ${job_file_name})
		echo ${InitJobName}
		for ((j=2;j<=${nbr_lines};j++))
		do
			JobName=$(sed -n ${j}p ${job_file_name})
			SecJobName="${JobName}_${slip_suffix}.inp"
			echo ${SecJobName}
			PBS_file_New=Yield_Surface_Sec_Star_${slip_suffix}_${modes_plane}_${j}
			cp ${PBS_file} ${PBS_file_New}
			### set suffix
			to_find=#suffix_value#
			replace_by=${suffix}
			sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}
			### set slip system
			to_find=#slip_suffix_value#
			replace_by=${slip_suffix}
			sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}
			### set modes plane
			to_find=#modes_plane_value#
			replace_by=${modes_plane}
			sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}		
			### set Initial Job Name
			to_find=#InitJobName_value#
			replace_by=${InitJobName}
			sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}		
			### set Initial Job Name
			to_find=#SecJobName_value#
			replace_by=${SecJobName}
			sed -i -e "s/${to_find}/${replace_by}/g" ${PBS_file_New}	
			### launch computation
			qsub ${PBS_file_New}
		done
	done
done

