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

Uref = Container()
Uref.EL = Container()
Uref.PL = Container()

Uref.EL.I = Container()
Uref.EL.II = Container()
Uref.EL.III = Container()

#----------------------------------------------------------------
#                       Call used functions
#----------------------------------------------------------------

srcFile = os.path.join(PostProcSrc, 'Extract_Nodes.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Extract_EL_Disp_Without_Correction.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Extract_Total_Disp_Without_Correction.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Projection.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Plastic_Field.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'POD.py')
execfile(srcFile)

#-------------------------------------------------------------------------------
#    Extract nodes from model (same model for different computations)
#-------------------------------------------------------------------------------

JobName = Job.I.EL.NormName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcEL,JobName))
dimensions.listN_TIP, dimensions.listN_F_unsorted, dimensions.listN_F_sorted, dimensions.listN_F_z_x_y, dimensions.listN_F_z_rad_ang =  Extract_Nodes_History_Output(odb)
odb.close()

dimensions.listN_F_len = len(dimensions.listN_F_sorted)

print 'Number of chosen nodes in the interest zone =', dimensions.listN_F_len
print 'number of radial nodes                      =', dimensions.rad_len
print 'number of angular nodes                     = ', dimensions.thet_len
print 'number of thickness nodes                   = ', dimensions.z_len

dimensions.radial = [ dimensions.listN_F_z_rad_ang[r*dimensions.thet_len][1]  for r in range(dimensions.rad_len)]

#-------------------------------------------------------------------------------
# 	 Import Reference fields
#-------------------------------------------------------------------------------
'''
Uref.EL.I.x  , Uref.EL.I.y  , Uref.EL.I.z   = loadtxt(os.path.join( ResultsDir,'plot_U_EL_ref_I_%s'   % ( suffix )) , unpack = True)
Uref.EL.II.x , Uref.EL.II.y , Uref.EL.II.z  = loadtxt(os.path.join( ResultsDir,'plot_U_EL_ref_II_%s'  % ( suffix )) , unpack = True)
Uref.EL.III.x, Uref.EL.III.y, Uref.EL.III.z = loadtxt(os.path.join( ResultsDir,'plot_U_EL_ref_III_%s' % ( suffix )) , unpack = True)

Uref.EL.I.f_r  , Uref.EL.I.g_theta_x  , Uref.EL.I.g_theta_y  , Uref.EL.I.g_theta_z   = POD_r_theta(Uref.EL.I.x  , Uref.EL.I.y  , Uref.EL.I.z  , 'Mode I'  , dimensions)
Uref.EL.II.f_r , Uref.EL.II.g_theta_x , Uref.EL.II.g_theta_y , Uref.EL.II.g_theta_z  = POD_r_theta(Uref.EL.II.x , Uref.EL.II.y , Uref.EL.II.z , 'Mode II' , dimensions)
Uref.EL.III.f_r, Uref.EL.III.g_theta_x, Uref.EL.III.g_theta_y, Uref.EL.III.g_theta_z = POD_r_theta(Uref.EL.III.x, Uref.EL.III.y, Uref.EL.III.z, 'Mode III', dimensions)
'''

#-------------------------------------------------------------------------------------------------
#                          Equi-biaxial elastic reference fields     Mode I
#-------------------------------------------------------------------------------------------------

JobName = Job.I.EL.NormName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcEL,JobName))

Ux_EL_I, Uy_EL_I, Uz_EL_I = Extract_EL_Disp_History_Output(odb, dimensions, coef_I)
print 'Elastic displacement of Equi-biaxial test successfully extracted'

odb.close()


#Ux_I, Uy_I, Uz_I, Ux_II, Uy_II, Uz_II, Ux_III, Uy_III, Uz_III = EL_Sym_Asym_Decomp(Ux_EL_I, Uy_EL_I, Uz_EL_I, rad_len, thet_len, z_len)
#Ux_EL_ref_I = Ux_I.reshape(listN_F_len)
#Uy_EL_ref_I = Uy_I.reshape(listN_F_len)
#Uz_EL_ref_I = Uz_I.reshape(listN_F_len)
#del Ux_I, Uy_I, Uz_I, Ux_II, Uy_II, Uz_II, Ux_III, Uy_III, Uz_III


