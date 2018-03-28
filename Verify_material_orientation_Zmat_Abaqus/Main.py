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

codeSrc = os.path.join('..','..','Code','Reference_Fields')
odbDir = 'Results_Odb'
compSrc = os.path.join(codeSrc,'src_Computation')

#for mat_or in [[[0,0,0],[0,0,0]],[[0,1,0],[1,0,0]],[[1,1,0],[1,-1,0]],[[1,1,0],[0,0,1]],[[1,1,0],[1,-1,1]],[[1,2,1],[3,-1,-1]]]:
#	if mat_or[0]==[0,0,0]:
#		elasticity_type = 'isotropic'
#	else :
#		elasticity_type = 'orthotropic'
#		hkl = np.asarray(mat_or[0])
#		uvw = np.asarray(mat_or[1])

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

if not os.path.exists(odbSrcEL):
	os.makedirs(odbSrcEL)

odbSrcLGEOM = os.path.join( odbSrc, 'LGEOM')
if not os.path.exists(odbSrcLGEOM):
	os.makedirs(odbSrcLGEOM)

#######################
#   Computation
#######################

#execfile(os.path.join(codeSrc,'Comp_Main.py'))

#######################
#   Post-processing
#######################

###### Reference fields and loading range

execfile(os.path.join(codeSrc,'Post_Proc.py'))

#execfile(os.path.join(codeSrc,'Projection_On_Crack_Lips.py'))


###### Reconstruction

#execfile(os.path.join(codeSrc,'Reconstruct_Fields.py'))
