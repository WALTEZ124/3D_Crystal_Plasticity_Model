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
odbSrcSlip = os.path.join( odbSrc, 'all_slip_systems')



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

ResultsDir_Slip = os.path.join(ResultsDir, 'all_slip_systems')
if not os.path.exists(ResultsDir_Slip):
    os.makedirs(ResultsDir_Slip)


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

print 'Number of chosen nodes in the interest zone =', dimensions.listN_F_len
print 'number of radial nodes                      =', dimensions.rad_len
print 'number of angular nodes                     = ', dimensions.thet_len
print 'number of thickness nodes                   = ', dimensions.z_len

dimensions.radial = [ dimensions.listN_F_z_rad_ang[r*dimensions.thet_len][1]  for r in range(dimensions.rad_len)]

#-------------------------------------------------------------------------------------------------
#                               Total field extraction   Mode I
#-------------------------------------------------------------------------------------------------

n_act_steps = 1

os.system('echo all slip systems mode I:')

test_I = Container()

test_I.JobName = Job.I.PL.MonName  + '_all_slip_systems.odb'

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
dimensions.time_len = len(test_I.time)

os.system('echo all slip systems mode I: Displacement successfully extracted')

time, EVCum_moy, EVCum_quad = Extract_All_Cumulated_Strain_Field_Output(odb,'Step-1', dimensions)

odb.close()

os.system('echo all slip systems mode I: EV Cumulated successfully extracted')


file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_moy_%s_all_slip_systems' % ( Job.I.PL.MonName  ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_moy[t][s])
    
    file2.write(' \n' )

file2.close() 

file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_quad_%s_all_slip_systems' % ( Job.I.PL.MonName  ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_quad[t][s])
    
    file2.write(' \n' )

file2.close() 


#-------------------------------------------------------------------------------------------------
#                               Total field extraction   Mode II
#-------------------------------------------------------------------------------------------------
os.system('echo all slip systems mode II:')

test_II = Container()

test_II.JobName = Job.II.PL.MonName  + '_all_slip_systems.odb'

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

os.system('echo all slip systems mode II: Displacement successfully extracted')

time, EVCum_moy, EVCum_quad = Extract_All_Cumulated_Strain_Field_Output(odb,'Step-1', dimensions)

odb.close()

os.system('echo all slip systems mode II: EV Cumulated successfully extracted')


file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_moy_%s_all_slip_systems' % ( Job.II.PL.MonName ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_moy[t][s])
    
    file2.write(' \n' )

file2.close() 

file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_quad_%s_all_slip_systems' % ( Job.II.PL.MonName ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_quad[t][s])
    
    file2.write(' \n' )

file2.close() 


#-------------------------------------------------------------------------------------------------
#                               Total field extraction   Mode III
#-------------------------------------------------------------------------------------------------

os.system('echo all slip systems mode III: ')

test_III = Container()

test_III.JobName = Job.III.PL.MonName  + '_all_slip_systems.odb'

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

os.system('echo all slip systems mode III: Displacement successfully extracted')

time, EVCum_moy, EVCum_quad = Extract_All_Cumulated_Strain_Field_Output(odb,'Step-1', dimensions)

odb.close()

os.system('echo all slip systems mode III: EV Cumulated successfully extracted')


file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_moy_%s_all_slip_systems' % ( Job.III.PL.MonName ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_moy[t][s])
    
    file2.write(' \n' )

file2.close() 

file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_quad_%s_all_slip_systems' % ( Job.III.PL.MonName  ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_quad[t][s])
    
    file2.write(' \n' )

file2.close() 



#-------------------------------------------------------------------------------------------------
#                               Total filed extraction   Mixed Mode
#-------------------------------------------------------------------------------------------------

os.system('echo all slip systems mode Mix:')

test_Mix = Container()

test_Mix.JobName = Job.Mix.PL.MonName  + '_all_slip_systems.odb'

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

os.system('echo all slip systems mode Mix: Displacement successfully extracted')

time, EVCum_moy, EVCum_quad = Extract_All_Cumulated_Strain_Field_Output(odb,'Step-1', dimensions)

odb.close()

os.system('echo all slip systems mode Mix: EV Cumulated successfully extracted')


file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_moy_%s_all_slip_systems' % ( Job.Mix.PL.MonName ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_moy[t][s])
    
    file2.write(' \n' )

file2.close() 

file2=open(os.path.join( ResultsDir_Slip,'EV_Cum_quad_%s_all_slip_systems' % ( Job.Mix.PL.MonName  ) ),'w') 
file2.write('time ,  EVCum1 , EVCum2, EVCum3, EVCum4, EVCum5, EVCum6, EVCum7, EVCum8, EVCum9, EVCum10, EVCum11, EVCum12')
file2.write(' \n' )
for t in range(len(time)):
    file2.write('%30.20E   ' % time[t])
    for s in range(12):
        file2.write('%30.20E   ' % EVCum_quad[t][s])
    
    file2.write(' \n' )

file2.close() 


test_Mix.MonKI_range   = Job.Mix.PL.MonKI_range  
test_Mix.MonKII_range  = Job.Mix.PL.MonKII_range
test_Mix.MonKIII_range = Job.Mix.PL.MonKIII_range

#-------------------------------------------------------------------------------------------------
#                         Save total fields
#-------------------------------------------------------------------------------------------------

file2=open(os.path.join( ResultsDir_Slip,'Test_I_%s_all_slip_systems.p' %  suffix ),'wb')
pickle.dump(test_I, file2)
file2.close()

file2=open(os.path.join( ResultsDir_Slip,'Test_II_%s_all_slip_systems.p' %  suffix ),'wb')
pickle.dump(test_II, file2)
file2.close()

file2=open(os.path.join( ResultsDir_Slip,'Test_III_%s_all_slip_systems.p' %  suffix ),'wb')
pickle.dump(test_III, file2)
file2.close()

file2=open(os.path.join( ResultsDir_Slip,'Test_Mix_%s_all_slip_systems.p' %  suffix ),'wb')
pickle.dump(test_Mix, file2)
file2.close()


