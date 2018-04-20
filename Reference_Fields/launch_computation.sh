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
def miller_to_euler(hkl, uvw):	
	qrs = np.cross(hkl, uvw) ;
	Nhkl = np.linalg.norm(hkl) ;
	Nuvw = np.linalg.norm(uvw) ;
	Nqrs = np.linalg.norm(qrs) ;
	g = np.array([[ uvw[0]/Nuvw,  qrs[0]/Nqrs, hkl[0]/Nhkl ],
	                [ uvw[1]/Nuvw, qrs[1]/Nqrs, hkl[1]/Nhkl ],
	                [ uvw[2]/Nuvw, qrs[2]/Nqrs, hkl[2]/Nhkl] ])     ;       
	R = np.array([[1,0,0],[0,0,-1],[0,1,0]]);
        g_prime = np.matmul(g, R )
	if abs(g_prime[2][2]-1)<1e-6 :
	        phi1 = np.arctan(g_prime[0][1]/g_prime[0][0])*180/np.pi ;
	        psi  = 0.;
	        phi2 = 0.;
	else :
	        phi1 = np.arctan(-g_prime[2][0]/g_prime[2][1])*180/np.pi;
	        psi  = np.arccos(g_prime[2][2])*180/np.pi;
	        phi2 = np.arctan(g_prime[0][2]/g_prime[1][2])*180/np.pi;
	print('%f %f %f' % (phi1, psi, phi2));

def miller_to_euler_1(hkl, uvw):	
	h,k,l = hkl;
	u, v, w = uvw;
	Nhkl = np.linalg.norm(hkl) ;
	Nuvw = np.linalg.norm(uvw) ;
	psi = np.arccos(l/Nhkl)*180/np.pi;
	phi2 = np.arccos(k/np.sqrt(h**2+k**2))*180/np.pi;
	phi1 = np.arcsin(w*Nhkl/(Nuvw*np.sqrt(h**2+k**2)))*180/np.pi;
	print('%f %f %f' % (phi1, psi, phi2));

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

## Up-date the material orientation in the Zmat file
sed -i -e "s/rotation.*/rotation ${Vectors}/" material_model_elastic.zmat
sed -i -e "s/rotation.*/rotation ${Vectors}/" material_model_elastic_plastic.zmat

Zpreload material_model_elastic.zmat > Zpreload_material_model_elastic.txt
Zpreload material_model_elastic_plastic.zmat > Zpreload_material_model_elastic_plastic.txt

## Generate INP File
abaqus_6.11-2 cae noGUI=Create_INP_file.py

## Import JobName and sources' path from previous computation
JobName=$(sed -n 1p last_job_file.txt).inp
OdbSrc=$(sed -n 2p last_job_file.txt)
OdbSrcEL=$(sed -n 3p last_job_file.txt)
OdbSrcLGEOM=$(sed -n 4p last_job_file.txt)

## Insert the Zmat material configuration in the inp file
sed -i -e 's/material=Elastic-Plastic\s*$/material=material_model_elastic_plastic.zmat/' $JobName
sed -i -e 's/material=Elastic\s*$/material=material_model_elastic.zmat/' $JobName

#sed -i -e 's/material=Elastic-Rigid\s*$/material=material_model_elastic.zmat/' "${JobName}.inp"

grep -A 4 '*MATERIAL,NAME' Zpreload_material_model_elastic.txt > material_def_inp.inp
grep -A 4 '*MATERIAL,NAME' Zpreload_material_model_elastic_plastic.txt >> material_def_inp.inp

materials_location=`grep -n '** MATERIALS' $JobName | awk -F ":" '{print $1}'`

insertion_line=$(($materials_location+2))

sed -i "${insertion_line}i **here" $JobName

begin="**here"
end="*Material, name=Elastic-Rigid"

sed -i -e "/$begin/,/$end/{/$begin/{p; r material_def_inp.inp
	}; /$end/p; d}" $JobName
sed -i '/**here/d' $JobName

## Launch Job on Zmat

# To configurate Zebulon with abaqus_6.11-2
#source ~zebulon/Z8.7/do_config.sh 

Zmat cpus=12 memory=16gb $JobName




