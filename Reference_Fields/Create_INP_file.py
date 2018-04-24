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

odbSrc = os.path.join(odbDir ,loading_type, 'src_Odb_%s_octahedral' % (suffix ),'Loading_Range')

odbSrcEL = os.path.join( odbSrc, 'Elastic')
if not os.path.exists(odbSrcEL):
	os.makedirs(odbSrcEL)

odbSrcLGEOM = os.path.join( odbSrc, 'LGEOM')
if not os.path.exists(odbSrcLGEOM):
	os.makedirs(odbSrcLGEOM)


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

PL_Mon_Job  = { 'n_tot_steps' : n_tot_steps, 'n_act_steps' : 1 , 'time_steps' : [ 10 ],
				 'max_num_inc': 1000, 'ini_inc' : dimensions.time_inc ,
				 'min_inc' : 1e-6, 'max_inc' : 1  }


#----------------------------------------------------------------------------------
#          Determination of parameters relating loading to nominals SIF 
#----------------------------------------------------------------------------------


file2=open(os.path.join(compSrc, 'Parameters_F_To_K_nominals_%s.p' %  suffix ),'rb')
Param = pickle.load(file2)
file2.close()

elastic = Elastic( eType = elasticity_type)
plastic = Plastic( pType = 'none')

#:------------------------------------
# Set elastic computation
#:------------------------------------

# Mode I

ELTest_I 	= { 'name' : 'EL_Norm', 'loading_type' : loading_type, 'KI_range' : [1.], 
				'KII_range' : [0.], 'KIII_range' : [0.], 'NLGEOM': False }

EL_Norm_JobName_I ,ELJob_Descrip_I = Compute(mdb, ELTest_I, EL_Job, Param, elastic, odbSrcEL)

# Mode II

ELTest_II 	= { 'name' : 'EL_Norm', 'loading_type' : loading_type, 'KI_range' : [0.], 
				'KII_range' : [1.], 'KIII_range' : [0.], 'NLGEOM': False }
EL_Norm_JobName_II , ELJob_Descrip_II = Compute(mdb, ELTest_II, EL_Job, Param, elastic, odbSrcEL)

# Mode III

ELTest_III 	= { 'name' : 'EL_Norm', 'loading_type' : loading_type, 'KI_range' : [0.], 
				'KII_range' : [0.], 'KIII_range' : [1.], 'NLGEOM': False }
EL_Norm_JobName_III , ELJob_Descrip_III = Compute(mdb, ELTest_III, EL_Job, Param, elastic, odbSrcEL)


file2=open('EL_job_details_I.txt','w') 
file2.write('%s\n' % EL_Norm_JobName_I) 
file2.write('%s\n' % ELJob_Descrip_I ) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

file2=open('EL_job_details_II.txt','w') 
file2.write('%s\n' % EL_Norm_JobName_II) 
file2.write('%s\n' % ELJob_Descrip_II ) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

file2=open('EL_job_details_III.txt','w') 
file2.write('%s\n' % EL_Norm_JobName_III) 
file2.write('%s\n' % ELJob_Descrip_III ) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

#:------------------------------------
# Set plastic computation
#:------------------------------------

# Test parameters:

KI_range_I   = [ 12.]
KII_range_I  = [  0.]
KIII_range_I = [  0.]

PLTest_I 	 = { 'name' : 'EP', 'test_type' : 'Mon', 'NLGEOM': False ,
				'loading_type' : loading_type, 'KI_range' : KI_range_I , 
				'KII_range' : KII_range_I, 'KIII_range' : KIII_range_I }

KI_range_II   = [  0.5 ]
KII_range_II  = [   7. ]
KIII_range_II = [   0. ]

PLTest_II 	 = { 'name' : 'EP', 'test_type' : 'Mon', 'NLGEOM': False ,
				'loading_type' : loading_type, 'KI_range' : KI_range_II, 
				'KII_range' : KII_range_II, 'KIII_range' : KIII_range_II }

KI_range_III   = [   0.5]
KII_range_III  = [   0. ]
KIII_range_III = [   7.]

PLTest_III 	 = { 'name' : 'EP', 'test_type' : 'Mon', 'NLGEOM': False ,
				'loading_type' : loading_type, 'KI_range' : KI_range_III, 
				'KII_range' : KII_range_III, 'KIII_range' : KIII_range_III }

KI_range_Mix   = [  10.]
KII_range_Mix  = [  6.]
KIII_range_Mix = [  4.]

PLTest_Mix 	 = { 'name' : 'EP', 'test_type' : 'Mon', 'NLGEOM': False ,
				'loading_type' : loading_type, 'KI_range' : KI_range_Mix, 
				'KII_range' : KII_range_Mix, 'KIII_range' : KIII_range_Mix }