Ux_EL_ref_I = Ux_EL_I
Uy_EL_ref_I = Uy_EL_I
Uz_EL_ref_I = Uz_EL_I

file2=open(os.path.join( ResultsDir,'plot_U_EL_ref_I_%s' % suffix),'w') 
for p in range(dimensions.listN_F_len):
    file2.write('%30.20E   ' % Ux_EL_ref_I[p]) 
    file2.write('%30.20E   ' % Uy_EL_ref_I[p])       
    file2.write('%30.20E   ' % Uz_EL_ref_I[p])       
    file2.write(' \n' )         

file2.close()

#-------------------------------------------------------------------------------------------------
#                          Left shear elastic reference fields     Mode II
#-------------------------------------------------------------------------------------------------

JobName = Job.II.EL.NormName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcEL, JobName ))

Ux_EL_II, Uy_EL_II, Uz_EL_II = Extract_EL_Disp_History_Output(odb, dimensions, coef_II)
print 'Elastic displacement of shear test successfully extracted'

odb.close()


#Ux_I, Uy_I, Uz_I, Ux_II, Uy_II, Uz_II, Ux_III, Uy_III, Uz_III = EL_Sym_Asym_Decomp(Ux_EL_II, Uy_EL_II, Uz_EL_II, rad_len, thet_len, z_len)
#Ux_EL_ref_II = Ux_II.reshape(listN_F_len)
#Uy_EL_ref_II = Uy_II.reshape(listN_F_len)
#Uz_EL_ref_II = Uz_II.reshape(listN_F_len)
#del Ux_I, Uy_I, Uz_I, Ux_II, Uy_II, Uz_II, Ux_III, Uy_III, Uz_III


Ux_EL_ref_II = Ux_EL_II
Uy_EL_ref_II = Uy_EL_II
Uz_EL_ref_II = Uz_EL_II

file2=open(os.path.join( ResultsDir,'plot_U_EL_ref_II_%s' % ( suffix )),'w') 
for p in range(dimensions.listN_F_len):
    file2.write('%30.20E   ' % Ux_EL_ref_II[p]) 
    file2.write('%30.20E   ' % Uy_EL_ref_II[p])       
    file2.write('%30.20E   ' % Uz_EL_ref_II[p])       
    file2.write(' \n' )         

file2.close()

#-------------------------------------------------------------------------------------------------
#                         Antiplane elastic reference fields     Mode III
#-------------------------------------------------------------------------------------------------

JobName = Job.III.EL.NormName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcEL, JobName ))

Ux_EL_III, Uy_EL_III, Uz_EL_III = Extract_EL_Disp_History_Output(odb, dimensions, coef_III)
print 'Elastic displacement of shear test successfully extracted'

odb.close()


#Ux_I, Uy_I, Uz_I, Ux_II, Uy_II, Uz_II, Ux_III, Uy_III, Uz_III = EL_Sym_Asym_Decomp(Ux_EL_III, Uy_EL_III, Uz_EL_III, rad_len, thet_len, z_len)
#Ux_EL_ref_III = Ux_III.reshape(listN_F_len)
#Uy_EL_ref_III = Uy_III.reshape(listN_F_len)
#Uz_EL_ref_III = Uz_III.reshape(listN_F_len)
#del Ux_I, Uy_I, Uz_I, Ux_II, Uy_II, Uz_II, Ux_III, Uy_III, Uz_III


Ux_EL_ref_III = Ux_EL_III
Uy_EL_ref_III = Uy_EL_III
Uz_EL_ref_III = Uz_EL_III

