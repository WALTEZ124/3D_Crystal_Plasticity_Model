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

odbSrc = os.path.join(odbDir ,loading_type, 'src_Odb_%s_%d_%d_%d' % (suffix, R0, C1, Gamma1 ),'Loading_Range')

odbSrcEL = os.path.join( odbSrc, 'Elastic')
#if not os.path.exists(odbSrcEL):
#	os.makedirs(odbSrcEL)

odbSrcLGEOM = os.path.join( odbSrc, 'LGEOM')
#if not os.path.exists(odbSrcLGEOM):
#	os.makedirs(odbSrcLGEOM)


srcFile =os.path.join(compSrc,'Model_Circular_Partition.py')
execfile(srcFile)
#openmdb = openMdb(pathName='3D_Model.cae')

# Pour l'affichage des masques dans le fichier rpy
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

#----------------------------------------------------------------------------------
# Job parameters :
#----------------------------------------------------------------------------------

n_tot_steps = 3

EL_Job      = { 'n_tot_steps' : n_tot_steps, 'n_act_steps' : 1 , 'time_steps' : [  1 ] ,
				'max_num_inc': 100, 'ini_inc' : 1.0 , 'min_inc' : 1e-3, 'max_inc' : 1 }

PL_Mon_Job  = { 'n_tot_steps' : n_tot_steps, 'n_act_steps' : 2 , 'time_steps' : [ 10, 10 ],
				 'max_num_inc': 700, 'ini_inc' : dimensions.time_inc ,
				 'min_inc' : 1e-6, 'max_inc' : 1  }


#----------------------------------------------------------------------------------
#          Determination of parameters relating loading to nominals SIF 
#----------------------------------------------------------------------------------


file2=open(os.path.join(compSrc, 'Parameters_F_To_K_nominals_%s.p' %  suffix ),'rb')
Param = pickle.load(file2)
file2.close()

elastic = Elastic( eType = elasticity_type)
plastic = Plastic( pType = 'none')

# Mode I

#ELTest_I 	= { 'name' : 'EL_Norm', 'loading_type' : loading_type, 'KI_range' : [1.], 
#				'KII_range' : [0.], 'KIII_range' : [0.], 'NLGEOM': False }

#EL_Norm_JobName_I = Compute(mdb, ELTest_I, EL_Job, Param, elastic, odbSrcEL)



# Test parameters:

KI_range_I   = [ 40., 0.1]
KII_range_I  = [  0.,  0.]
KIII_range_I = [  0.,  0.]

PLTest_I 	 = { 'name' : 'EP', 'test_type' : 'Mon', 'NLGEOM': False ,
				'loading_type' : loading_type, 'KI_range' : KI_range_I , 
				'KII_range' : KII_range_I, 'KIII_range' : KIII_range_I }


Mon_PL_JobName_I   = Compute(mdb, PLTest_I  , PL_Mon_Job, Param, elastic, odbSrcLGEOM)

#Mon_PL_JobName_I   , EPJob_Descrip_I   = Generate_names(PLTest_I  , elastic, odbSrcLGEOM )


file2=open('last_job_file.txt','w') 
file2.write('%s\n' % Mon_PL_JobName_I) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

