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

Pi=acos(-1.)

coef_I   = 1.
coef_II  = 1.
coef_III = 1.

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

## Source folders

PostProcSrc = os.path.join(codeSrc,'src_Post_Proc')

R1 = 'Results_Post_Proc'
R2 =  loading_type
R3 = 'Results_Post_Proc_octahedral'
R4 = 'Results_Post_Proc_%s' % (suffix )
R5 = 'AM1_20'

ResultsDir = os.path.join(R1, R2, R3, R4, R5)
if not os.path.exists(ResultsDir):
    os.makedirs(ResultsDir)

class Container(object):
    def __init__(self):
        pass

# Load Job parameters:
file2=open(os.path.join( odbSrc,'Job_Parameters_%s.p' %  suffix ),'rb')
Job = pickle.load(file2)
file2.close()

#----------------------------------------------------------------
#                       Call used functions
#----------------------------------------------------------------

srcFile = os.path.join(PostProcSrc, 'Extract_Nodes.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Extract_Total_Disp_Without_Correction.py')
execfile(srcFile)


#-------------------------------------------------------------------------------
#    Extract nodes from model (same model for different computations)
#-------------------------------------------------------------------------------

JobName = Job.I.EL.NormName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcEL,JobName))
dimensions.listN_TIP, dimensions.listN_F_unsorted, dimensions.listN_F_sorted, dimensions.listN_F_z_x_y, dimensions.listN_F_z_rad_ang =  Extract_Nodes_History_Output(odb)
odb.close()

dimensions.listN_F_len = len(dimensions.listN_F_sorted)

dimensions.radial = [ dimensions.listN_F_z_rad_ang[r*dimensions.thet_len][1]  for r in range(dimensions.rad_len)]

#-------------------------------------------------------------------------------
#    Extract nodes from model (same model for different computations)
#-------------------------------------------------------------------------------

n_act_steps = 1
slip_systems_list = ['b4','b2','b5','d4','d1','d6','a2','a6','a3','c5','c3','c1']


for slip_suffix in slip_systems_list :
    ### Results folder:
    odbSrcSlip = os.path.join( odbSrc, slip_suffix )
    ResultsDir_Slip = os.path.join(ResultsDir, slip_suffix)
    if not os.path.exists(ResultsDir_Slip):
        os.makedirs(ResultsDir_Slip)
    for mode in ['I','II','III']:
    	os.system('echo slip system %s mode %s' % (slip_suffix, mode) )
    	JobName = '%s_%s' % (eval('Job.%s.PL.MonName'% mode) , slip_suffix)
    	odb=openOdb(path=os.path.join(odbSrcSlip, '%s.odb' %JobName ))
    	time , EV1_Cum_tot, EV1_Cum_moy, EV1_Cum_quad = Extract_Cumulated_Strain_Field_Output(odb,'Step-1', dimensions)
    	odb.close()
    	file2=open(os.path.join( ResultsDir_Slip,'EV1_Cum_moy_%s' % ( JobName ) ),'w') 
    	file2.write('time ,  EV1 Cum arithmetic mean, EV1 Cum quadratic mean')
    	file2.write(' \n' )
    	for t in range(len(time)):
        	file2.write('%30.20E   ' % time[t])
        	file2.write('%30.20E   ' % EV1_Cum_moy[t])
        	file2.write('%30.20E   ' % EV1_Cum_quad[t])
        	file2.write(' \n' )
    	file2.close()