file2=open(os.path.join( ResultsDir,'plot_U_EL_ref_III_%s' % ( suffix )),'w') 
for p in range(dimensions.listN_F_len):
    file2.write('%30.20E   ' % Ux_EL_ref_III[p]) 
    file2.write('%30.20E   ' % Uy_EL_ref_III[p])       
    file2.write('%30.20E   ' % Uz_EL_ref_III[p])       
    file2.write(' \n' )         

file2.close()

#-------------------------------------------------------------------------------------------------
#                                Elastic reference fields
#-------------------------------------------------------------------------------------------------

Norme_EL_I   = pow(np.linalg.norm(Ux_EL_ref_I)  ,2) + pow(np.linalg.norm(Uy_EL_ref_I)  ,2) + pow(np.linalg.norm(Uz_EL_ref_I)  ,2)
Norme_EL_II  = pow(np.linalg.norm(Ux_EL_ref_II) ,2) + pow(np.linalg.norm(Uy_EL_ref_II) ,2) + pow(np.linalg.norm(Uz_EL_ref_II) ,2)
Norme_EL_III = pow(np.linalg.norm(Ux_EL_ref_III),2) + pow(np.linalg.norm(Uy_EL_ref_III),2) + pow(np.linalg.norm(Uz_EL_ref_III),2)

Uref.EL.I.x      = Ux_EL_ref_I
Uref.EL.I.y      = Uy_EL_ref_I
Uref.EL.I.z      = Uz_EL_ref_I
Uref.EL.I.norme  = Norme_EL_I

Uref.EL.II.x     = Ux_EL_ref_II
Uref.EL.II.y     = Uy_EL_ref_II
Uref.EL.II.z     = Uz_EL_ref_II
Uref.EL.II.norme = Norme_EL_II

Uref.EL.III.x     = Ux_EL_ref_III
Uref.EL.III.y     = Uy_EL_ref_III
Uref.EL.III.z     = Uz_EL_ref_III
Uref.EL.III.norme = Norme_EL_III

# Displacement jump around the crack tip

