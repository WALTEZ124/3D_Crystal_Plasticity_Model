# -*- coding: utf-8 -*-

from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbMaterial import *
from odbAccess import *
from textRepr import *
import pickle
import os
import shutil
from os.path import *
from time import *
from numpy import *
import numpy as np
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

#---------------------------------------------------------------------------------
#          Management of source and output folders 
#---------------------------------------------------------------------------------

#codeSrc = os.path.join('..','..','Code','Verify_material_orientation_Zmat_Abaqus')
codeSrc = '.'
odbDir = 'Results_Odb'
compSrc = os.path.join(codeSrc,'src_Computation')

execfile(os.path.join(codeSrc,'Input_Computation.py'))	
elastic = Elastic( eType = elasticity_type)
if elastic.eType =='isotropic' :
	suffix = 'isotropic'
elif elastic.eType =='orthotropic' :
	Shkl = "%d%d%d" % (elastic.hkl[0],elastic.hkl[1],elastic.hkl[2])
	Suvw = "%d%d%d" % (elastic.uvw[0],elastic.uvw[1],elastic.uvw[2])
	suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)


slip_suffix = 'b5'

odbSrc = os.path.join(odbDir , 'src_Odb_%s_octahedral' % (suffix ),'Yield_Surface',slip_suffix)
if not os.path.exists(odbSrc):
	os.makedirs(odbSrc)

#----------------------------------------------------------------------------------
# Create Model:
#----------------------------------------------------------------------------------

srcFile =os.path.join(compSrc,'Model_Circular_Partition.py')
execfile(srcFile)
#openmdb = openMdb(pathName='3D_Model.cae')
# Pour l'affichage des masques dans le fichier rpy
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)


# Prepare a restart computation:

mdb.Model(name='Model-1-Restart', objectToCopy=mdb.models['Model-1'])

mdb.models['Model-1'].steps['Step-2'].Restart(frequency=4, numberIntervals=0, overlay=ON, timeMarks=OFF)

mdb.models['Model-1'].steps['Step-3'].suppress()
mdb.models['Model-1-Restart'].steps['Step-3'].suppress()

#----------------------------------------------------------------------------------
# Job parameters :
#----------------------------------------------------------------------------------

n_tot_steps = 3

PL_Star_Job  = { 'n_tot_steps' : n_tot_steps, 'n_init_steps' : 2 , 
					'time_steps' : [ 10, 1 , 10 ] , 'max_num_inc': 1000, 
					'ini_inc' : dimensions.time_inc , 'min_inc' : 1e-6, 'max_inc' : 1 }


Job_Star = Container()
Job_Star.I_II   = Container()
Job_Star.I_III  = Container()
Job_Star.II_III = Container()

#----------------------------------------------------------------------------------
#          Determination of parameters relating loading to nominals SIF 
#----------------------------------------------------------------------------------


file2=open(os.path.join(compSrc, 'Parameters_F_To_K_nominals_%s.p' %  suffix ),'rb')
Param = pickle.load(file2)
file2.close()

elastic = Elastic( eType = elasticity_type)
plastic = Plastic( pType = 'none')

#:------------------------------------
# Set plastic computation
#:------------------------------------

# Test parameters:

KI_Center   = 30. 
KII_Center  = 12.
KIII_Center = 10.

stab_rad = 4.
KRadius  = 8.

#:--------------------
#     Plane I-II
#:--------------------

os.system('echo Write INP for plane I-II' )

init_prop_angle = np.arccos(KII_Center/sqrt(KI_Center**2+KII_Center**2) )

KI_max  = KI_Center  + stab_rad * np.sin( init_prop_angle) 
KII_max = KII_Center + stab_rad * np.cos( init_prop_angle) 

KI_init_range   = [ KI_max , KI_Center ]
KII_init_range  = [ KII_max , KII_Center ]
KIII_init_range = [ 0. , 0. ]

PL_Init_Test_I_II = { 'name' : 'EP', 'test_type' : 'Star', 'loading_type' : loading_type, 
					'KI_init_range' : KI_init_range ,'KII_init_range' : KII_init_range, 
					'KIII_init_range' : KIII_init_range, 'NLGEOM': False }

# Write inp files

#Init_JobName_I_II, Init_Description_I_II     = Create_INP_Initial_Loading(mdb, 'Model-1' , PL_Init_Test_I_II , PL_Star_Job, Param, elastic)

Init_JobName, Init_Description_I_II = generate_init_job_name(PL_Init_Test_I_II, suffix)

