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

odbSrc = os.path.join(odbDir ,loading_type, 'src_Odb_%s_octahedral' % (suffix ),'Cyclic_Loading')

## Source folders

PostProcSrc = os.path.join(codeSrc,'src_Post_Proc')

R1 = 'Results_Post_Proc'
R2 =  loading_type
R3 = 'Results_Post_Proc_octahedral'
R4 = 'Results_Post_Proc_%s' % (suffix )
R5 = 'Cyclic_Loading'

ResultsDir = os.path.join(R1, R2, R3, R4, R5)
if not os.path.exists(ResultsDir):
    os.makedirs(ResultsDir)


class Container(object):
    def __init__(self):
        pass


# Load Job parameters:
file2=open(os.path.join( compSrc,'Job_Parameters_%s.p' %  suffix ),'rb')
Job = pickle.load(file2)
file2.close()

#----------------------------------------------------------------
#                       Call used functions
#----------------------------------------------------------------

srcFile = os.path.join(PostProcSrc, 'Extract_Nodes.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Extract_Total_Disp_Without_Correction.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Projection.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Reconstruct_Fields.py')
execfile(srcFile)


#-------------------------------------------------------------------------------
# 	 Import Reference fields
#-------------------------------------------------------------------------------

mode_order = 'order_I_II_III'

Uref_PL = Container()
file2=open(os.path.join( codeSrc, 'src_Reference_Fields', 'Projection_On_Crack_Lips', mode_order ,'Uref_PL_I_%s_%s_protocole2.p' % (mode_order, suffix) ),'rb')
Uref_PL.I = pickle.load(file2 )
file2.close()

file2=open(os.path.join( codeSrc, 'src_Reference_Fields', 'Projection_On_Crack_Lips', mode_order  ,'Uref_PL_II_%s_%s_protocole2.p' % (mode_order, suffix) ),'rb')
Uref_PL.II = pickle.load(file2)
file2.close()
file2=open(os.path.join( codeSrc, 'src_Reference_Fields', 'Projection_On_Crack_Lips', mode_order  ,'Uref_PL_III_%s_%s_protocole2.p' % (mode_order, suffix) ),'rb')

Uref_PL.III = pickle.load(file2)
file2.close()

rad_min, rad_max = Uref_PL.I.Extraction_zone

