#!/bin/bash

## Input material orientation
hkl_list=(1 1 0)
uvw_list=(1 -1 0)

## Modify the Input File (for file names)
sed -i '' "s/hkl =.*/hkl = np.asarray([ ${hkl_list[0]}, ${hkl_list[1]}, ${hkl_list[2]}])/" Input_Computation.py
sed -i '' "s/uvw =.*/uvw = np.asarray([ ${uvw_list[0]}, ${uvw_list[1]}, ${uvw_list[2]}])/" Input_Computation.py

## Transformation from Miller Indices to Zmat orientation
Vectors=$(python <<< "
import numpy as np ;
hkl = np.asarray([ ${hkl_list[0]}, ${hkl_list[1]}, ${hkl_list[2]}]); 
uvw = np.asarray([ ${uvw_list[0]}, ${uvw_list[1]}, ${uvw_list[2]}]);
qrs = np.cross(hkl, uvw) ;
Nhkl = np.linalg.norm(hkl) ;
Nuvw = np.linalg.norm(uvw) ;
Nqrs = np.linalg.norm(qrs) ;
g_prime_transpose = np.array([[ uvw[0]/Nuvw,  uvw[1]/Nuvw, uvw[2]/Nuvw ],
								[ hkl[0]/Nhkl,  hkl[1]/Nhkl, hkl[2]/Nhkl ],
								[-qrs[0]/Nqrs, -qrs[1]/Nqrs, -qrs[2]/Nqrs] ]) 	;	
NormalAxis  = np.dot( g_prime_transpose, np.array([1,0,0]) )	;					
PrimaryAxis = np.dot( g_prime_transpose, np.array([0,1,0]) )	;
t3 = np.cross(NormalAxis, PrimaryAxis) ;
print( NormalAxis, PrimaryAxis, t3) ;" )

echo ${Vectors}

## Up-date the material orientation in the Zmat file
sed -i '' "s/rotation.*/rotation ${Vectors}/" material_model.zmat

## Generate INP File
abaqus_6.11-2 cae noGUI=Create_INP_file.py

## Import JobName and sources' path from previous computation
JobName=$(sed -n 1p last_job_file.txt)
OdbSrc=$(sed -n 2p last_job_file.txt)
OdbSrcEL=$(sed -n 3p last_job_file.txt)
OdbSrcLGEOM=$(sed -n 4p last_job_file.txt)

#find . -name '*.inp' -cmin -1 > JobName

## Insert the Zmat material configuration in the inp file
sed '' 's/material=Elastic-Plastic/material_model_Elastic_Plastic.zmat/' ${JobName}.inp
sed '' 's/material=Elastic/material_model_Elastic.zmat/' ${JobName}.inp

## Launch Job on Zmat
#zmat ${JobName}.inp

## Move files
#mv ${JobName}.* ${OdbSrcEL}