Init_JobName_I_II = '%s_%s' %(Init_JobName, slip_suffix)

Job_Star.I_II.Init_JobName     = Init_JobName_I_II
Job_Star.I_II.Init_Description = Init_Description_I_II
Job_Star.I_II.KI_init_range   = KI_init_range
Job_Star.I_II.KII_init_range  = KII_init_range
Job_Star.I_II.KIII_init_range = KIII_init_range


file2=open('Star_job_details_I_II.txt','w') 
file2.write('%s\n' % Init_JobName_I_II ) 

n_exp_dir = 8
Explored_Directions = [ n*360./n_exp_dir for n in range(n_exp_dir) ]

Sec_JobNames_list = []
KI_sec_range   = []
KII_sec_range  = []
KIII_sec_range = []

for sec_prop_angle in Explored_Directions :
	KI_sec   =  KI_Center  + KRadius*np.sin( sec_prop_angle*np.pi/180 ) 
	KII_sec  =  KII_Center + KRadius*np.cos( sec_prop_angle*np.pi/180 ) 
	KIII_sec =  0.
	PL_Sec_Test_I_II = { 'name' : 'EP', 'test_type' : 'Star', 'loading_type' : loading_type, 
				'KI_sec' : KI_sec , 'KII_sec' : KII_sec, 'KIII_sec' : KIII_sec, 'NLGEOM': False }
	Sec_JobName_I_II, Sec_Description_I_II = Create_INP_Sec_Loading( mdb, 'Model-1-Restart', Init_JobName_I_II , PL_Sec_Test_I_II, PL_Star_Job, Param, elastic)
	file2.write('%s\n' % Sec_JobName_I_II ) 
	Sec_JobNames_list += [Sec_JobName_I_II]
	KI_sec_range   += [KI_sec]
	KII_sec_range  += [KII_sec]
	KIII_sec_range += [KIII_sec]

file2.close()

Job_Star.I_II.Sec_JobNames_list = Sec_JobNames_list
Job_Star.I_II.KI_sec_range   = KI_sec_range
Job_Star.I_II.KII_sec_range  = KII_sec_range
Job_Star.I_II.KIII_sec_range = KIII_sec_range

#:--------------------
#     Plane I-III
#:--------------------

os.system('echo Write INP for plane I-III' )

init_prop_angle = np.arccos(KIII_Center/sqrt(KI_Center**2+KIII_Center**2) )

KI_max   = KI_Center  + stab_rad * np.sin( init_prop_angle) 
KIII_max = KIII_Center + stab_rad *np.cos( init_prop_angle) 

KI_init_range   = [ KI_max , KI_Center ]
KII_init_range  = [ 0 , 0 ]
KIII_init_range = [ KIII_max , KIII_Center ]

PL_Init_Test_I_III = { 'name' : 'EP', 'test_type' : 'Star', 'loading_type' : loading_type, 
					'KI_init_range' : KI_init_range ,'KII_init_range' : KII_init_range, 
					'KIII_init_range' : KIII_init_range, 'NLGEOM': False }

# Write inp files

#Init_JobName_I_III, Init_Description_I_III   = Create_INP_Initial_Loading(mdb, 'Model-1' , PL_Init_Test_I_III  , PL_Star_Job, Param, elastic)

Init_JobName, Init_Description_I_III = generate_init_job_name(PL_Init_Test_I_III, suffix)

Init_JobName_I_III = '%s_%s' %(Init_JobName, slip_suffix)

Job_Star.I_III.Init_JobName     = Init_JobName_I_III
Job_Star.I_III.Init_Description = Init_Description_I_III
Job_Star.I_III.KI_init_range   = KI_init_range
Job_Star.I_III.KII_init_range  = KII_init_range
Job_Star.I_III.KIII_init_range = KIII_init_range

file2=open('Star_job_details_I_III.txt','w') 
file2.write('%s\n' % Init_JobName_I_III ) 

n_exp_dir = 8
Explored_Directions = [ n*360./n_exp_dir for n in range(n_exp_dir) ]

Sec_JobNames_list = []
KI_sec_range   = []
KII_sec_range  = []
KIII_sec_range = []

