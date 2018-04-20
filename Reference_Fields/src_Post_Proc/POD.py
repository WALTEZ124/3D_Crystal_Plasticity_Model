
# -*- coding: utf-8 -*-
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



def POD_PL(dUx_PL,dUy_PL,dUz_PL, dimensions):
    listN_F_len = dimensions.listN_F_len
    time_len    = dimensions.time_len
    rad_len     = dimensions.rad_len
    thet_len    = dimensions.thet_len
    z_len       = dimensions.z_len
    #ref_field_len = dimensions.ref_field_len
    Ux_aux = np.asarray(dUx_PL)
    Uy_aux = np.asarray(dUy_PL)
    Uz_aux = np.asarray(dUz_PL)
    #z_orig1 = rad_len*thet_len*int(z_len/2)
    #z_orig2 = rad_len*thet_len*(int(z_len/2)+1)
    #Ux_PL = Ux_aux[z_orig1 : z_orig2][:]
    #Uy_PL = Uy_aux[z_orig1 : z_orig2][:]
    #Uz_PL = Uz_aux[z_orig1 : z_orig2][:]
    VUPLtemps = np.vstack(( Ux_aux, Uy_aux, Uz_aux))
     #en temps et en espace et recuperation de la fonction de l'espace
    C = np.dot(VUPLtemps,VUPLtemps.T)
    autoval,autovect = power(C)    # LM stands for larger in magnitude
    UPL = autovect.reshape([np.shape(autovect)[0],1])
    drho = np.dot(VUPLtemps.T,UPL[:,0])
    drho = drho.reshape([np.shape(drho)[0],1])
    if np.mean(drho)<0 :                               # Because of the problem of sign of the POD
        UPL  = np.multiply(UPL, -1)
        drho = np.multiply(drho, -1)  
    else :
        UPL = np.asarray(UPL)
    UPL_mat = UPL.reshape(3,listN_F_len)
    Ux_PL_POD = UPL_mat[0]
    Uy_PL_POD = UPL_mat[1]
    Uz_PL_POD = UPL_mat[2]
    return Ux_PL_POD, Uy_PL_POD, Ux_PL_POD, drho


def SVD_PL(dUx_PL,dUy_PL,dUz_PL , dimensions):
    listN_F_len = dimensions.listN_F_len
    time_len    = dimensions.time_len
    rad_len     = dimensions.rad_len
    thet_len    = dimensions.thet_len
    z_len       = dimensions.z_len
    #ref_field_len = dimensions.ref_field_len
    Ux_aux = np.asarray(dUx_PL)
    Uy_aux = np.asarray(dUy_PL)
    Uz_aux = np.asarray(dUz_PL)
    #z_orig1 = rad_len*thet_len*int(z_len/2)
    #z_orig2 = rad_len*thet_len*(int(z_len/2)+1)
    #Ux_PL = Ux_aux[z_orig1 : z_orig2][:]
    #Uy_PL = Uy_aux[z_orig1 : z_orig2][:]
    #Uz_PL = Uz_aux[z_orig1 : z_orig2][:]
    VUPLtime = np.vstack(( Ux_aux, Uy_aux, Uz_aux))
    #POD en temps et en espace et recuperation de la fonction de l'espace
    U, sI, V = np.linalg.svd(VUPLtime, full_matrices=True)
    UPL    = [x[0] for x in U]
    VT  = np.transpose(V)
    dRho =  [sI[0]*x[0] for x in VT ]
    if np.mean(dRho)<0 :                               # Because of the problem of sign of the POD
        UPL  = np.multiply(UPL, -1)
        dRho = np.multiply(dRho, -1)    
    else :
        UPL = np.asarray(UPL)
    UPL_mat = UPL.reshape(3,listN_F_len)
    Ux_PL_SVD = UPL_mat[0]
    Uy_PL_SVD = UPL_mat[1]
    Uz_PL_SVD = UPL_mat[2]
    return Ux_PL_SVD, Uy_PL_SVD, Ux_PL_SVD, dRho