Uref.EL.I.Delta_x = [ Uref.EL.I.x[(r+1)*dimensions.thet_len -1 ] - Uref.EL.I.x[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]
Uref.EL.I.Delta_y = [ Uref.EL.I.y[(r+1)*dimensions.thet_len -1 ] - Uref.EL.I.y[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]
Uref.EL.I.Delta_z = [ Uref.EL.I.z[(r+1)*dimensions.thet_len -1 ] - Uref.EL.I.z[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]

Uref.EL.II.Delta_x = [ Uref.EL.II.x[(r+1)*dimensions.thet_len -1 ] - Uref.EL.II.x[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]
Uref.EL.II.Delta_y = [ Uref.EL.II.y[(r+1)*dimensions.thet_len -1 ] - Uref.EL.II.y[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]
Uref.EL.II.Delta_z = [ Uref.EL.II.z[(r+1)*dimensions.thet_len -1 ] - Uref.EL.II.z[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]

Uref.EL.III.Delta_x = [ Uref.EL.III.x[(r+1)*dimensions.thet_len -1 ] - Uref.EL.III.x[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]
Uref.EL.III.Delta_y = [ Uref.EL.III.y[(r+1)*dimensions.thet_len -1 ] - Uref.EL.III.y[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]
Uref.EL.III.Delta_z = [ Uref.EL.III.z[(r+1)*dimensions.thet_len -1 ] - Uref.EL.III.z[r*dimensions.thet_len]  for r in range(dimensions.rad_len)  ]

Uref.EL.I.DU_norme   = pow(np.linalg.norm(Uref.EL.I.Delta_x)  ,2) + pow(np.linalg.norm(Uref.EL.I.Delta_y)  ,2) + pow(np.linalg.norm(Uref.EL.I.Delta_z)  ,2)
Uref.EL.II.DU_norme  = pow(np.linalg.norm(Uref.EL.II.Delta_x) ,2) + pow(np.linalg.norm(Uref.EL.II.Delta_y) ,2) + pow(np.linalg.norm(Uref.EL.II.Delta_z) ,2)
Uref.EL.III.DU_norme = pow(np.linalg.norm(Uref.EL.III.Delta_x),2) + pow(np.linalg.norm(Uref.EL.III.Delta_y),2) + pow(np.linalg.norm(Uref.EL.III.Delta_z),2)

#----------------------------------------------------------------
#        POD r-theta  for elastic reference fields
#----------------------------------------------------------------

Uref.EL.I.f_r  , Uref.EL.I.g_theta_x  , Uref.EL.I.g_theta_y  , Uref.EL.I.g_theta_z   = POD_r_theta(Uref.EL.I.x  , Uref.EL.I.y  , Uref.EL.I.z  , 'Mode I'  , dimensions)
Uref.EL.II.f_r , Uref.EL.II.g_theta_x , Uref.EL.II.g_theta_y , Uref.EL.II.g_theta_z  = POD_r_theta(Uref.EL.II.x , Uref.EL.II.y , Uref.EL.II.z , 'Mode II' , dimensions)
Uref.EL.III.f_r, Uref.EL.III.g_theta_x, Uref.EL.III.g_theta_y, Uref.EL.III.g_theta_z = POD_r_theta(Uref.EL.III.x, Uref.EL.III.y, Uref.EL.III.z, 'Mode III', dimensions)

file2=open(os.path.join( ResultsDir,'plot_f_r_EL_I_%s' %  suffix ),'w') 
for p in range(dimensions.rad_len): 
    file2.write('%30.20E'    % dimensions.radial[p])
    file2.write('%30.20E   ' % Uref.EL.I.f_r[p])
    file2.write(' \n' )

file2.close()

file2=open(os.path.join( ResultsDir,'plot_g_theta_EL_I_%s'% suffix ),'w') 
theta= -Pi
for p in range(dimensions.thet_len):  
    file2.write('%30.20E   ' % theta)   
    file2.write('%30.20E   ' % Uref.EL.I.g_theta_x[p]) 
    file2.write('%30.20E   ' % Uref.EL.I.g_theta_y[p])        
    file2.write('%30.20E   ' % Uref.EL.I.g_theta_z[p])        
    file2.write(' \n' )  
    theta += 2*Pi/(dimensions.thet_len-1)

file2.close()

file2=open(os.path.join( ResultsDir,'plot_f_r_EL_II_%s' %  suffix ),'w') 
for p in range(dimensions.rad_len): 
    file2.write('%30.20E'    % dimensions.radial[p])
    file2.write('%30.20E   ' % Uref.EL.II.f_r[p])
    file2.write(' \n' )

file2.close()

file2=open(os.path.join( ResultsDir,'plot_g_theta_EL_II_%s'% suffix ),'w') 
theta= -Pi
for p in range(dimensions.thet_len):  
    file2.write('%30.20E   ' % theta)   
    file2.write('%30.20E   ' % Uref.EL.II.g_theta_x[p]) 
    file2.write('%30.20E   ' % Uref.EL.II.g_theta_y[p])        
    file2.write('%30.20E   ' % Uref.EL.II.g_theta_z[p])        
    file2.write(' \n' )  
    theta += 2*Pi/(dimensions.thet_len-1)

file2.close()

file2=open(os.path.join( ResultsDir,'plot_f_r_EL_III_%s' %  suffix ),'w') 
for p in range(dimensions.rad_len): 
    file2.write('%30.20E'    % dimensions.radial[p])
    file2.write('%30.20E   ' % Uref.EL.III.f_r[p])
    file2.write(' \n' )

file2.close()

file2=open(os.path.join( ResultsDir,'plot_g_theta_EL_III_%s'% suffix ),'w') 
theta= -Pi
for p in range(dimensions.thet_len):  
    file2.write('%30.20E   ' % theta)   
    file2.write('%30.20E   ' % Uref.EL.III.g_theta_x[p]) 
    file2.write('%30.20E   ' % Uref.EL.III.g_theta_y[p])        
    file2.write('%30.20E   ' % Uref.EL.III.g_theta_z[p])        
    file2.write(' \n' )  
    theta += 2*Pi/(dimensions.thet_len-1)

file2.close()

Uref.EL.I.radial   = dimensions.radial
Uref.EL.II.radial  = dimensions.radial
Uref.EL.III.radial = dimensions.radial


file2=open(os.path.join( ResultsDir,'Uref_EL_%s.p' %  suffix ),'wb')
pickle.dump(Uref, file2)
file2.close()

#-------------------------------------------------------------------------------
# 	 Import Total fields
#-------------------------------------------------------------------------------

'''
file2=open(os.path.join( ResultsDir,'Test_I_%s.p' %  suffix ),'rb')
test_I = pickle.load(file2)
file2.close()
file2=open(os.path.join( ResultsDir,'Test_II_%s.p' %  suffix ),'rb')
test_II = pickle.load(file2)
file2.close()
file2=open(os.path.join( ResultsDir,'Test_III_%s.p' %  suffix ),'rb')
test_III = pickle.load(file2)
file2.close()
dimensions.time_len = len(test_I.time)
'''



n_act_steps = 1
slip_systems_list = ['b4','b2','b5','d4','d1','d6','a2','a6','a3','c5','c3','c1']

for slip_suffix in slip_systems_list :
    ### Results folder:
    odbSrcSlip = os.path.join( odbSrc, slip_suffix )
    ResultsDir_Slip = os.path.join(ResultsDir, slip_suffix)
    if not os.path.exists(ResultsDir_Slip):
        os.makedirs(ResultsDir_Slip)
    #-------------------------------------------------------------------------------------------------
    #                               Total field extraction   Mode I
    #-------------------------------------------------------------------------------------------------
    test_I = Container()
    test_I.JobName = '%s_%s.odb' % (Job.I.PL.MonName , slip_suffix)
    odb=openOdb(path=os.path.join(odbSrcSlip, test_I.JobName ))
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
    
    test_I.time = time_tot
    test_I.dUx_tot = np.transpose(Ux_tot)
    test_I.dUy_tot = np.transpose(Uy_tot)
    test_I.dUz_tot = np.transpose(Uz_tot)
    del time_tot, Ux_tot, Uy_tot, Uz_tot
    print 'Plastic displacement of mode I test successfully extracted:'
    odb.close()
    dimensions.time_len = len(test_I.time)
    #-------------------------------------------------------------------------------------------------
    #                               Total field extraction   Mode II
    #-------------------------------------------------------------------------------------------------
    test_II = Container()
    test_II.JobName = '%s_%s.odb' % (Job.II.PL.MonName , slip_suffix)
    odb=openOdb(path=os.path.join(odbSrcSlip, test_II.JobName ))
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
    test_II.time = time_tot
    test_II.dUx_tot = np.transpose(Ux_tot)
    test_II.dUy_tot = np.transpose(Uy_tot)
    test_II.dUz_tot = np.transpose(Uz_tot)
    del time_tot, Ux_tot, Uy_tot, Uz_tot
    print 'Plastic displacement of mode II test successfully extracted:'
    odb.close()
    #-------------------------------------------------------------------------------------------------
    #                               Total field extraction   Mode III
    #-------------------------------------------------------------------------------------------------
    test_III = Container()
    test_III.JobName = '%s_%s.odb' % (Job.III.PL.MonName , slip_suffix)
    odb=openOdb(path=os.path.join(odbSrcSlip, test_III.JobName ))
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
    
    test_III.time = time_tot
    test_III.dUx_tot = np.transpose(Ux_tot)
    test_III.dUy_tot = np.transpose(Uy_tot)
    test_III.dUz_tot = np.transpose(Uz_tot)
    del time_tot, Ux_tot, Uy_tot, Uz_tot
    print 'Plastic displacement of mode III test successfully extracted:'
    odb.close()
    #-------------------------------------------------------------------------------------------------
    #                         Save total fields
    #-------------------------------------------------------------------------------------------------    
    mode_order_list        = [  ['','','']   , ['I','II','III'] ]
    mode_order_suffix_list = ['without_order', 'order_I_II_III' ]
    for mode_order, mode_order_suffix in zip(mode_order_list, mode_order_suffix_list) :
        ResultsDir_Order_Dependent = os.path.join(ResultsDir_Slip, mode_order_suffix)
        if not os.path.exists(ResultsDir_Order_Dependent):
            os.makedirs(ResultsDir_Order_Dependent)
        if mode_order_suffix == 'without_order':
            dUx_PL_I  , dUy_PL_I  , dUz_PL_I  , dKI_tild_I  , dKII_tild_I  , dKIII_tild_I   = Plastic_Field_Faces_Projection(test_I , Uref.EL , dimensions)
            dUx_PL_II , dUy_PL_II , dUz_PL_II , dKI_tild_II , dKII_tild_II , dKIII_tild_II  = Plastic_Field_Faces_Projection(test_II , Uref.EL , dimensions)
            dUx_PL_III, dUy_PL_III, dUz_PL_III, dKI_tild_III, dKII_tild_III, dKIII_tild_III = Plastic_Field_Faces_Projection(test_III , Uref.EL , dimensions)
        else :
            dUx_PL_I  , dUy_PL_I  , dUz_PL_I  , dKI_tild_I  , dKII_tild_I  , dKIII_tild_I   = Plastic_Field_Faces_Projection_Order_Dependent(test_I, mode_order , Uref.EL , dimensions)
            dUx_PL_II , dUy_PL_II , dUz_PL_II , dKI_tild_II , dKII_tild_II , dKIII_tild_II  = Plastic_Field_Faces_Projection_Order_Dependent(test_II, mode_order , Uref.EL , dimensions)
            dUx_PL_III, dUy_PL_III, dUz_PL_III, dKI_tild_III, dKII_tild_III, dKIII_tild_III = Plastic_Field_Faces_Projection_Order_Dependent(test_III, mode_order , Uref.EL , dimensions)
        ##### Mode I
        file2=open(os.path.join( ResultsDir_Order_Dependent,'plot_dK_I_%s' % suffix),'w') 
        for t in range(len(test_I.time)-1):
            file2.write('%30.20E   ' % test_I.time[t+1])
            file2.write('%30.20E   ' % dKI_tild_I[t])
            file2.write('%30.20E   ' % dKII_tild_I[t])
            file2.write('%30.20E   ' % dKIII_tild_I[t])
            file2.write(' \n' )
        file2.close()
        ##### Mode II
        file2=open(os.path.join( ResultsDir_Order_Dependent,'plot_dK_II_%s' % suffix),'w') 
        for t in range(len(test_II.time)-1):
            file2.write('%30.20E   ' % test_II.time[t+1])
            file2.write('%30.20E   ' % dKI_tild_II[t])
            file2.write('%30.20E   ' % dKII_tild_II[t])
            file2.write('%30.20E   ' % dKIII_tild_II[t])
            file2.write(' \n' )
        file2.close()
        ##### Mode III
        file2=open(os.path.join( ResultsDir_Order_Dependent,'plot_dK_III_%s' % suffix),'w') 
        for t in range(len(test_III.time)-1):
            file2.write('%30.20E   ' % test_III.time[t+1])
            file2.write('%30.20E   ' % dKI_tild_III[t])
            file2.write('%30.20E   ' % dKII_tild_III[t])
            file2.write('%30.20E   ' % dKIII_tild_III[t])
            file2.write(' \n' )
        file2.close()
        #-------------------------------------------------------------------------------------------------
        #                         Save plastic fields
        #-------------------------------------------------------------------------------------------------
        Order          = Container()
        Order.dUPL     = Container()
        Order.dUPL.I   = Container()
        Order.dUPL.II  = Container()
        Order.dUPL.III = Container()
        Order.dUPL.I.time  , Order.dUPL.I.x  , Order.dUPL.I.y  , Order.dUPL.I.z  , Order.dUPL.I.dKI_tild  ,  Order.dUPL.I.dKII_tild  ,  Order.dUPL.I.dKIII_tild   = test_I.time  , dUx_PL_I  , dUy_PL_I  , dUz_PL_I  , dKI_tild_I  , dKII_tild_I  , dKIII_tild_I
        Order.dUPL.II.time , Order.dUPL.II.x , Order.dUPL.II.y , Order.dUPL.II.z , Order.dUPL.II.dKI_tild ,  Order.dUPL.II.dKII_tild ,  Order.dUPL.II.dKIII_tild  = test_II.time , dUx_PL_II , dUy_PL_II , dUz_PL_II , dKI_tild_II , dKII_tild_II , dKIII_tild_II
        Order.dUPL.III.time, Order.dUPL.III.x, Order.dUPL.III.y, Order.dUPL.III.z, Order.dUPL.III.dKI_tild,  Order.dUPL.III.dKII_tild,  Order.dUPL.III.dKIII_tild = test_III.time, dUx_PL_III, dUy_PL_III, dUz_PL_III, dKI_tild_III, dKII_tild_III, dKIII_tild_III
        Order.dUPL.I.Loading_range   = Job.I.PL.MonKI_range
        Order.dUPL.II.Loading_range  = Job.II.PL.MonKII_range
        Order.dUPL.III.Loading_range = Job.III.PL.MonKIII_range
        file2=open(os.path.join( ResultsDir_Order_Dependent,'Plastic_Field_%s_%s.p' % (mode_order_suffix, suffix ) ),'wb')
        pickle.dump(Order, file2)
        file2.close()
    file2=open(os.path.join( ResultsDir_Slip,'Test_I_%s_%s.p' %  (suffix, slip_suffix) ),'wb')
    pickle.dump(test_I, file2)
    file2.close()
    file2=open(os.path.join( ResultsDir_Slip,'Test_II_%s_%s.p' %  (suffix, slip_suffix) ),'wb')
    pickle.dump(test_II, file2)
    file2.close()
    file2=open(os.path.join( ResultsDir_Slip,'Test_III_%s_%s.p' %  (suffix, slip_suffix) ),'wb')
    pickle.dump(test_III, file2)
    file2.close()
    #-------------------------------------------------------------------------------------------------
    #                               Total filed extraction   Mixed Mode
    #-------------------------------------------------------------------------------------------------
    '''
    test_Mix = Container()
    test_Mix.JobName = '%s_%s.odb' % (Job.Mix.PL.MonName , slip_suffix)
    odb=openOdb(path=os.path.join(odbSrcSlip, test_Mix.JobName ))
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
    
    test_Mix.time = time_tot
    test_Mix.dUx_tot = np.transpose(Ux_tot)
    test_Mix.dUy_tot = np.transpose(Uy_tot)
    test_Mix.dUz_tot = np.transpose(Uz_tot)
    del time_tot, Ux_tot, Uy_tot, Uz_tot
    print 'Plastic displacement of mode III test successfully extracted:'
    odb.close()
    test_Mix.MonKI_range   = Job.Mix.PL.MonKI_range  
    test_Mix.MonKII_range  = Job.Mix.PL.MonKII_range
    test_Mix.MonKIII_range = Job.Mix.PL.MonKIII_range
    #-------------------------------------------------------------------------------------------------
    #                         Save total fields
    #-------------------------------------------------------------------------------------------------
    file2=open(os.path.join( ResultsDir,'Test_Mix_%s_%s.p' %  (suffix, slip_suffix) ),'wb')
    pickle.dump(test_Mix, file2)
    file2.close()
    '''

