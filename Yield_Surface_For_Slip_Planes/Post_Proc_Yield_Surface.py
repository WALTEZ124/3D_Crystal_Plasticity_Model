
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

class Container(object):
    def __init__(self):
        pass

codeSrc = '.'
execfile(os.path.join(codeSrc,'Input_Computation.py'))  

elastic = Elastic( eType = elasticity_type)

Shkl = "%d%d%d" % (elastic.hkl[0],elastic.hkl[1],elastic.hkl[2])
Suvw = "%d%d%d" % (elastic.uvw[0],elastic.uvw[1],elastic.uvw[2])
suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)

PostProcSrc = os.path.join(codeSrc,'src_Post_Proc')

Extracted_Nodes = False 

#slip_systems_list = ['b4','b2','b5','d4','d1','d6','a2','a6','a3','c5','c3','c1']

slip_systems_list = ['b2','c1']

modes_plane_list=['I_II', 'I_III', 'II_III']

mode_order = 'order_I_II_III'

for slip_suffix in slip_systems_list :
    odbSrc = os.path.join('..', slip_suffix)
    #-------------------------------------------------------------------------------
    #    Import Reference fields
    #-------------------------------------------------------------------------------
    Uref_PL = Container()
    file2=open(os.path.join( codeSrc, 'src_Reference_Fields', 'Uref_PL_I_%s_%s_%s_prot2.p' % (mode_order, suffix, slip_suffix ) ),'rb')
    Uref_PL.I = pickle.load(file2 )
    file2.close()
    file2=open(os.path.join( codeSrc, 'src_Reference_Fields', 'Uref_PL_II_%s_%s_%s_prot2.p' % (mode_order, suffix, slip_suffix) ),'rb')
    Uref_PL.II = pickle.load(file2)
    file2.close()
    file2=open(os.path.join( codeSrc, 'src_Reference_Fields', 'Uref_PL_III_%s_%s_%s_prot2.p' % (mode_order, suffix, slip_suffix) ),'rb')
    Uref_PL.III = pickle.load(file2)
    file2.close()
    rad_min, rad_max = Uref_PL.I.Extraction_zone
    file2=open(os.path.join( codeSrc, 'src_Reference_Fields' , 'Uref_EL_%s.p' % suffix ), 'rb' )
    Uref = pickle.load(file2 )
    file2.close() 
    Uref_EL = Uref.EL
    os.system('echo slip system %s : reference fields successfully imported' % (slip_suffix ) )
    #-------------------------------------------------------------------------------
    #    Start fields extraction and projection
    #-------------------------------------------------------------------------------
    for modes_plane in modes_plane_list :
        ResultsDir = os.path.join( 'Results',slip_suffix, modes_plane )
        if not os.path.exists(ResultsDir):
            os.makedirs(ResultsDir)
        JobList = loadtxt(os.path.join(odbSrc , 'Star_job_details_%s' % modes_plane) , unpack = True )
        for j, JobName in enumerate(JobList) :  
            if j == 0 :
                ### Initial star loading
                NewJobName = JobName + '.odb'                 
                NameSuffix = JobName.replace('EP_', '')
                range_act_steps = range(1,3)
                odb=openOdb(path=os.path.join(odbSrc, NewJobName) )
                if Extracted_Nodes == False :
                    dimensions.listN_TIP, dimensions.listN_F_unsorted, dimensions.listN_F_sorted, dimensions.listN_F_z_x_y, dimensions.listN_F_z_rad_ang =  Extract_Nodes_History_Output(odb)
                    dimensions.listN_F_len = len(dimensions.listN_F_sorted)
                    print 'Number of chosen nodes in the interest zone =', dimensions.listN_F_len
                    print 'number of radial nodes                      =', dimensions.rad_len
                    print 'number of angular nodes                     = ', dimensions.thet_len
                    print 'number of thickness nodes                   = ', dimensions.z_len
                    dimensions.radial = [ dimensions.listN_F_z_rad_ang[r*dimensions.thet_len][1]  for r in range(dimensions.rad_len)]
                    Extracted_Nodes = True 
                else :
                    pass
            else :
                ### Secondary star loading
                NewJobName = JobName + '_%s.odb' % slip_suffix
                NameSuffix = JobName.replace('EP_', '')
                NameSuffix += '_%s' % slip_suffix
                range_act_steps = range(3,4)
                odb=openOdb(path=os.path.join(odbSrc, NewJobName) )
            Ux_tot, Uy_tot, Uz_tot, time_tot, Gamma_tot, Gamma_moy, Gamma_quad, EV1_Cum_tot, EV1_Cum_moy, EV1_Cum_quad = [], [], [], [], [], [], [], [], [], []
            for i in range_act_steps :
                step = 'Step-%d' %i
                time_tmp, Ux_tot_tmp, Uy_tot_tmp, Uz_tot_tmp = Extract_Total_Disp_History_Output(odb,step, dimensions)
                os.system('echo slip system %s modes plane %s : displacement of %s of %s successfully extracted' % (slip_suffix, modes_plane, step, NameSuffix ) )
                time_tmp , EV1_Cum_tot_tmp, EV1_Cum_moy_tmp, EV1_Cum_quad_tmp, Gamma_tot_tmp, Gamma_moy_tmp, Gamma_quad_tmp = Extract_Strain_Field_Output(odb, step , dimensions)
                os.system('echo slip system %s modes plane %s : EV1 cumulated of %s of %s successfully extracted' % (slip_suffix, modes_plane, step, NameSuffix ) )
                if i == 1 :
                    Ux_tot   = np.transpose(Ux_tot_tmp)
                    Uy_tot   = np.transpose(Uy_tot_tmp)
                    Uz_tot   = np.transpose(Uz_tot_tmp)
                    time_tot = time_tmp
                    EV1_Cum_moy = EV1_Cum_moy_tmp
                    EV1_Cum_quad= EV1_Cum_quad_tmp
                    Gamma_moy   = Gamma_moy_tmp
                    Gamma_quad  = Gamma_quad_tmp
                    EV1_Cum_tot = np.transpose(EV1_Cum_tot_tmp)
                    Gamma_tot   = np.transpose(Gamma_tot_tmp)
                else :
                    time_tmp.pop(0)
                    EV1_Cum_moy_tmp.pop(0)
                    EV1_Cum_quad_tmp.pop(0)
                    time_tmp = [ x + time_tot[-1] for x in time_tmp]
                    time_tot     += time_tmp
                    EV1_Cum_moy  += EV1_Cum_moy_tmp
                    EV1_Cum_quad += EV1_Cum_quad_tmp
                    Gamma_moy    += Gamma_moy_tmp
                    Gamma_quad   += Gamma_quad_tmp
                    Ux_tot = np.concatenate((Ux_tot, np.transpose(Ux_tot_tmp)))
                    Uy_tot = np.concatenate((Uy_tot, np.transpose(Uy_tot_tmp)))
                    Uz_tot = np.concatenate((Uz_tot, np.transpose(Uz_tot_tmp)))
                    EV1_Cum_tot = np.concatenate((EV1_Cum_tot, np.transpose(EV1_Cum_tot_tmp)))
                    Gamma_tot   = np.concatenate((Gamma_tot, np.transpose(Gamma_tot_tmp)))
                del time_tmp, Ux_tot_tmp, Uy_tot_tmp, Uz_tot_tmp, EV1_Cum_moy_tmp, EV1_Cum_quad_tmp, Gamma_moy_tmp, Gamma_quad_tmp
            odb.close()
            test = Container()
            test.time = time_tot
            test.dUx_tot = np.transpose(Ux_tot)
            test.dUy_tot = np.transpose(Uy_tot)
            test.dUz_tot = np.transpose(Uz_tot)
            test.EV1_Cum_moy  = EV1_Cum_moy
            test.EV1_Cum_quad = EV1_Cum_quad
            test.EV1_Cum_tot = np.transpose(EV1_Cum_tot)
            test.Gamma_moy   = Gamma_moy
            test.Gamma_quad  = Gamma_quad
            test.Gamma_tot   = np.transpose(Gamma_tot)
            del time_tot, Ux_tot, Uy_tot, Uz_tot , Gamma_tot, Gamma_moy, Gamma_quad, EV1_Cum_tot, EV1_Cum_moy, EV1_Cum_quad
            dimensions.time_len = len(test.time)
            file2=open(os.path.join( ResultsDir,'EV1_Cum_moy_%s' % ( NameSuffix ) ),'w')
            file2.write('time ,  EV1 Cum arithmetic mean, EV1 Cum quadratic mean, Gamma moy, Gamma quad' )
            file2.write(' \n' )
            for t in range(len(test.time)):
                file2.write('%30.20E   ' % test.time[t] )
                file2.write('%30.20E   ' % test.EV1_Cum_moy[t] )
                file2.write('%30.20E   ' % test.EV1_Cum_quad[t] )
                file2.write('%30.20E   ' % test.Gamma_moy[t] )
                file2.write('%30.20E   ' % test.Gamma_quad[t] )
                file2.write(' \n')
            file2.close()
            test.dKI_tild, test.dKII_tild, test.dKIII_tild, test.dRhoI, test.dRhoII, test.dRhoIII = Projection_reduced_zone_Order_Dependent(test, mode_order_list, Uref_EL, Uref_PL)
            os.system('echo slip system %s modes plane %s : %s successfully projected on reference fields' % (slip_suffix, modes_plane, NameSuffix ) )
            file2=open(os.path.join( ResultsDir,'dK_dRho_%s' %( NameSuffix ) ) ,'w') 
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
            #                          Reconstruct fields
            #-------------------------------------------------------------------------------------------------
            test.CeR_tmp, test.CcR_tmp, test.Plastic_ratio = Reconstruct_Fields( test , Uref_EL, Uref_PL )
            os.system('echo slip system %s modes plane %s : %s successfully reconstructed' % (slip_suffix, modes_plane, NameSuffix ) )
            file2=open(os.path.join( ResultsDir,'Errors_%s' %( NameSuffix ) ) ,'w')
            file2.write('time ,     CeR_tmp,      CcR_tmp,    Plastic_ratio')
            file2.write(' \n' )
            for t in range(len(test.time)-1):
                file2.write('%30.20E   ' % test.time[t+1])
                file2.write('%30.20E   ' % test.CeR_tmp[t])
                file2.write('%30.20E   ' % test.CcR_tmp[t])
                file2.write('%30.20E   ' % test.Plastic_ratio[t])        
                file2.write(' \n' )    
            file2.close()
            #-------------------------------------------------------------------------------------------------
            #                         Save total fields
            #-------------------------------------------------------------------------------------------------
            file2 = open(os.path.join( ResultsDir,'Test_%s.p' %( NameSuffix ) ) ,'wb') 
            pickle.dump(test, file2)
            file2.close()


