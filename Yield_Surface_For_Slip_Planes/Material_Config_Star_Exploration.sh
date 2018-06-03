#!/bin/bash

## Input material orientation
hkl_list=(0 1 0)
uvw_list=(1 0 0)

## Modify the Input File (for file names)
sed -i -e "s/	hkl =.*/	hkl = np.asarray([ ${hkl_list[0]}, ${hkl_list[1]}, ${hkl_list[2]}])/" Input_Computation.py
sed -i -e "s/	uvw =.*/	uvw = np.asarray([ ${uvw_list[0]}, ${uvw_list[1]}, ${uvw_list[2]}])/" Input_Computation.py

# Transformation from Miller Indices to Zmat orientation
Vectors=$(python <<< "
import numpy as np ;
hkl = [ ${hkl_list[0]}, ${hkl_list[1]}, ${hkl_list[2]}]; 
uvw = [ ${uvw_list[0]}, ${uvw_list[1]}, ${uvw_list[2]}];
hkl = np.asarray(hkl); 
uvw = np.asarray(uvw);

def miller_to_matrix(hkl, uvw):
	qrs = np.cross(hkl, uvw) ;
	Nhkl = np.linalg.norm(hkl) ;
	Nuvw = np.linalg.norm(uvw) ;
	Nqrs = np.linalg.norm(qrs) ;
	g = np.array([[ uvw[0]/Nuvw,  qrs[0]/Nqrs, hkl[0]/Nhkl ],
			[ uvw[1]/Nuvw, qrs[1]/Nqrs, hkl[1]/Nhkl ],
			[ uvw[2]/Nuvw, qrs[2]/Nqrs, hkl[2]/Nhkl] ]) 	;
	R = np.array([[1,0,0],[0,0,-1],[0,1,0]]);
	g_prime = np.matmul(g, R )
	X1 = np.dot( g_prime, np.array([1,0,0]) )	;					
	X2 = np.dot( g_prime, np.array([0,1,0]) )	;
	X1_txt = '%f %f %f' % (X1[0],X1[1],X1[2]) ;
	X2_txt = '%f %f %f' % (X2[0],X2[1],X2[2]) ;
	print( 'x1 %s x2 %s' %(X1_txt, X2_txt) ) ;

miller_to_matrix(hkl, uvw)" )

echo "${Vectors}"

used_material='am1_20'
inp_folder="inp_files_${hkl_list[0]}${hkl_list[1]}${hkl_list[2]}_${uvw_list[0]}${uvw_list[1]}${uvw_list[2]}"



## Up-date the material orientation in the Zmat file

material_file_elastic="material_model_elastic_${used_material}.zmat"
sed -i -e "s/rotation.*/rotation ${Vectors}/" ${material_file_elastic}
Zpreload ${material_file_elastic} > "Zpreload_material_model_elastic_${used_material}.txt"

slip_systems_list=("(1. 1. 1.) (-1. 0. 1.)" "(1. 1. 1.) (0. -1. 1.)" "(1. 1. 1.) (-1. 1. 0.)" "(1. -1. 1.) (-1. 0. 1.)" "(1. -1. 1.) (0. 1. 1.)" "(1. -1. 1.) (1. 1. 0.)" "(-1. 1. 1.) (0. -1. 1.)" "(-1. 1. 1.) (1. 1. 0.)" "(-1. 1. 1.) (1. 0. 1.)" "(1. 1. -1.) (-1. 1. 0.)" "(1. 1. -1.) (1. 0. 1.)" "(1. 1. -1.) (0. 1. 1.)")
slip_systems_suffix=("b4" "b2" "b5" "d4" "d1" "d6" "a2" "a6" "a3" "c5" "c3" "c1")

#slip_systems_list=("(1. 1. 1.) (0. -1. 1.)")
#slip_systems_suffix=("b2")

for (( i=0; i<${#slip_systems_list[@]}; i++ ))
do
	slip_system=${slip_systems_list[$i]}
	slip_suffix=${slip_systems_suffix[$i]}
	material_file_elastic_plastic="material_model_elastic_plastic_${used_material}_${slip_suffix}.zmat"
	cp "material_model_elastic_plastic_${used_material}.zmat" ${material_file_elastic_plastic}
	sed -i -e "s/**potential.*/**potential plane ${slip_system}/" ${material_file_elastic_plastic}
	Zpreload ${material_file_elastic_plastic} > "Zpreload_material_model_elastic_plastic_${used_material}_${slip_suffix}.txt"
	## Write INP files for elastic-plastic computation
	grep -A 4 '*MATERIAL,NAME' "Zpreload_material_model_elastic_${used_material}.txt" > material_def_inp.inp
	grep -A 4 '*MATERIAL,NAME' "Zpreload_material_model_elastic_plastic_${used_material}_${slip_suffix}.txt" >> material_def_inp.inp
	mkdir -p ${inp_folder}/${slip_suffix}/
	## Generate INP File
	sed -i -e "s/slip_suffix =.*/slip_suffix = '${slip_suffix}'/" Create_INP_file_Star_Exploration.py
	abaqus_6.11-2 cae noGUI=Create_INP_file_Star_Exploration.py
	## Import JobName and sources' path from previous computation
	for job_file_name in Star_job_details_I_II.txt Star_job_details_I_III.txt Star_job_details_II_III.txt
	do
		nbr_lines=$(wc -l < ${job_file_name})
		echo ${job_file_name}
		echo ${nbr_lines}
		for ((j=2;j<=${nbr_lines};j++))
		do
			JobName=$(sed -n ${j}p ${job_file_name})
			NewJobName="${JobName}_${slip_suffix}.inp"
			cp "${JobName}.inp" $NewJobName
			echo $NewJobName
			## Insert the Zmat material configuration in the inp file
			match='*Restart, read,'
			sed -i -e "/${match}/{ r material_def_inp.inp
					} " ${NewJobName}
			echo "Material defined and inserted into ${NewJobName}"
			## Launch Job on Zmat
			# To configurate Zebulon with abaqus_6.11-2
			#source ~zebulon/Z8.7/do_config.sh 
			#Zmat cpus=12 memory=16gb $NewJobName
			mv ${NewJobName} ${inp_folder}/${slip_suffix}/
			echo "file moved"
		done
	done
	mv "Zpreload_material_model_elastic_plastic_${used_material}_${slip_suffix}.txt" ${inp_folder}/${slip_suffix}/
	echo "Zpreload of ${slip_suffix} moved"
	mv ${material_file_elastic_plastic} ${inp_folder}/${slip_suffix}/
	cp Star_job_details* ${inp_folder}/${slip_suffix}/
	cp ${material_file_elastic} ${inp_folder}/${slip_suffix}/
done