def SVD_Tot(test, dimensions):
    listN_F_len = dimensions.listN_F_len
    time_len    = dimensions.time_len
    rad_len     = dimensions.rad_len
    thet_len    = dimensions.thet_len
    z_len       = dimensions.z_len
    #ref_field_len = dimensions.ref_field_len
    Ux_aux = np.asarray(test.dUx_tot)
    Uy_aux = np.asarray(test.dUy_tot)
    Uz_aux = np.asarray(test.dUz_tot)
    #z_orig1 = rad_len*thet_len*int(z_len/2)
    #z_orig2 = rad_len*thet_len*(int(z_len/2)+1)
    #Ux_PL = Ux_aux[z_orig1 : z_orig2][:]
    #Uy_PL = Uy_aux[z_orig1 : z_orig2][:]
    #Uz_PL = Uz_aux[z_orig1 : z_orig2][:]
    VUPLtime = np.vstack(( Ux_aux, Uy_aux, Uz_aux))
    #POD en temps et en espace et recuperation de la fonction de l'espace
    U, sI, V = np.linalg.svd(VUPLtime, full_matrices=True)
    UEL    = [x[0] for x in U]
    VT = np.transpose(V)
    dK_tild  =  [sI[0]*x[0] for x in VT ]
    UPL      = [x[1] for x in U]
    VT = np.transpose(V)
    dRho  =  [sI[1]*x[1] for x in VT ]
    print 'dK_tild: ',dK_tild
    print 'dRho: '   ,dRho
    if np.mean(dRho)<0 :                               # Because of the problem of sign of the POD
        UPL  = np.multiply(UPL, -1)
        dRho = np.multiply(dRho, -1)    
    print 'drho: ',drho
    Ux_EL_SVD=[]
    Uy_EL_SVD=[]
    Uz_EL_SVD=[]
    Ux_PL_SVD=[]
    Uy_PL_SVD=[]
    Uz_PL_SVD=[]
    #ref_field_len = rad_len*thet_len
    for j in range(listN_F_len):
        Ux_EL_SVD.append(UEL[j])
        Uy_EL_SVD.append(UEL[j+listN_F_len])
        Uz_EL_SVD.append(UEL[j+2*listN_F_len])
        Ux_PL_SVD.append(UPL[j])
        Uy_PL_SVD.append(UPL[j+listN_F_len])
        Uz_PL_SVD.append(UPL[j+2*listN_F_len])
    return Ux_EL_SVD, Uy_EL_SVD, Ux_EL_SVD ,  dK_tild, Ux_PL_SVD, Uy_PL_SVD, Ux_PL_SVD, dRho




def POD_PL_Component(U_PL_Component, temps, listN_F_len):
    VUPLtemps = np.asarray(U_PL_Component)
	#POD time and space
    C = np.dot(VUPLtemps,VUPLtemps.T)
    autoval,autovect = power(C)    # LM stands for larger in magnitude
    UPL = autovect.reshape([np.shape(autovect)[0],1])
    drho = np.dot(VUPLtemps.T,UPL[:,0])
    drho = drho.reshape([np.shape(drho)[0],1])
    print 'drho: ',drho
    return UPL, drho


def POD_r_theta(Ux_ref, Uy_ref, Uz_ref, Mode, dimensions):
    ###############################################################################################
    #   POD - Computation of f(r) (radial dependency) and g(theta) (angular dependancy)   #
    ###############################################################################################
    #:Diagonalisation et enregistrement - VU
    rad_len     = dimensions.rad_len
    thet_len    = dimensions.thet_len
    z_len       = dimensions.z_len
    Ux = np.asarray(Ux_ref)
    Uy = np.asarray(Uy_ref)
    Uz = np.asarray(Uz_ref)
    Ux_aux = Ux.reshape(rad_len, thet_len).T
    Uy_aux = Uy.reshape(rad_len, thet_len).T
    Uz_aux = Uz.reshape(rad_len, thet_len).T