for sec_prop_angle in Explored_Directions :
	KI_sec   =  KI_Center  + KRadius * np.sin( sec_prop_angle*np.pi/180 ) 
	KII_sec  =  0. 
	KIII_sec =  KIII_Center + KRadius * np.cos( sec_prop_angle*np.pi/180 ) 
	PL_Sec_Test_I_III = { 'name' : 'EP', 'test_type' : 'Star', 'loading_type' : loading_type, 
				'KI_sec' : KI_sec , 'KII_sec' : KII_sec, 'KIII_sec' : KIII_sec, 'NLGEOM': False }
	Sec_JobName_I_III, Sec_Description_I_III = Create_INP_Sec_Loading( mdb, 'Model-1-Restart', Init_JobName_I_III , PL_Sec_Test_I_III, PL_Star_Job, Param, elastic)
	file2.write('%s\n' % Sec_JobName_I_III ) 
	Sec_JobNames_list += [Sec_JobName_I_III]
	KI_sec_range   += [KI_sec]
	KII_sec_range  += [KII_sec]
	KIII_sec_range += [KIII_sec]

file2.close()

Job_Star.I_III.Sec_JobNames_list = Sec_JobNames_list
Job_Star.I_III.KI_sec_range   = KI_sec_range
Job_Star.I_III.KII_sec_range  = KII_sec_range
Job_Star.I_III.KIII_sec_range = KIII_sec_range

#:--------------------
#     Plane II-III
#:--------------------

os.system('echo Write INP for plane II-III' )

init_prop_angle = np.arccos(KIII_Center/sqrt(KII_Center**2+KIII_Center**2) )

KII_max  = KII_Center  + stab_rad * np.sin( init_prop_angle) 
KIII_max = KIII_Center + stab_rad * np.cos( init_prop_angle) 

KI_init_range   = [ 0.5 , 0.5 ]
KII_init_range  = [ KII_max , KII_Center ]
KIII_init_range = [ KIII_max , KIII_Center ]

PL_Init_Test_II_III = { 'name' : 'EP', 'test_type' : 'Star', 'loading_type' : loading_type, 
					'KI_init_range' : KI_init_range ,'KII_init_range' : KII_init_range, 
					'KIII_init_range' : KIII_init_range, 'NLGEOM': False }

# Write inp files

#Init_JobName_II_III, Init_Description_II_III = Create_INP_Initial_Loading(mdb, 'Model-1' , PL_Init_Test_II_III , PL_Star_Job, Param, elastic)

Init_JobName, Init_Description_II_III = generate_init_job_name(PL_Init_Test_II_III, suffix)

Init_JobName_II_III = '%s_%s' %(Init_JobName, slip_suffix)

Job_Star.II_III.Init_JobName     = Init_JobName_II_III
Job_Star.II_III.Init_Description = Init_Description_II_III
Job_Star.II_III.KI_init_range   = KI_init_range
Job_Star.II_III.KII_init_range  = KII_init_range
Job_Star.II_III.KIII_init_range = KIII_init_range

file2=open('Star_job_details_II_III.txt','w') 
file2.write('%s\n' % Init_JobName_II_III ) 

n_exp_dir = 8
Explored_Directions = [ n*360./n_exp_dir for n in range(n_exp_dir) ]

Sec_JobNames_list = []
KI_sec_range   = []
KII_sec_range  = []
KIII_sec_range = []

for sec_prop_angle in Explored_Directions :
	KI_sec   =  0.5
	KII_sec  =  KII_Center  + KRadius * np.sin( sec_prop_angle*np.pi/180 ) 
	KIII_sec =  KIII_Center + KRadius * np.cos( sec_prop_angle*np.pi/180 ) 
	PL_Sec_Test_II_III = { 'name' : 'EP', 'test_type' : 'Star', 'loading_type' : loading_type, 
				'KI_sec' : KI_sec , 'KII_sec' : KII_sec, 'KIII_sec' : KIII_sec, 'NLGEOM': False }
	Sec_JobName_II_III, Sec_Description_II_III = Create_INP_Sec_Loading( mdb, 'Model-1-Restart', Init_JobName_I_III , PL_Sec_Test_II_III, PL_Star_Job, Param, elastic)
	file2.write('%s\n' % Sec_JobName_II_III ) 
	Sec_JobNames_list += [Sec_JobName_II_III]
	KI_sec_range   += [KI_sec]
	KII_sec_range  += [KII_sec]
	KIII_sec_range += [KIII_sec]

file2.close()

Job_Star.II_III.Sec_JobNames_list = Sec_JobNames_list
Job_Star.II_III.KI_sec_range   = KI_sec_range
Job_Star.II_III.KII_sec_range  = KII_sec_range
Job_Star.II_III.KIII_sec_range = KIII_sec_range


file2=open(os.path.join( odbSrc,'Star_Job_Parameters_%s.p' %  suffix),'wb')
pickle.dump(Job_Star, file2)
file2.close()

