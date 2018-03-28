#!/bin/bash

##  Generate INP File

hkl_list=(1 1 0)
uvw_list=(1 -1 0)

sed -i '' "s/hkl =.*/hkl = np.asarray([ ${hkl_list[0]}, ${hkl_list[1]}, ${hkl_list[2]}])/" Input_Computation.py
sed -i '' "s/uvw =.*/uvw = np.asarray([ ${uvw_list[0]}, ${uvw_list[1]}, ${uvw_list[2]}])/" Input_Computation.py

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

sed -i '' "s/rotation.*/rotation ${Vectors}/" material_model.zmat

abaqus_6.11-2 cae noGUI=Main.py

find . -name '*.inp' -cmin -1 > JobName

sed '' 's/material=Elastic-Plastic/material_model_Elastic_Plastic.zmat/' ${JobName}

sed '' 's/material=Elastic/material_model_Elastic.zmat/' ${JobName}


#zmat JobName