#    Ux_ref = Ux_aux[int(z_len/2)][:][:].T
#    Uy_ref = Uy_aux[int(z_len/2)][:][:].T
#    Uz_ref = Uz_aux[int(z_len/2)][:][:].T
    POD_snapshot = np.vstack((Ux_aux, Uy_aux, Uz_aux))
    C = np.dot(POD_snapshot,POD_snapshot.T)
    #  find the biggest eigenvalue and relative eigenvector"
    autoval,autovect = power(C)    # LM stands for larger in magnitude
    autovect = autovect.reshape([np.shape(autovect)[0],1])
    gx=[]
    gy=[]
    gz=[]
    if Mode == 'Mode I':
        adim_coef = abs(autovect[2*thet_len-1])              # Divide by the last X component to size the CTOD = 1 (at Theta = Pi)
    elif Mode == 'Mode II':
        adim_coef = abs(autovect[thet_len-1])     # Divide by the last Y component to size the CTSD = 1 (at Theta = Pi)
    elif Mode == 'Mode III':
        adim_coef = abs(autovect[3*thet_len-1])     # Divide by the last Y component to size the CTSD = 1 (at Theta = Pi)    
    for i in range(thet_len):
        gx += [ autovect[i] / adim_coef / 2. ]
        gy += [ autovect[thet_len+i] / adim_coef / 2. ]    
        gz += [ autovect[2*thet_len+i] / adim_coef / 2. ]
    Urad=np.dot(POD_snapshot.T,autovect[:,0])
    Urad=Urad.reshape([np.shape(Urad)[0],1])
    Urad = np.multiply(Urad, 2*adim_coef)
    if Urad[0] < 0 :
        Urad = np.multiply(Urad, -1)
        gx = np.multiply(gx, -1 )
        gy = np.multiply(gy, -1 )
        gz = np.multiply(gz, -1 )
    return Urad, gx, gy , gz


def POD_r_theta_Combined(Ux_I, Uy_I, Ux_II, Uy_II, radlong, thetalong):      # Non adimensionné 
    Ux_I = np.asarray(Ux_I)
    Uy_I = np.asarray(Uy_I)
    Ux_II = np.asarray(Ux_II)
    Uy_II = np.asarray(Uy_II)
    Ux_I = Ux_I.reshape( radlong,thetalong).T
    Uy_I = Uy_I.reshape( radlong, thetalong).T
    Ux_II = Ux_II.reshape( radlong,thetalong).T
    Uy_II = Uy_II.reshape( radlong, thetalong).T    
    POD_snapshot = np.vstack((Ux_I, Uy_I, Ux_II, Uy_II))
    C = np.dot(POD_snapshot,POD_snapshot.T)
    #  find the biggest eigenvalue and relative eigenvector"
    autoval,autovect = power(C)    # LM stands for larger in magnitude
    autovect = autovect.reshape([np.shape(autovect)[0],1])
    ###############################################################################################
    #   POD - Computation of f(r) (radial dependency) and g(theta) (angular dependancy)   #
    ###############################################################################################
    #:Diagonalisation et enregistrement - VU    
    Ux_I=[]
    Uy_I=[]
    Ux_II=[]
    Uy_II=[]
    for i in range(thetalong):
        Ux_I  += [ autovect[i] ]
        Uy_I  += [ autovect[thetalong+i] ]
        Ux_II += [ autovect[2*thetalong+i] ]
        Uy_II += [ autovect[3*thetalong+i] ]
    Urad=np.dot(POD_snapshot.T,autovect[:,0])
    Urad=Urad.reshape([np.shape(Urad)[0],1])
    return Urad, Ux_I, Uy_I, Ux_II, Uy_II