Uref_PL.I.Delta_x = [ Uref_PL.I.x[(r+1)*dimensions.thet_len -1 ] - Uref_PL.I.x[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]
Uref_PL.I.Delta_y = [ Uref_PL.I.y[(r+1)*dimensions.thet_len -1 ] - Uref_PL.I.y[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]
Uref_PL.I.Delta_z = [ Uref_PL.I.z[(r+1)*dimensions.thet_len -1 ] - Uref_PL.I.z[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]

Uref_PL.II.Delta_x = [ Uref_PL.II.x[(r+1)*dimensions.thet_len -1 ] - Uref_PL.II.x[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]
Uref_PL.II.Delta_y = [ Uref_PL.II.y[(r+1)*dimensions.thet_len -1 ] - Uref_PL.II.y[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]
Uref_PL.II.Delta_z = [ Uref_PL.II.z[(r+1)*dimensions.thet_len -1 ] - Uref_PL.II.z[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]

Uref_PL.III.Delta_x = [ Uref_PL.III.x[(r+1)*dimensions.thet_len -1 ] - Uref_PL.III.x[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]
Uref_PL.III.Delta_y = [ Uref_PL.III.y[(r+1)*dimensions.thet_len -1 ] - Uref_PL.III.y[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]
Uref_PL.III.Delta_z = [ Uref_PL.III.z[(r+1)*dimensions.thet_len -1 ] - Uref_PL.III.z[r*dimensions.thet_len]  for r in range(rad_min, rad_max)  ]


file2=open(os.path.join( codeSrc, 'src_Reference_Fields' , 'Projection_On_Crack_Lips','Uref_EL_%s.p' %suffix ),'rb')
Uref = pickle.load(file2 )
file2.close() 
Uref_EL = Uref.EL


#-------------------------------------------------------------------------------------------------
#                               Extract data
#-------------------------------------------------------------------------------------------------


n_act_steps = 2

mode = 'I'

Job = eval('Job.%s' % mode )

test = Container()
test.JobName = Job.PL.CycName  + '.odb'

odb=openOdb(path=os.path.join(odbSrc, test.JobName ))

#-------------------------------------------------------------------------------
#    Extract nodes from model (same model for different computations)
#-------------------------------------------------------------------------------

dimensions.listN_TIP, dimensions.listN_F_unsorted, dimensions.listN_F_sorted, dimensions.listN_F_z_x_y, dimensions.listN_F_z_rad_ang =  Extract_Nodes_History_Output(odb)

dimensions.listN_F_len = len(dimensions.listN_F_sorted)

print 'Number of chosen nodes in the interest zone =', dimensions.listN_F_len
print 'number of radial nodes                      =', dimensions.rad_len
print 'number of angular nodes                     = ', dimensions.thet_len
print 'number of thickness nodes                   = ', dimensions.z_len

dimensions.radial = [ dimensions.listN_F_z_rad_ang[r*dimensions.thet_len][1]  for r in range(dimensions.rad_len)]

#-------------------------------------------------------------------------------------------------
#                               Total field extraction 
#-------------------------------------------------------------------------------------------------

Ux_tot   =[]
Uy_tot   =[]
Uz_tot   =[]
time_tot =[]

for i in range(1,n_act_steps+1):
    step = 'Step-%d' %i
    time_tmp, Ux_tot_tmp, Uy_tot_tmp, Uz_tot_tmp = Extract_Total_Disp_History_Output(odb,step, dimensions)
    if i == 1 :
        Ux_tot   = np.transpose(Ux_tot_tmp)
        Uy_tot   = np.transpose(Uy_tot_tmp)
        Uz_tot   = np.transpose(Uz_tot_tmp)
        time_tot = time_tmp
        #theta_corr_Mix = theta_corr_tmp
    else :  
        time_tmp.pop(0)
        time_tmp = [ x+ time_tot[-1] for x in time_tmp]
        Ux_tot = np.concatenate((Ux_tot, np.transpose(Ux_tot_tmp)))
        Uy_tot = np.concatenate((Uy_tot, np.transpose(Uy_tot_tmp)))
        Uz_tot = np.concatenate((Uz_tot, np.transpose(Uz_tot_tmp)))
        time_tot += time_tmp
    del time_tmp, Ux_tot_tmp, Uy_tot_tmp, Uz_tot_tmp

test.time = time_tot
test.dUx_tot = np.transpose(Ux_tot)
test.dUy_tot = np.transpose(Uy_tot)
test.dUz_tot = np.transpose(Uz_tot)

del time_tot, Ux_tot, Uy_tot, Uz_tot

print 'Plastic displacement successfully extracted:'

odb.close()

dimensions.time_len = len(test.time)

#-------------------------------------------------------------------------------------------------
#                         Project fields on crack faces
#-------------------------------------------------------------------------------------------------

ResultsDir_Order_Dependent = os.path.join(ResultsDir, mode_order)
if not os.path.exists(ResultsDir_Order_Dependent):
    os.makedirs(ResultsDir_Order_Dependent)

mode_order_list =  mode_order.split('_')
mode_order_list.pop(0)

test.dKI_tild, test.dKII_tild, test.dKIII_tild, test.dRhoI, test.dRhoII, test.dRhoIII = Projection_on_crack_faces_of_reduced_zone_order_dependent(test, mode_order_list, Uref_EL, Uref_PL)

file2=open(os.path.join( ResultsDir_Order_Dependent,'dK_dRho_%s_Cyclic_mode_%s_Crack_Faces_Projection' %( suffix, mode ) ) ,'w') 

file2.write('time ,    dKI_tild,    dKII_tild,     dKIII_tild,      dRhoI,      dRhoII,      dRhoIII')
file2.write(' \n' )

for t in range(len(test.time)-1):
    file2.write('%30.20E   ' % test.time[t+1])
    file2.write('%30.20E   ' % test.dKI_tild[t])
    file2.write('%30.20E   ' % test.dKII_tild[t])
    file2.write('%30.20E   ' % test.dKIII_tild[t])
    file2.write('%30.20E   ' % test.dRhoI[t])
    file2.write('%30.20E   ' % test.dRhoII[t])
    file2.write('%30.20E   ' % test.dRhoIII[t])    
    file2.write(' \n' )

file2.close()

#-------------------------------------------------------------------------------------------------
#                         Reconstruct fields
#-------------------------------------------------------------------------------------------------

CeR_tmp, CcR_tmp, Plastic_ratio = Reconstruct_Fields( test , Uref_EL, Uref_PL )

file2=open(os.path.join( ResultsDir_Order_Dependent,'Errors_%s_Cyclic_mode_%s_Crack_Faces_Projection' %( suffix, mode ) ) ,'w') 
file2.write('time ,     CeR_tmp,      CcR_tmp,    Plastic_ratio')
file2.write(' \n' )
for t in range(len(test.time)-1):
    file2.write('%30.20E   ' % test.time[t+1])
    file2.write('%30.20E   ' % CeR_tmp[t])
    file2.write('%30.20E   ' % CcR_tmp[t])
    file2.write('%30.20E   ' % Plastic_ratio[t]) 
    file2.write(' \n' )

file2.close()


#-------------------------------------------------------------------------------------------------
#                         Project fields on full fields
#-------------------------------------------------------------------------------------------------

ResultsDir_Order_Dependent = os.path.join(ResultsDir, mode_order)
if not os.path.exists(ResultsDir_Order_Dependent):
    os.makedirs(ResultsDir_Order_Dependent)

mode_order_list =  mode_order.split('_')
mode_order_list.pop(0)

test.dKI_tild, test.dKII_tild, test.dKIII_tild, test.dRhoI, test.dRhoII, test.dRhoIII = Projection_reduced_zone_Order_Dependent(test, mode_order_list, Uref_EL, Uref_PL)

file2=open(os.path.join( ResultsDir_Order_Dependent,'dK_dRho_%s_Cyclic_mode_%s_Full_Field_Projection' %( suffix, mode ) ) ,'w') 

file2.write('time ,    dKI_tild,    dKII_tild,     dKIII_tild,      dRhoI,      dRhoII,      dRhoIII')
file2.write(' \n' )

for t in range(len(test.time)-1):
    file2.write('%30.20E   ' % test.time[t+1])
    file2.write('%30.20E   ' % test.dKI_tild[t])
    file2.write('%30.20E   ' % test.dKII_tild[t])
    file2.write('%30.20E   ' % test.dKIII_tild[t])
    file2.write('%30.20E   ' % test.dRhoI[t])
    file2.write('%30.20E   ' % test.dRhoII[t])
    file2.write('%30.20E   ' % test.dRhoIII[t])    
    file2.write(' \n' )

file2.close()

#-------------------------------------------------------------------------------------------------
#                         Reconstruct fields
#-------------------------------------------------------------------------------------------------

CeR_tmp, CcR_tmp, Plastic_ratio = Reconstruct_Fields( test , Uref_EL, Uref_PL )

file2=open(os.path.join( ResultsDir_Order_Dependent,'Errors_%s_Cyclic_mode_%s_Full_Field_Projection' %( suffix, mode ) ) ,'w') 
file2.write('time ,     CeR_tmp,      CcR_tmp,    Plastic_ratio')
file2.write(' \n' )
for t in range(len(test.time)-1):
    file2.write('%30.20E   ' % test.time[t+1])
    file2.write('%30.20E   ' % CeR_tmp[t])
    file2.write('%30.20E   ' % CcR_tmp[t])
    file2.write('%30.20E   ' % Plastic_ratio[t]) 
    file2.write(' \n' )

file2.close()


#-------------------------------------------------------------------------------------------------
#                         Mixed Projection on full field then on crack faces
#-------------------------------------------------------------------------------------------------

ResultsDir_Order_Dependent = os.path.join(ResultsDir, mode_order)
if not os.path.exists(ResultsDir_Order_Dependent):
    os.makedirs(ResultsDir_Order_Dependent)

mode_order_list =  mode_order.split('_')
mode_order_list.pop(0)

test.dKI_tild, test.dKII_tild, test.dKIII_tild, test.dRhoI, test.dRhoII, test.dRhoIII = Mixed_Projection_on_reduced_zone_order_dependent(test, mode_order_list, Uref_EL, Uref_PL)

file2=open(os.path.join( ResultsDir_Order_Dependent,'dK_dRho_%s_Cyclic_mode_%s_Mixed_Projection' %( suffix, mode ) ) ,'w') 

file2.write('time ,    dKI_tild,    dKII_tild,     dKIII_tild,      dRhoI,      dRhoII,      dRhoIII')
file2.write(' \n' )

for t in range(len(test.time)-1):
    file2.write('%30.20E   ' % test.time[t+1])
    file2.write('%30.20E   ' % test.dKI_tild[t])
    file2.write('%30.20E   ' % test.dKII_tild[t])
    file2.write('%30.20E   ' % test.dKIII_tild[t])
    file2.write('%30.20E   ' % test.dRhoI[t])
    file2.write('%30.20E   ' % test.dRhoII[t])
    file2.write('%30.20E   ' % test.dRhoIII[t])    
    file2.write(' \n' )

file2.close()

#-------------------------------------------------------------------------------------------------
#                         Reconstruct fields
#-------------------------------------------------------------------------------------------------

CeR_tmp, CcR_tmp, Plastic_ratio = Reconstruct_Fields( test , Uref_EL, Uref_PL )

file2=open(os.path.join( ResultsDir_Order_Dependent,'Errors_%s_Cyclic_mode_%s_Mixed_Projection' %( suffix, mode ) ) ,'w') 
file2.write('time ,     CeR_tmp,      CcR_tmp,    Plastic_ratio')
file2.write(' \n' )
for t in range(len(test.time)-1):
    file2.write('%30.20E   ' % test.time[t+1])
    file2.write('%30.20E   ' % CeR_tmp[t])
    file2.write('%30.20E   ' % CcR_tmp[t])
    file2.write('%30.20E   ' % Plastic_ratio[t]) 
    file2.write(' \n' )

file2.close()

#-------------------------------------------------------------------------------------------------
#                         Save total fields
#-------------------------------------------------------------------------------------------------

file2 = open(os.path.join( ResultsDir,'Test_%s_Cyclic_mode_%s_Crack_Faces_Projection' %( suffix, mode ) ) ,'w') 
pickle.dump(test, file2)
file2.close()


