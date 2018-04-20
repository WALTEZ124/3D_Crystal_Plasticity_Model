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
coef_II  = 1.		# if Right 1 , if left -1
coef_III = 1.        # 
coef_Mix = 1.


PostProcSrc = os.path.join(codeSrc,'src_Post_Proc')

R1 = 'Results_Post_Proc'
R2 =  loading_type
R3 = 'Results_Post_Proc_%d_%d_%d' % (R0, C1, Gamma1 )
R4 = 'Results_Post_Proc_%s' % (suffix )
R5 = 'Small_Loading_Unloading'

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

Uref.PL = Container()
Uref.PL.I = Container()
Uref.PL.II = Container()
Uref.PL.III = Container()

#----------------------------------------------------------------
#                       Call used functions
#----------------------------------------------------------------

srcFile = os.path.join(PostProcSrc, 'Extract_Nodes.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Extract_EL_Disp_Without_Correction.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Extract_Total_Disp_Without_Correction.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'EL_Sym_Asym_Decomp.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'PL_Sym_Asym_Decomp.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'POD.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Plastic_Field.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Projection.py')
execfile(srcFile)
srcFile = os.path.join(PostProcSrc, 'Reconstruct_Fields.py')
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

#-------------------------------------------------------------------------------------------------
#                          Equi-biaxial elastic reference fields     Mode I
#-------------------------------------------------------------------------------------------------
'''
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

#-------------------------------------------------------------------------------------------------
#                               Total field extraction   Mode I
#-------------------------------------------------------------------------------------------------

test_I = Container()

test_I.JobName = Job.I.PL.MonName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcLGEOM, test_I.JobName ))

Ux_tot   =[]
Uy_tot   =[]
Uz_tot   =[]
time_tot =[]

for i in range(1,3):
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
#                               Total filed extraction   Mode II
#-------------------------------------------------------------------------------------------------

test_II = Container()

test_II.JobName = Job.II.PL.MonName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcLGEOM, test_II.JobName ))

Ux_tot   =[]
Uy_tot   =[]
Uz_tot   =[]
time_tot =[]

for i in range(1,3):
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
#                               Total filed extraction   Mode III
#-------------------------------------------------------------------------------------------------

test_III = Container()

test_III.JobName = Job.III.PL.MonName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcLGEOM, test_III.JobName ))

Ux_tot   =[]
Uy_tot   =[]
Uz_tot   =[]
time_tot =[]

for i in range(1,3):
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

file2=open(os.path.join( ResultsDir,'Test_I_%s.p' %  suffix ),'wb')
pickle.dump(test_I, file2)
file2.close()

file2=open(os.path.join( ResultsDir,'Test_II_%s.p' %  suffix ),'wb')
pickle.dump(test_II, file2)
file2.close()

file2=open(os.path.join( ResultsDir,'Test_III_%s.p' %  suffix ),'wb')
pickle.dump(test_III, file2)
file2.close()
'''
#-------------------------------------------------------------------------------
#    Explore different projection orders
#-------------------------------------------------------------------------------
'''
mode_order_list        = [ ['I','II','III'], ['I','III','II'], ['II','I','III'], ['II','III','I'], ['III','I','II'], ['III','II','I'] ]
mode_order_suffix_list = [ 'order_I_II_III', 'order_I_III_II', 'order_II_I_III', 'order_II_III_I', 'order_III_I_II', 'order_III_II_I' ]

for mode_order, mode_order_suffix in zip(mode_order_list, mode_order_suffix_list) :
    ResultsDir_Order_Dependent = os.path.join(ResultsDir, mode_order_suffix)
    if not os.path.exists(ResultsDir_Order_Dependent):
        os.makedirs(ResultsDir_Order_Dependent)
    ##### Mode I
    dUx_PL_I, dUy_PL_I, dUz_PL_I, dKI_tild_I, dKII_tild_I, dKIII_tild_I = Plastic_Field_Order_Dependent(test_I, mode_order , Uref.EL , dimensions)
    file2=open(os.path.join( ResultsDir_Order_Dependent,'plot_dK_I_%s' % suffix),'w') 
    for t in range(dimensions.time_len-1):
        file2.write('%30.20E   ' % test_I.time[t+1])
        file2.write('%30.20E   ' % dKI_tild_I[t])
        file2.write('%30.20E   ' % dKII_tild_I[t])
        file2.write('%30.20E   ' % dKIII_tild_I[t])
        file2.write(' \n' )
    file2.close()
    ##### Mode II
    dUx_PL_II, dUy_PL_II, dUz_PL_II, dKI_tild_II, dKII_tild_II, dKIII_tild_II = Plastic_Field_Order_Dependent(test_II, mode_order , Uref.EL , dimensions)
    file2=open(os.path.join( ResultsDir_Order_Dependent,'plot_dK_II_%s' % suffix),'w') 
    for t in range(dimensions.time_len-1):
        file2.write('%30.20E   ' % test_II.time[t+1])
        file2.write('%30.20E   ' % dKI_tild_II[t])
        file2.write('%30.20E   ' % dKII_tild_II[t])
        file2.write('%30.20E   ' % dKIII_tild_II[t])
        file2.write(' \n' )
    file2.close()
    ##### Mode III
    dUx_PL_III, dUy_PL_III, dUz_PL_III, dKI_tild_III, dKII_tild_III, dKIII_tild_III = Plastic_Field_Order_Dependent(test_III, mode_order , Uref.EL , dimensions)
    file2=open(os.path.join( ResultsDir_Order_Dependent,'plot_dK_III_%s' % suffix),'w') 
    for t in range(dimensions.time_len-1):
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
    file2=open(os.path.join( ResultsDir_Order_Dependent,'Pastic_Field_%s_%s.p' % (mode_order_suffix, suffix ) ),'wb')
    pickle.dump(Order, file2)
    file2.close()

'''

'''

#-------------------------------------------------------------------------------------------------
#                               Plastic field of Mode I test
#-------------------------------------------------------------------------------------------------

#Ux_PL_I, Uy_PL_I, Uz_PL_I, KI_tild_I, KII_tild_I, KIII_tild_I = Plastic_Field(test_I, Uref.EL , dimensions)


dUx_PL_I, dUy_PL_I, dUz_PL_I, dUx_I_II_III, dUy_I_II_III, dUz_I_II_III, dKI_tild_I, dKII_tild_I, dKIII_tild_I = Plastic_Field_Order_Dependent(test_I, ['I','II','III'] , Uref.EL , dimensions)


print 'dKI_tild_I:  ', dKI_tild_I
print 'dKII_tild_I: ', dKII_tild_I
print 'dKIII_tild_I:', dKIII_tild_I

file2=open(os.path.join( ResultsDir,'plot_dK_I_%s' % suffix),'w') 
for t in range(dimensions.time_len-1):
    file2.write('%30.20E   ' % test_I.time[t+1])
    file2.write('%30.20E   ' % dKI_tild_I[t])
    file2.write('%30.20E   ' % dKII_tild_I[t])
    file2.write('%30.20E   ' % dKIII_tild_I[t])
    file2.write(' \n' )

file2.close()


#-------------------------------------------------------------------------------------------------
#                               Plastic field of Mode II test
#-------------------------------------------------------------------------------------------------

#Ux_PL_II, Uy_PL_II, Uz_PL_II, KI_tild_II, KII_tild_II, KIII_tild_II = Plastic_Field(test_II , Uref.EL , dimensions)

dUx_PL_II, dUy_PL_II, dUz_PL_II, dUx_I_II_III, dUy_I_II_III, dUz_I_II_III, dKI_tild_II, dKII_tild_II, dKIII_tild_II = Plastic_Field_Order_Dependent(test_II, ['I','II','III'] , Uref.EL , dimensions)


print 'dKI_tild_II:  ', dKI_tild_II
print 'dKII_tild_II: ', dKII_tild_II
print 'dKIII_tild_II:', dKIII_tild_II

file2=open(os.path.join( ResultsDir,'plot_dK_II_%s' % suffix),'w') 
for t in range(dimensions.time_len-1):
    file2.write('%30.20E   ' % test_II.time[t+1])
    file2.write('%30.20E   ' % dKI_tild_II[t])
    file2.write('%30.20E   ' % dKII_tild_II[t])
    file2.write('%30.20E   ' % dKIII_tild_II[t])
    file2.write(' \n' )

file2.close()


#-------------------------------------------------------------------------------------------------
#                               Plastic field of Mode III test
#-------------------------------------------------------------------------------------------------

#Ux_PL_III, Uy_PL_III, Uz_PL_III, KI_tild_III, KII_tild_III, KIII_tild_III = Plastic_Field(test_III, Uref.EL , dimensions)

dUx_PL_III, dUy_PL_III, dUz_PL_III, dUx_I_II_III, dUy_I_II_III, dUz_I_II_III, dKI_tild_III, dKII_tild_III, dKIII_tild_III = Plastic_Field_Order_Dependent(test_III, ['I','II','III'] , Uref.EL , dimensions)

print 'dKI_tild_III:  ', dKI_tild_III
print 'dKII_tild_III: ', dKII_tild_III
print 'dKIII_tild_III:', dKIII_tild_III

file2=open(os.path.join( ResultsDir,'plot_dK_III_%s' % suffix),'w') 
for t in range(dimensions.time_len-1):
    file2.write('%30.20E   ' % test_III.time[t+1])
    file2.write('%30.20E   ' % dKI_tild_III[t])
    file2.write('%30.20E   ' % dKII_tild_III[t])
    file2.write('%30.20E   ' % dKIII_tild_III[t])
    file2.write(' \n' )

file2.close()


#-------------------------------------------------------------------------------------------------
#                         Explore different loading ranges
#-------------------------------------------------------------------------------------------------

KI_FL = np.linspace( 0., Job.I.PL.MonKI_range[0], int(dimensions.time_len/2)+1 )                               # First Loading
KI_FU = np.linspace( Job.I.PL.MonKI_range[0], int(Job.I.PL.MonKI_range[1]), int(dimensions.time_len/2)+1 )     # First Unloading
KI_nom = np.concatenate((KI_FL, KI_FU[1:] ))

KII_FL = np.linspace( 0., Job.II.PL.MonKII_range[0], int(dimensions.time_len/2)+1 )                               # First Loading
KII_FU = np.linspace( Job.II.PL.MonKII_range[0], int(Job.II.PL.MonKII_range[1]), int(dimensions.time_len/2)+1 )     # First Unloading
KII_nom = np.concatenate((KII_FL, KII_FU[1:] ))

KIII_FL = np.linspace( 0., Job.III.PL.MonKIII_range[0], int(dimensions.time_len/2)+1 )                               # First Loading
KIII_FU = np.linspace( Job.III.PL.MonKIII_range[0], int(Job.III.PL.MonKIII_range[1]), int(dimensions.time_len/2)+1 )     # First Unloading
KIII_nom = np.concatenate((KIII_FL, KIII_FU[1:] ))

KI_I_range     = [ round(KI_nom[i+1]  ,2) for i in range(len(dKI_tild_I)) ]
KII_II_range   = [ round(KII_nom[i+1] ,2) for i in range(len(dKII_tild_II)) ] 
KIII_III_range = [ round(KIII_nom[i+1],2) for i in range(len(dKIII_tild_III)) ] 

l    = len(KI_I_range)
half = l/2 - 1

list_ranges = [[ 0, half],[ half-30, half-10], [ half-20, half], [ half-10, half], 
                [ half, half+10], [ half, half+20],[ half+10, half+30], [ half, l-1], 
                [ half-5, half+5 ], [ half-10, half+10 ],[ half-15, half+15 ],
                [ half-20, half+20 ], [ half-25, half+25 ], [ half-30, half+30 ],
                [ half-40, half+40 ], [ half-50, half+50 ], [ half-60, half+60 ],
                [ half-70, half+70 ], [ half-80, half+80 ], [ half-90, half+90 ] ]

Plastic_Field_Extraction = 'With_POD'

#---------
# Mode I
#---------

list_KI_ranges = list_ranges

for couple in list_KI_ranges:
    KI_I_min = KI_I_range[couple[0]]
    KI_I_max = KI_I_range[couple[1]]    
    len_I_min = couple[0]
    len_I_max = couple[1]
    if Plastic_Field_Extraction == 'With_POD' :
        time_I_red = [ test_I.time[i]  for i in range(len_I_min, len_I_max+1) ]
        dUx_PL_I_red = np.transpose( [ np.transpose(dUx_PL_I)[i] for i in range(len_I_min, len_I_max) ])  #  to obtain only a reduced field from the requested loading range
        dUy_PL_I_red = np.transpose( [ np.transpose(dUy_PL_I)[i] for i in range(len_I_min, len_I_max) ])
        dUz_PL_I_red = np.transpose( [ np.transpose(dUz_PL_I)[i] for i in range(len_I_min, len_I_max) ])
        #Ux_PL_ref_I, Uy_PL_ref_I, Uz_PL_ref_I, dRhoI_I = POD_PL(dUx_PL_I_red, dUy_PL_I_red, dUz_PL_I_red)
        Ux_PL_ref_I, Uy_PL_ref_I, Uz_PL_ref_I, dRhoI_I = SVD_PL(dUx_PL_I_red, dUy_PL_I_red, dUz_PL_I_red)     
        file2=open(os.path.join( ResultsDir,'plot_dRho_I_Krange_[%3.2f_%3.2f]_%s' % ( KI_I_min, KI_I_max, suffix) ),'w') 
        for t in range(len(time_I_red)-1):
            file2.write('%30.20E   ' % test_I.time[t+1])  
            file2.write('%30.20E   ' % dRhoI_I[t])
            file2.write(' \n' )
        file2.close()
    elif Plastic_Field_Extraction == 'Without_POD' :
        time_I_red = [ test_I.time[i]  for i in range(len_I_min, len_I_max+1) ]
        Ux_PL_ref_I = [sum(dUx_PL_I[i][len_I_min:len_I_max]) for i in range(dimensions.listN_F_len)]
        Uy_PL_ref_I = [sum(dUy_PL_I[i][len_I_min:len_I_max]) for i in range(dimensions.listN_F_len)]
        Uz_PL_ref_I = [sum(dUz_PL_I[i][len_I_min:len_I_max]) for i in range(dimensions.listN_F_len)]
    file2=open(os.path.join( ResultsDir,'plot_U_PL_ref_I_Krange_[%3.2f_%3.2f]_%s' % ( KI_I_min, KI_I_max, suffix )),'w') 
    for p in range(dimensions.listN_F_len):
        file2.write('%30.20E   ' % Ux_PL_ref_I[p]) 
        file2.write('%30.20E   ' % Uy_PL_ref_I[p])
        file2.write('%30.20E   ' % Uz_PL_ref_I[p])
        file2.write(' \n' )         
    file2.close()
    Norme_PL_I = pow(np.linalg.norm(Ux_PL_ref_I), 2) + pow(np.linalg.norm(Uy_PL_ref_I), 2) + pow(np.linalg.norm(Uz_PL_ref_I), 2)
    Uref.PL.I.x = Ux_PL_ref_I
    Uref.PL.I.y = Uy_PL_ref_I
    Uref.PL.I.z = Uz_PL_ref_I
    Uref.PL.I.norme = Norme_PL_I
    Uref.PL.I.f_r , Uref.PL.I.g_theta_x , Uref.PL.I.g_theta_y, Uref.PL.I.g_theta_z  = POD_r_theta(Uref.PL.I.x , Uref.PL.I.y , Uref.PL.I.z , 'Mode I' , dimensions)
    file2=open(os.path.join( ResultsDir,'plot_f_r_PL_I_Krange_[%3.2f_%3.2f]_%s' % ( KI_I_min, KI_I_max, suffix)),'w') 
    for p in range(dimensions.rad_len): 
        file2.write('%30.20E'    % dimensions.radial[p])
        file2.write('%30.20E   ' % Uref.PL.I.f_r[p])
        file2.write(' \n' )
    file2.close()
    file2=open(os.path.join( ResultsDir,'plot_g_theta_PL_I_Krange_[%3.2f_%3.2f]_%s' % ( KI_I_min, KI_I_max, suffix)),'w')
    theta= -Pi
    for p in range(dimensions.thet_len):
        file2.write('%30.20E   ' % theta)
        file2.write('%30.20E   ' % Uref.PL.I.g_theta_x[p])
        file2.write('%30.20E   ' % Uref.PL.I.g_theta_y[p])
        file2.write('%30.20E   ' % Uref.PL.I.g_theta_z[p])
        file2.write(' \n' )
        theta += 2*Pi/(dimensions.thet_len-1)
    file2.close()

file2=open(os.path.join( ResultsDir,'plot_KI_I_list_ranges_%d_%s' % ( Job.I.PL.MonKI_range[-1], suffix)),'w')
for couple in list_KI_ranges : 
    file2.write('% 3.2f ' % KI_I_range[couple[0]])
    file2.write('% 3.2f'  % KI_I_range[couple[1]])
    file2.write(' \n' )

file2.close()



#---------
# Mode II
#---------

list_KII_ranges = list_ranges

for couple in list_KII_ranges:
    KII_II_min = KII_II_range[couple[0]]
    KII_II_max = KII_II_range[couple[1]]    
    len_II_min = couple[0]
    len_II_max = couple[1]
    if Plastic_Field_Extraction == 'With_POD' :
        time_II_red = [ test_II.time[i]  for i in range(len_II_min, len_II_max+1) ]
        dUx_PL_II_red = np.transpose( [ np.transpose(dUx_PL_II)[i] for i in range(len_II_min, len_II_max) ])  #  to obtain only a reduced field from the requested loading range
        dUy_PL_II_red = np.transpose( [ np.transpose(dUy_PL_II)[i] for i in range(len_II_min, len_II_max) ])
        dUz_PL_II_red = np.transpose( [ np.transpose(dUz_PL_II)[i] for i in range(len_II_min, len_II_max) ])
        #Ux_PL_ref_II, Uy_PL_ref_II, Uz_PL_ref_II, dRhoII_II = POD_PL(dUx_PL_II_red, dUy_PL_II_red, dUz_PL_II_red)     
        Ux_PL_ref_II, Uy_PL_ref_II, Uz_PL_ref_II, dRhoII_II = SVD_PL(dUx_PL_II_red, dUy_PL_II_red, dUz_PL_II_red)     
        file2=open(os.path.join( ResultsDir,'plot_dRho_II_Krange_[%3.2f_%3.2f]_%s' % ( KII_II_min, KII_II_max, suffix) ),'w') 
        for t in range(len(time_II_red)-1):
            file2.write('%30.20E   ' % test_II.time[t+1])  
            file2.write('%30.20E   ' % dRhoII_II[t])
            file2.write(' \n' )
        file2.close()
    elif Plastic_Field_Extraction == 'Without_POD' :
        time_II_red = [ test_II.time[i]  for i in range(len_II_min, len_II_max+1) ]
        Ux_PL_ref_II = [sum(dUx_PL_II[i][len_II_min:len_II_max]) for i in range(dimensions.listN_F_len)]
        Uy_PL_ref_II = [sum(dUy_PL_II[i][len_II_min:len_II_max]) for i in range(dimensions.listN_F_len)]
        Uz_PL_ref_II = [sum(dUz_PL_II[i][len_II_min:len_II_max]) for i in range(dimensions.listN_F_len)]
    file2=open(os.path.join( ResultsDir,'plot_U_PL_ref_II_Krange_[%3.2f_%3.2f]_%s' % ( KII_II_min, KII_II_max, suffix )),'w') 
    for p in range(dimensions.listN_F_len):
        file2.write('%30.20E   ' % Ux_PL_ref_II[p]) 
        file2.write('%30.20E   ' % Uy_PL_ref_II[p])
        file2.write('%30.20E   ' % Uz_PL_ref_II[p])
        file2.write(' \n' )         
    file2.close()
    Norme_PL_II = pow(np.linalg.norm(Ux_PL_ref_II), 2) + pow(np.linalg.norm(Uy_PL_ref_II), 2) + pow(np.linalg.norm(Uz_PL_ref_II), 2)
    Uref.PL.II.x = Ux_PL_ref_II
    Uref.PL.II.y = Uy_PL_ref_II
    Uref.PL.II.z = Uz_PL_ref_II
    Uref.PL.II.norme = Norme_PL_II
    Uref.PL.II.f_r , Uref.PL.II.g_theta_x , Uref.PL.II.g_theta_y, Uref.PL.II.g_theta_z  = POD_r_theta(Uref.PL.II.x , Uref.PL.II.y , Uref.PL.II.z , 'Mode II' , dimensions)
    file2=open(os.path.join( ResultsDir,'plot_f_r_PL_II_Krange_[%3.2f_%3.2f]_%s' % ( KII_II_min, KII_II_max, suffix)),'w') 
    for p in range(dimensions.rad_len): 
        file2.write('%30.20E'    % dimensions.radial[p])
        file2.write('%30.20E   ' % Uref.PL.II.f_r[p])
        file2.write(' \n' )
    file2.close()
    file2=open(os.path.join( ResultsDir,'plot_g_theta_PL_II_Krange_[%3.2f_%3.2f]_%s' % ( KII_II_min, KII_II_max, suffix)),'w')
    theta= -Pi
    for p in range(dimensions.thet_len):
        file2.write('%30.20E   ' % theta)
        file2.write('%30.20E   ' % Uref.PL.II.g_theta_x[p])
        file2.write('%30.20E   ' % Uref.PL.II.g_theta_y[p])
        file2.write('%30.20E   ' % Uref.PL.II.g_theta_z[p])
        file2.write(' \n' )
        theta += 2*Pi/(dimensions.thet_len-1)
    file2.close()

file2=open(os.path.join( ResultsDir,'plot_KII_II_list_ranges_%d_%s' % ( Job.II.PL.MonKII_range[-1], suffix)),'w')
for couple in list_KII_ranges :
    file2.write('% 3.2f ' % KII_II_range[couple[0]])
    file2.write('% 3.2f' % KII_II_range[couple[1]])
    file2.write(' \n' )

file2.close()

#---------
# Mode III
#---------

list_KIII_ranges = list_ranges

for couple in list_KIII_ranges:
    KIII_III_min = KIII_III_range[couple[0]]
    KIII_III_max = KIII_III_range[couple[1]]    
    len_III_min = couple[0]
    len_III_max = couple[1]
    if Plastic_Field_Extraction == 'With_POD' :
        time_III_red = [ test_III.time[i]  for i in range(len_III_min, len_III_max+1) ]
        dUx_PL_III_red = np.transpose( [ np.transpose(dUx_PL_III)[i] for i in range(len_III_min, len_III_max) ])  #  to obtain only a reduced field from the requested loading range
        dUy_PL_III_red = np.transpose( [ np.transpose(dUy_PL_III)[i] for i in range(len_III_min, len_III_max) ])
        dUz_PL_III_red = np.transpose( [ np.transpose(dUz_PL_III)[i] for i in range(len_III_min, len_III_max) ])
        #Ux_PL_ref_III, Uy_PL_ref_III, Uz_PL_ref_III, dRhoIII_III = POD_PL(dUx_PL_III_red, dUy_PL_III_red, dUz_PL_III_red)
        Ux_PL_ref_III, Uy_PL_ref_III, Uz_PL_ref_III, dRhoIII_III = SVD_PL(dUx_PL_III_red, dUy_PL_III_red, dUz_PL_III_red)     
        file2=open(os.path.join( ResultsDir,'plot_dRho_III_Krange_[%3.2f_%3.2f]_%s' % ( KIII_III_min, KIII_III_max, suffix) ),'w') 
        for t in range(len(time_III_red)-1):
            file2.write('%30.20E   ' % test_III.time[t+1])  
            file2.write('%30.20E   ' % dRhoIII_III[t])
            file2.write(' \n' )
        file2.close()
    elif Plastic_Field_Extraction == 'Without_POD' :
        time_III_red = [ test_III.time[i]  for i in range(len_III_min, len_III_max+1) ]
        Ux_PL_ref_III = [sum(dUx_PL_III[i][len_III_min:len_III_max]) for i in range(dimensions.listN_F_len)]
        Uy_PL_ref_III = [sum(dUy_PL_III[i][len_III_min:len_III_max]) for i in range(dimensions.listN_F_len)]
        Uz_PL_ref_III = [sum(dUz_PL_III[i][len_III_min:len_III_max]) for i in range(dimensions.listN_F_len)]
    file2=open(os.path.join( ResultsDir,'plot_U_PL_ref_III_Krange_[%3.2f_%3.2f]_%s' % ( KIII_III_min, KIII_III_max, suffix )),'w') 
    for p in range(dimensions.listN_F_len):
        file2.write('%30.20E   ' % Ux_PL_ref_III[p]) 
        file2.write('%30.20E   ' % Uy_PL_ref_III[p])
        file2.write('%30.20E   ' % Uz_PL_ref_III[p])
        file2.write(' \n' )         
    file2.close()
    Norme_PL_III = pow(np.linalg.norm(Ux_PL_ref_III), 2) + pow(np.linalg.norm(Uy_PL_ref_III), 2) + pow(np.linalg.norm(Uz_PL_ref_III), 2)
    Uref.PL.III.x = Ux_PL_ref_III
    Uref.PL.III.y = Uy_PL_ref_III
    Uref.PL.III.z = Uz_PL_ref_III
    Uref.PL.III.norme = Norme_PL_III
    Uref.PL.III.f_r , Uref.PL.III.g_theta_x , Uref.PL.III.g_theta_y, Uref.PL.III.g_theta_z  = POD_r_theta(Uref.PL.III.x , Uref.PL.III.y , Uref.PL.III.z , 'Mode III' , dimensions)
    file2=open(os.path.join( ResultsDir,'plot_f_r_PL_III_Krange_[%3.2f_%3.2f]_%s' % ( KIII_III_min, KIII_III_max, suffix)),'w') 
    for p in range(dimensions.rad_len): 
        file2.write('%30.20E'    % dimensions.radial[p])
        file2.write('%30.20E   ' % Uref.PL.III.f_r[p])
        file2.write(' \n' )
    file2.close()
    file2=open(os.path.join( ResultsDir,'plot_g_theta_PL_III_Krange_[%3.2f_%3.2f]_%s' % ( KIII_III_min, KIII_III_max, suffix)),'w')
    theta= -Pi
    for p in range(dimensions.thet_len):  
        file2.write('%30.20E   ' % theta)   
        file2.write('%30.20E   ' % Uref.PL.III.g_theta_x[p]) 
        file2.write('%30.20E   ' % Uref.PL.III.g_theta_y[p])        
        file2.write('%30.20E   ' % Uref.PL.III.g_theta_z[p])        
        file2.write(' \n' )  
        theta += 2*Pi/(dimensions.thet_len-1)
    file2.close()

file2=open(os.path.join( ResultsDir,'plot_KIII_III_list_ranges_%d_%s' % ( Job.III.PL.MonKIII_range[-1], suffix)),'w')
for couple in list_KIII_ranges : 
    file2.write('% 3.2f ' % KIII_III_range[couple[0]])
    file2.write('% 3.2f' % KIII_III_range[couple[1]])
    file2.write(' \n' )

file2.close()
'''


'''
file2=open(os.path.join( ResultsDir,'Dimensions.p' ),'wb')
pickle.dump(dim, file2)
file2.close()
'''
#-------------------------------------------------------------------------------------------------
#                               Total filed extraction   Mixed Mode
#-------------------------------------------------------------------------------------------------

test_Mix = Container()

test_Mix.JobName = Job.Mix.PL.MonName  + '.odb'

odb=openOdb(path=os.path.join(odbSrcLGEOM, test_Mix.JobName ))

Ux_tot   =[]
Uy_tot   =[]
Uz_tot   =[]
time_tot =[]

for i in range(1,3):
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

file2=open(os.path.join( ResultsDir,'Test_Mix_%s.p' %  suffix ),'wb')
pickle.dump(test_Mix, file2)
file2.close()