# Write inp files

Mon_PL_JobName_I   , EPJob_Descrip_I   = Compute(mdb, PLTest_I  , PL_Mon_Job, Param, elastic, odbSrcLGEOM)
Mon_PL_JobName_II  , EPJob_Descrip_II  = Compute(mdb, PLTest_II , PL_Mon_Job, Param, elastic, odbSrcLGEOM)
Mon_PL_JobName_III , EPJob_Descrip_III = Compute(mdb, PLTest_III, PL_Mon_Job, Param, elastic, odbSrcLGEOM)
Mon_PL_JobName_Mix , EPJob_Descrip_Mix = Compute(mdb, PLTest_Mix, PL_Mon_Job, Param, elastic, odbSrcLGEOM)

file2=open('EP_job_details_I.txt','w') 
file2.write('%s\n' % Mon_PL_JobName_I) 
file2.write('%s\n' % EPJob_Descrip_I ) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

file2=open('EP_job_details_II.txt','w') 
file2.write('%s\n' % Mon_PL_JobName_II) 
file2.write('%s\n' % EPJob_Descrip_II ) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

file2=open('EP_job_details_III.txt','w') 
file2.write('%s\n' % Mon_PL_JobName_III) 
file2.write('%s\n' % EPJob_Descrip_III ) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

file2=open('EP_job_details_Mix.txt','w') 
file2.write('%s\n' % Mon_PL_JobName_Mix) 
file2.write('%s\n' % EPJob_Descrip_Mix ) 
file2.write('%s\n' % odbSrc) 
file2.write('%s\n' % odbSrcEL ) 
file2.write('%s\n' % odbSrcLGEOM ) 
file2.close()

# Save Job Container for Post processing

Job = Container()
# For mode I
Job.I = Container()
Job.I.EL = Container()
Job.I.PL = Container()
# For mode II
Job.II = Container()
Job.II.EL = Container()
Job.II.PL = Container()
# For mode III
Job.III = Container()
Job.III.EL = Container()
Job.III.PL = Container()

Job.Mix = Container()
Job.Mix.EL = Container()
Job.Mix.PL = Container()

EL_Norm_JobName_I  , ELJob_Descrip_I   = Generate_names(ELTest_I  , elastic, odbSrcLGEOM )
EL_Norm_JobName_II , ELJob_Descrip_II  = Generate_names(ELTest_II , elastic, odbSrcLGEOM )
EL_Norm_JobName_III, ELJob_Descrip_III = Generate_names(ELTest_III, elastic, odbSrcLGEOM )

Mon_PL_JobName_I   , EPJob_Descrip_I   = Generate_names(PLTest_I  , elastic, odbSrcLGEOM )
Mon_PL_JobName_II  , EPJob_Descrip_II  = Generate_names(PLTest_II , elastic, odbSrcLGEOM )
Mon_PL_JobName_III , EPJob_Descrip_III = Generate_names(PLTest_III, elastic, odbSrcLGEOM )
Mon_PL_JobName_Mix , EPJob_Descrip_Mix = Generate_names(PLTest_Mix, elastic, odbSrcLGEOM )

Job.I.EL.NormName       = EL_Norm_JobName_I
Job.I.PL.MonName        = Mon_PL_JobName_I
Job.I.PL.MonKI_range    = KI_range_I
Job.I.PL.MonKII_range   = KII_range_I
Job.I.PL.MonKIII_range  = KIII_range_I

Job.II.EL.NormName      = EL_Norm_JobName_II
Job.II.PL.MonName       = Mon_PL_JobName_II
Job.II.PL.MonKI_range   = KI_range_II
Job.II.PL.MonKII_range  = KII_range_II
Job.II.PL.MonKIII_range = KIII_range_II

Job.III.EL.NormName      = EL_Norm_JobName_III
Job.III.PL.MonName       = Mon_PL_JobName_III
Job.III.PL.MonKI_range   = KI_range_III
Job.III.PL.MonKII_range  = KII_range_III
Job.III.PL.MonKIII_range = KIII_range_III

Job.Mix.PL.MonName       = Mon_PL_JobName_Mix
Job.Mix.PL.MonKI_range   = KI_range_Mix
Job.Mix.PL.MonKII_range  = KII_range_Mix
Job.Mix.PL.MonKIII_range = KIII_range_Mix

file2=open(os.path.join( odbSrc,'Job_Parameters_%s.p' %  suffix),'wb')
pickle.dump(Job, file2)
file2.close()

