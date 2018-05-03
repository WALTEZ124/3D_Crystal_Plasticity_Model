
# -*- coding: utf-8 -*-

import numpy as np
import os
import pickle
from scipy.optimize import curve_fit

def power(A):
    '''  
    power function to find the biggest eigenvalues in magnitude
    '''
    toler=10**(-9)
    q=np.ones(A.shape[0])
    q=q/np.linalg.norm(q)
    z=np.dot(A,q)
    err=1
    eig_old=0
    while err>toler:
        q=z/np.linalg.norm(z)
        z=np.dot(A,q)
        eig=np.dot(q.T,np.dot(A,q))
        err=abs(eig-eig_old)
        eig_old=eig
    return eig, q

def exp_func(x, a, b):
    return a * np.exp(-b * x)

class Container(object):
    def __init__(self):
        pass


loading_type   = 'Imposed_Force'



material_orientation_list = [ [(0,1,0),(1,0,0)] ,[(1,1,0),(1,-1,0)], [(1,1,0),(0,0,1)], [(1,1,0),(1,-1,1)]]

for couple in  material_orientation_list :
    Shkl = "%d%d%d" % couple[0]
    Suvw = "%d%d%d" % couple[1]
    if Shkl == '000' and Suvw == '000':
        suffix = 'isotropic' 
    else :
        suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)
    #suffix_var = suffix.replace('-','_')
    R1 = 'Results_Post_Proc'
    R2 =  loading_type
    R3 = 'Results_Post_Proc_octahedral'
    R4 = 'Results_Post_Proc_%s' % (suffix )
    R5 = 'Small_Loading'
    R6 = 'Projection_On_Crack_Faces'
    ResultsDir_New = os.path.join(R1, R2, R3, R4, R5, R6)
    file2=open(os.path.join( ResultsDir_New,'Uref_EL_%s.p' %suffix ),'rb')
    Uref = pickle.load(file2)
    #Uref = pickle.load(file2, encoding='latin1')
    file2.close()
    rad = eval('Uref.EL.I.radial' )
    rad_len = len(rad)
    thet_len = len(Uref.EL.I.g_theta_x)
    theta = np.linspace(-np.pi,np.pi,thet_len)
    loading_step = 5
    # Load Elastic Reference Fields:
    mode_order_list = [ 'without_order', 'order_I_II_III' ]
    for mode_order in mode_order_list :
        # Load Plastic fields:
        src_folder = os.path.join(ResultsDir_New, mode_order )
        file2=open(os.path.join( src_folder,'Plastic_Field_%s_%s.p' % (mode_order, suffix) ),'rb')
        PL_field = pickle.load(file2)
        #PL_field = pickle.load(file2, encoding='latin1')
        file2.close()
        for mode in ['I','II', 'III']:
            PL = eval('PL_field.dUPL.%s' %mode)
            #PL.x = PL.x.tolist()
            #PL.y = PL.y.tolist()
            #PL.z = PL.z.tolist()
            listN_F_len = len(PL.x)
            K_max = PL.Loading_range[0]
            time_len = len(PL.time)
            rad_min = 0
            file2=open(os.path.join( ResultsDir_New,'Exp_Coef_mode_%s_%s_%s' % (mode, mode_order, suffix) ),'w') 
            file2.write('fit radial function with A.exp(-p*r) for different loading ranges [K_min, K_max] and on different extraction zone sizes [rad_min, rad_max]:') 
            file2.write(' \n' )  
            file2.write('rad_min , rad_max, K_min, K_max, A , p, error  ') 
            file2.write(' \n' )  
            for rad_max in range(int(rad_len/2), rad_len) :
                for len_min in np.arange(0, int(time_len)-2*loading_step+1, loading_step ):
                    for len_max in np.arange(len_min+loading_step , int(time_len)-loading_step+1, loading_step ):
                        Ux_PL_ref = [sum(PL.x[i][len_min:len_max]) for i in range(listN_F_len)]
                        Uy_PL_ref = [sum(PL.y[i][len_min:len_max]) for i in range(listN_F_len)]
                        Uz_PL_ref = [sum(PL.z[i][len_min:len_max]) for i in range(listN_F_len)]
                        rad_red = rad[rad_min:rad_max]
                        Ux_PL_ref_red =  np.asarray(Ux_PL_ref[rad_min*thet_len : rad_max*thet_len])
                        Uy_PL_ref_red =  np.asarray(Uy_PL_ref[rad_min*thet_len : rad_max*thet_len])
                        Uz_PL_ref_red =  np.asarray(Uz_PL_ref[rad_min*thet_len : rad_max*thet_len])
                        Ux_PL_ref_red = Ux_PL_ref_red.reshape( rad_max-rad_min , thet_len).T
                        Uy_PL_ref_red = Uy_PL_ref_red.reshape( rad_max-rad_min , thet_len).T
                        Uz_PL_ref_red = Uz_PL_ref_red.reshape( rad_max-rad_min , thet_len).T
                        POD_snapshot = np.vstack(( Ux_PL_ref_red, Uy_PL_ref_red, Uz_PL_ref_red))
                        C = np.dot(POD_snapshot,POD_snapshot.T)
                        autoval,autovect = power(C)    # LM stands for larger in magnitude
                        autovect = autovect.reshape([np.shape(autovect)[0],1])     
                        if mode == 'I':
                            adim_coef = abs(autovect[2*thet_len-1])              # Divide by the last X component to size the CTOD = 1 (at Theta = Pi)
                        elif mode == 'II':
                            adim_coef = abs(autovect[thet_len-1])     # Divide by the last Y component to size the CTSD = 1 (at Theta = Pi)
                        elif mode == 'III':
                            adim_coef = abs(autovect[3*thet_len-1])     # Divide by the last Y component to size the CTSD = 1 (at Theta = Pi)    
                        Urad=np.dot(POD_snapshot.T,autovect[:,0])
                        Urad=Urad.reshape([np.shape(Urad)[0],1])
                        Urad = np.multiply(Urad, 2*adim_coef)
                        if Urad[0] < 0 :
                            fr = np.multiply(Urad, -1)
                        else :
                            fr = np.asarray(Urad)
                        fr  = [x[0] for x in fr]
                        rad_red = np.transpose(rad_red)
                        popt, pcov = curve_fit( exp_func, rad_red, fr )
                        perr = np.sqrt(np.diag(pcov))
                        err_index = perr[0]*np.exp(perr[1])*1000
                        file2.write('%4.6E   ' % rad[rad_min] )             
                        file2.write('%4.6E   ' % rad[rad_max] ) 
                        file2.write('%4.6E   ' % len_min )       
                        file2.write('%4.6E   ' % len_max )  
                        file2.write('%4.6E   ' % popt[0] )
                        file2.write('%4.6E   ' % popt[1] )       
                        file2.write('%4.6E   ' % err_index ) 
                        file2.write(' \n' )         
            file2.close()


