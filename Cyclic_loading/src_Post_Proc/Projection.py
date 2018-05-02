# -*- coding: utf-8 -*-
def Projection_on_crack_faces_of_reduced_zone_order_dependent(test, mode_order_list, Uref_EL, Uref_PL):
    dUx_tot = test.dUx_tot
    dUy_tot = test.dUy_tot
    dUz_tot = test.dUz_tot
    # Refernce fields of the whole zone
    Ux_EL_ref_I   = eval('Uref_EL.%s.x' %mode_order_list[0])
    Uy_EL_ref_I   = eval('Uref_EL.%s.y' %mode_order_list[0])
    Uz_EL_ref_I   = eval('Uref_EL.%s.z' %mode_order_list[0])
    Ux_EL_ref_II  = eval('Uref_EL.%s.x' %mode_order_list[1])
    Uy_EL_ref_II  = eval('Uref_EL.%s.y' %mode_order_list[1])
    Uz_EL_ref_II  = eval('Uref_EL.%s.z' %mode_order_list[1])
    Ux_EL_ref_III = eval('Uref_EL.%s.x' %mode_order_list[2])
    Uy_EL_ref_III = eval('Uref_EL.%s.y' %mode_order_list[2])
    Uz_EL_ref_III = eval('Uref_EL.%s.z' %mode_order_list[2])
    Ux_PL_ref_I   = eval('Uref_PL.%s.x' %mode_order_list[0])
    Uy_PL_ref_I   = eval('Uref_PL.%s.y' %mode_order_list[0])
    Uz_PL_ref_I   = eval('Uref_PL.%s.z' %mode_order_list[0])
    Ux_PL_ref_II  = eval('Uref_PL.%s.x' %mode_order_list[1])
    Uy_PL_ref_II  = eval('Uref_PL.%s.y' %mode_order_list[1])
    Uz_PL_ref_II  = eval('Uref_PL.%s.z' %mode_order_list[1])
    Ux_PL_ref_III = eval('Uref_PL.%s.x' %mode_order_list[2])
    Uy_PL_ref_III = eval('Uref_PL.%s.y' %mode_order_list[2])
    Uz_PL_ref_III = eval('Uref_PL.%s.z' %mode_order_list[2])
    # Displacement jump field
    DUx_EL_Lips_I   = eval('Uref_EL.%s.Delta_x' %mode_order_list[0])
    DUy_EL_Lips_I   = eval('Uref_EL.%s.Delta_y' %mode_order_list[0])
    DUz_EL_Lips_I   = eval('Uref_EL.%s.Delta_z' %mode_order_list[0])
    DUx_EL_Lips_II  = eval('Uref_EL.%s.Delta_x' %mode_order_list[1])
    DUy_EL_Lips_II  = eval('Uref_EL.%s.Delta_y' %mode_order_list[1])
    DUz_EL_Lips_II  = eval('Uref_EL.%s.Delta_z' %mode_order_list[1])
    DUx_EL_Lips_III = eval('Uref_EL.%s.Delta_x' %mode_order_list[2])
    DUy_EL_Lips_III = eval('Uref_EL.%s.Delta_y' %mode_order_list[2])
    DUz_EL_Lips_III = eval('Uref_EL.%s.Delta_z' %mode_order_list[2])
    DUx_PL_Lips_I   = eval('Uref_PL.%s.Delta_x' %mode_order_list[0])
    DUy_PL_Lips_I   = eval('Uref_PL.%s.Delta_y' %mode_order_list[0])
    DUz_PL_Lips_I   = eval('Uref_PL.%s.Delta_z' %mode_order_list[0])
    DUx_PL_Lips_II  = eval('Uref_PL.%s.Delta_x' %mode_order_list[1])
    DUy_PL_Lips_II  = eval('Uref_PL.%s.Delta_y' %mode_order_list[1])
    DUz_PL_Lips_II  = eval('Uref_PL.%s.Delta_z' %mode_order_list[1])
    DUx_PL_Lips_III = eval('Uref_PL.%s.Delta_x' %mode_order_list[2])
    DUy_PL_Lips_III = eval('Uref_PL.%s.Delta_y' %mode_order_list[2])
    DUz_PL_Lips_III = eval('Uref_PL.%s.Delta_z' %mode_order_list[2])
    rad_min, rad_max = Uref_PL.I.Extraction_zone
    thet_len = len(Uref_PL.I.theta)
    time_len = len(test.time)
    Norme_EL_I   = pow(np.linalg.norm(DUx_EL_Lips_I[rad_min : rad_max])  ,2) + pow(np.linalg.norm(DUy_EL_Lips_I[rad_min : rad_max])  ,2) + pow(np.linalg.norm(DUz_EL_Lips_I[rad_min : rad_max])  ,2)
    Norme_EL_II  = pow(np.linalg.norm(DUx_EL_Lips_II[rad_min : rad_max]) ,2) + pow(np.linalg.norm(DUy_EL_Lips_II[rad_min : rad_max]) ,2) + pow(np.linalg.norm(DUz_EL_Lips_II[rad_min : rad_max]) ,2)
    Norme_EL_III = pow(np.linalg.norm(DUx_EL_Lips_III[rad_min : rad_max]),2) + pow(np.linalg.norm(DUy_EL_Lips_III[rad_min : rad_max]),2) + pow(np.linalg.norm(DUz_EL_Lips_III[rad_min : rad_max]),2)
    Norme_PL_I   = pow(np.linalg.norm(DUx_PL_Lips_I)  ,2) + pow(np.linalg.norm(DUy_PL_Lips_I)  ,2) + pow(np.linalg.norm(DUz_PL_Lips_I)  ,2)
    Norme_PL_II  = pow(np.linalg.norm(DUx_PL_Lips_II) ,2) + pow(np.linalg.norm(DUy_PL_Lips_II) ,2) + pow(np.linalg.norm(DUz_PL_Lips_II) ,2)
    Norme_PL_III = pow(np.linalg.norm(DUx_PL_Lips_III),2) + pow(np.linalg.norm(DUy_PL_Lips_III),2) + pow(np.linalg.norm(DUz_PL_Lips_III),2)
    KI_tild   =[]
    KII_tild  =[]
    KIII_tild =[]
    RhoI      =[]
    RhoII     =[]
    RhoIII    =[]
    for i in range(time_len-1):
        dKI_tild=0.
        for j in range(rad_min,rad_max):
            j1 = (j-rad_min) *thet_len 
            j2 = (j+1-rad_min)*thet_len - 1 
            dKI_tild   += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Lips_I[j] )   + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Lips_I[j] )   + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Lips_I[j] )   #projection du saut de deplacement totatl sur le saut de deplacement de reference
        KItild  = dKI_tild  / Norme_EL_I
        KI_tild.append(KItild)
        dKII_tild=0.
        dUx_int_I = []
        dUy_int_I = []
        dUz_int_I = []
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int   = ( dUx_tot[j][i] - KItild * Ux_EL_ref_I[j])  
            dUy_int   = ( dUy_tot[j][i] - KItild * Uy_EL_ref_I[j])  
            dUz_int   = ( dUz_tot[j][i] - KItild * Uz_EL_ref_I[j])  
            dUx_int_I += [dUx_int]
            dUy_int_I += [dUy_int]
            dUz_int_I += [dUz_int]
        for j in range(rad_min,rad_max):
            j1 = (j-rad_min) *thet_len 
            j2 = (j+1-rad_min)*thet_len - 1 
            dKII_tild  += ( (dUx_int_I[j2]-dUx_int_I[j1]) * DUx_EL_Lips_II[j] )  + ( (dUy_int_I[j2]-dUy_int_I[j1]) * DUy_EL_Lips_II[j] )  + ( (dUz_int_I[j2]-dUz_int_I[j1]) * DUz_EL_Lips_II[j] )
        KIItild = dKII_tild / Norme_EL_II
        KII_tild.append(KIItild)
        dUx_int_I_II = []
        dUy_int_I_II = []
        dUz_int_I_II = []
        dKIII_tild=0.
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int   = ( dUx_int_I[j] - KIItild * Ux_EL_ref_II[j])  
            dUy_int   = ( dUy_int_I[j] - KIItild * Uy_EL_ref_II[j])  
            dUz_int   = ( dUz_int_I[j] - KIItild * Uz_EL_ref_II[j])  
            dUx_int_I_II += [dUx_int]
            dUy_int_I_II += [dUy_int]
            dUz_int_I_II += [dUz_int]
        for j in range(rad_min,rad_max):
            j1 = (j-rad_min) *thet_len 
            j2 = (j+1-rad_min)*thet_len - 1 
            dKIII_tild += ( (dUx_int_I_II[j2]-dUx_int_I_II[j1]) * DUx_EL_Lips_III[j] )  + ( (dUy_int_I_II[j2]-dUy_int_I_II[j1]) * DUy_EL_Lips_III[j] )  + ( (dUz_int_I_II[j2]-dUz_int_I_II[j1]) * DUz_EL_Lips_III[j] )
        KIIItild = dKIII_tild / Norme_EL_III
        KIII_tild.append(KIIItild)
        dUx_int_I_II_III = []
        dUy_int_I_II_III = []       
        dUz_int_I_II_III = []
        drhoI = 0.
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int  = dUx_int_I_II[j] - KIIItild * Ux_EL_ref_III[j]
            dUy_int  = dUy_int_I_II[j] - KIIItild * Uy_EL_ref_III[j]
            dUz_int  = dUz_int_I_II[j] - KIIItild * Uz_EL_ref_III[j]
            dUx_int_I_II_III += [dUx_int]
            dUy_int_I_II_III += [dUy_int]
            dUz_int_I_II_III += [dUz_int]
        for j in range(rad_max-rad_min):
            j1 = j*thet_len
            j2 = (j+1)*thet_len-1
            drhoI += ( (dUx_int_I_II_III[j2]-dUx_int_I_II_III[j1]) * DUx_PL_Lips_I[j] )  + ( (dUy_int_I_II_III[j2]-dUy_int_I_II_III[j1]) * DUy_PL_Lips_I[j] )  + ( (dUz_int_I_II_III[j2]-dUz_int_I_II_III[j1]) * DUz_PL_Lips_I[j] )
        rhoI = drhoI/Norme_PL_I
        RhoI.append(rhoI)
        dUx_PL_int_I = []
        dUy_PL_int_I = []       
        dUz_PL_int_I = []
        drhoII = 0.
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int  = dUx_int_I_II_III[j] - rhoI * Ux_PL_ref_I[j]
            dUy_int  = dUy_int_I_II_III[j] - rhoI * Uy_PL_ref_I[j]
            dUz_int  = dUz_int_I_II_III[j] - rhoI * Uz_PL_ref_I[j]
            dUx_PL_int_I += [dUx_int]
            dUy_PL_int_I += [dUy_int]
            dUz_PL_int_I += [dUz_int]
        for j in range(rad_max-rad_min):
            j1 = j*thet_len
            j2 = (j+1)*thet_len-1
            drhoII += ( (dUx_PL_int_I[j2]-dUx_PL_int_I[j1]) * DUx_PL_Lips_II[j] )  + ( (dUy_PL_int_I[j2]-dUy_PL_int_I[j1]) * DUy_PL_Lips_II[j] )  + ( (dUz_PL_int_I[j2]-dUz_PL_int_I[j1]) * DUz_PL_Lips_II[j] )
        rhoII = drhoII/Norme_PL_II
        RhoII.append(rhoII)
        dUx_PL_int_I_II = []
        dUy_PL_int_I_II = []        
        dUz_PL_int_I_II = []
        drhoIII = 0.
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int  = dUx_PL_int_I[j] - rhoII * Ux_PL_ref_II[j]
            dUy_int  = dUy_PL_int_I[j] - rhoII * Uy_PL_ref_II[j]
            dUz_int  = dUz_PL_int_I[j] - rhoII * Uz_PL_ref_II[j]
            dUx_PL_int_I_II += [dUx_int]
            dUy_PL_int_I_II += [dUy_int]
            dUz_PL_int_I_II += [dUz_int]
        for j in range(rad_max-rad_min):
            j1 = j*thet_len
            j2 = (j+1)*thet_len-1
            drhoIII += ( (dUx_PL_int_I_II[j2]-dUx_PL_int_I_II[j1]) * DUx_PL_Lips_III[j] )  + ( (dUy_PL_int_I_II[j2]-dUy_PL_int_I_II[j1]) * DUy_PL_Lips_III[j] )  + ( (dUz_PL_int_I_II[j2]-dUz_PL_int_I_II[j1]) * DUz_PL_Lips_III[j] )
        rhoIII = drhoIII/Norme_PL_III
        RhoIII.append(rhoIII)
    #       dUx_Res = []
    #       dUy_Res = []        
    #       dUz_Res = []
    #       for j in range(listN_F_len):
    #           dUx_int  = dUx_PL_int_I_II[j] - rhoIII * Ux_PL_ref_III[j]
    #           dUy_int  = dUy_PL_int_I_II[j] - rhoIII * Uy_PL_ref_III[j]
    #           dUz_int  = dUz_PL_int_I_II[j] - rhoIII * Uz_PL_ref_III[j]
    #           dUx_Res += [dUx_int]
    #           dUy_Res += [dUy_int]
    #           dUz_Res += [dUz_int]
    return KI_tild, KII_tild, KIII_tild, RhoI, RhoII, RhoIII


def Projection_on_crack_faces_of_reduced_zone(test, Uref_EL, Uref_PL):
    dUx_tot = test.dUx_tot
    dUy_tot = test.dUy_tot
    dUz_tot = test.dUz_tot
    DUx_EL_Lips_I   = Uref_EL.I.Delta_x
    DUy_EL_Lips_I   = Uref_EL.I.Delta_y
    DUz_EL_Lips_I   = Uref_EL.I.Delta_z
    DUx_EL_Lips_II  = Uref_EL.II.Delta_x
    DUy_EL_Lips_II  = Uref_EL.II.Delta_y
    DUz_EL_Lips_II  = Uref_EL.II.Delta_z
    DUx_EL_Lips_III = Uref_EL.III.Delta_x
    DUy_EL_Lips_III = Uref_EL.III.Delta_y
    DUz_EL_Lips_III = Uref_EL.III.Delta_z
    DUx_PL_Lips_I   = Uref_PL.I.Delta_x
    DUy_PL_Lips_I   = Uref_PL.I.Delta_y
    DUz_PL_Lips_I   = Uref_PL.I.Delta_z
    DUx_PL_Lips_II  = Uref_PL.II.Delta_x
    DUy_PL_Lips_II  = Uref_PL.II.Delta_y
    DUz_PL_Lips_II  = Uref_PL.II.Delta_z
    DUx_PL_Lips_III = Uref_PL.III.Delta_x
    DUy_PL_Lips_III = Uref_PL.III.Delta_y
    DUz_PL_Lips_III = Uref_PL.III.Delta_z
    rad_min, rad_max = Uref_PL.I.Extraction_zone
    thet_len = len(Uref_PL.I.theta)
    time_len = len(test.time)
    Norme_EL_I   = pow(np.linalg.norm(DUx_EL_Lips_I[rad_min : rad_max])  ,2) + pow(np.linalg.norm(DUy_EL_Lips_I[rad_min : rad_max])  ,2) + pow(np.linalg.norm(DUz_EL_Lips_I[rad_min : rad_max])  ,2)
    Norme_EL_II  = pow(np.linalg.norm(DUx_EL_Lips_II[rad_min : rad_max]) ,2) + pow(np.linalg.norm(DUy_EL_Lips_II[rad_min : rad_max]) ,2) + pow(np.linalg.norm(DUz_EL_Lips_II[rad_min : rad_max]) ,2)
    Norme_EL_III = pow(np.linalg.norm(DUx_EL_Lips_III[rad_min : rad_max]),2) + pow(np.linalg.norm(DUy_EL_Lips_III[rad_min : rad_max]),2) + pow(np.linalg.norm(DUz_EL_Lips_III[rad_min : rad_max]),2)
    Norme_PL_I   = pow(np.linalg.norm(DUx_PL_Lips_I)  ,2) + pow(np.linalg.norm(DUy_PL_Lips_I)  ,2) + pow(np.linalg.norm(DUz_PL_Lips_I)  ,2)
    Norme_PL_II  = pow(np.linalg.norm(DUx_PL_Lips_II) ,2) + pow(np.linalg.norm(DUy_PL_Lips_II) ,2) + pow(np.linalg.norm(DUz_PL_Lips_II) ,2)
    Norme_PL_III = pow(np.linalg.norm(DUx_PL_Lips_III),2) + pow(np.linalg.norm(DUy_PL_Lips_III),2) + pow(np.linalg.norm(DUz_PL_Lips_III),2)
    KI_tild   =[]
    KII_tild  =[]
    KIII_tild =[]
    RhoI      =[]
    RhoII     =[]
    RhoIII    =[]
    for i in range(time_len-1):
        dKI_tild=0.
        dKII_tild=0.
        dKIII_tild=0.       
        drhoI   = 0.
        drhoII  = 0.
        drhoIII = 0.
        for j in range(rad_min,rad_max):
            j1 = j*thet_len
            j2 = (j+1)*thet_len-1
            dKI_tild   += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Lips_I[j] )   + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Lips_I[j] )   + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Lips_I[j] )   #projection du saut de deplacement totatl sur le saut de deplacement de reference
            dKII_tild  += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Lips_II[j] )  + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Lips_II[j] )  + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Lips_II[j] )
            dKIII_tild += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Lips_III[j] ) + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Lips_III[j] ) + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Lips_III[j] )
            drhoI  += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_PL_Lips_I[j] )    + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_PL_Lips_I[j] )    + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_PL_Lips_I[j] )
            drhoII += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_PL_Lips_II[j] )   + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_PL_Lips_II[j] )   + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_PL_Lips_II[j] )
            drhoIII+= ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_PL_Lips_III[j] )  + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_PL_Lips_III[j] )  + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_PL_Lips_III[j] )
        KItild  = dKI_tild  / Norme_EL_I
        KI_tild.append(KItild)
        KIItild = dKII_tild / Norme_EL_II
        KII_tild.append(KIItild)
        KIIItild = dKIII_tild / Norme_EL_III
        KIII_tild.append(KIIItild)
        drI  = drhoI  / Norme_PL_I
        RhoI.append(drI)
        drII  = drhoII  / Norme_PL_II
        RhoII.append(drII)
        drIII  = drhoIII  / Norme_PL_III
        RhoIII.append(drIII)
    return KI_tild, KII_tild, KIII_tild, RhoI, RhoII, RhoIII



def Projection_reduced_zone_Order_Dependent(test, mode_order_list, Uref_EL, Uref_PL):
    dUx_tot = test.dUx_tot
    dUy_tot = test.dUy_tot
    dUz_tot = test.dUz_tot
    # Refernce fields of the whole zone
    Ux_EL_ref_I   = eval('Uref_EL.%s.x' % mode_order_list[0])
    Uy_EL_ref_I   = eval('Uref_EL.%s.y' % mode_order_list[0])
    Uz_EL_ref_I   = eval('Uref_EL.%s.z' % mode_order_list[0])
    Ux_EL_ref_II  = eval('Uref_EL.%s.x' % mode_order_list[1])
    Uy_EL_ref_II  = eval('Uref_EL.%s.y' % mode_order_list[1])
    Uz_EL_ref_II  = eval('Uref_EL.%s.z' % mode_order_list[1])
    Ux_EL_ref_III = eval('Uref_EL.%s.x' % mode_order_list[2])
    Uy_EL_ref_III = eval('Uref_EL.%s.y' % mode_order_list[2])
    Uz_EL_ref_III = eval('Uref_EL.%s.z' % mode_order_list[2])
    Ux_PL_ref_I   = eval('Uref_PL.%s.x' % mode_order_list[0])
    Uy_PL_ref_I   = eval('Uref_PL.%s.y' % mode_order_list[0])
    Uz_PL_ref_I   = eval('Uref_PL.%s.z' % mode_order_list[0])
    Ux_PL_ref_II  = eval('Uref_PL.%s.x' % mode_order_list[1])
    Uy_PL_ref_II  = eval('Uref_PL.%s.y' % mode_order_list[1])
    Uz_PL_ref_II  = eval('Uref_PL.%s.z' % mode_order_list[1])
    Ux_PL_ref_III = eval('Uref_PL.%s.x' % mode_order_list[2])
    Uy_PL_ref_III = eval('Uref_PL.%s.y' % mode_order_list[2])
    Uz_PL_ref_III = eval('Uref_PL.%s.z' % mode_order_list[2])
    rad_min, rad_max = Uref_PL.I.Extraction_zone
    thet_len = len(Uref_PL.I.theta)
    time_len = len(test.time)
    Norme_EL_I   = pow(np.linalg.norm(Ux_EL_ref_I[rad_min*thet_len : rad_max*thet_len])    ,2) + pow(np.linalg.norm(Uy_EL_ref_I[rad_min*thet_len : rad_max*thet_len])    ,2) + pow(np.linalg.norm(Uz_EL_ref_I[rad_min*thet_len : rad_max*thet_len])    ,2)
    Norme_EL_II  = pow(np.linalg.norm(Ux_EL_ref_II[rad_min*thet_len : rad_max*thet_len])   ,2) + pow(np.linalg.norm(Uy_EL_ref_II[rad_min*thet_len : rad_max*thet_len])   ,2) + pow(np.linalg.norm(Uz_EL_ref_II[rad_min*thet_len : rad_max*thet_len])   ,2)
    Norme_EL_III = pow(np.linalg.norm(Ux_EL_ref_III[rad_min*thet_len : rad_max*thet_len])  ,2) + pow(np.linalg.norm(Uy_EL_ref_III[rad_min*thet_len : rad_max*thet_len])  ,2) + pow(np.linalg.norm(Uz_EL_ref_III[rad_min*thet_len : rad_max*thet_len])  ,2)
    Norme_PL_I   = pow(np.linalg.norm(Ux_PL_ref_I)   ,2) + pow(np.linalg.norm(Uy_PL_ref_I)   ,2) + pow(np.linalg.norm(Uz_PL_ref_I)   ,2)
    Norme_PL_II  = pow(np.linalg.norm(Ux_PL_ref_II)  ,2) + pow(np.linalg.norm(Uy_PL_ref_II)  ,2) + pow(np.linalg.norm(Uz_PL_ref_II)  ,2)
    Norme_PL_III = pow(np.linalg.norm(Ux_PL_ref_III) ,2) + pow(np.linalg.norm(Uy_PL_ref_III) ,2) + pow(np.linalg.norm(Uz_PL_ref_III) ,2)
    KI_tild   =[]
    KII_tild  =[]
    KIII_tild =[]
    RhoI      =[]
    RhoII     =[]
    RhoIII    =[]
    for i in range(time_len-1):
        dKI_tild=0.
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dKI_tild   += (dUx_tot[j][i] * Ux_EL_ref_I[j])   + (dUy_tot[j][i] * Uy_EL_ref_I[j])   + (dUz_tot[j][i] * Uz_EL_ref_I[j])   #projection du champ elastique de reference sur le champ total
        KItild  = dKI_tild  / Norme_EL_I
        KI_tild.append(KItild)
        dKII_tild=0.
        dUx_int_I = []
        dUy_int_I = []
        dUz_int_I = []
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dUx_int   = ( dUx_tot[j][i] - KItild * Ux_EL_ref_I[j])  
            dUy_int   = ( dUy_tot[j][i] - KItild * Uy_EL_ref_I[j])  
            dUz_int   = ( dUz_tot[j][i] - KItild * Uz_EL_ref_I[j])  
            dKII_tild += (dUx_int * Ux_EL_ref_II[j]) + (dUy_int * Uy_EL_ref_II[j])  + (dUz_int * Uz_EL_ref_II[j])
            dUx_int_I += [dUx_int]
            dUy_int_I += [dUy_int]
            dUz_int_I += [dUz_int]
        KIItild = dKII_tild / Norme_EL_II
        KII_tild.append(KIItild)
        dUx_int_I_II = []
        dUy_int_I_II = []
        dUz_int_I_II = []
        dKIII_tild=0.
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dUx_int   = ( dUx_int_I[j] - KIItild * Ux_EL_ref_II[j])  
            dUy_int   = ( dUy_int_I[j] - KIItild * Uy_EL_ref_II[j])  
            dUz_int   = ( dUz_int_I[j] - KIItild * Uz_EL_ref_II[j])  
            dKIII_tild  += (dUx_int * Ux_EL_ref_III[j]) + (dUy_int * Uy_EL_ref_III[j])  + (dUz_int * Uz_EL_ref_III[j])
            dUx_int_I_II += [dUx_int]
            dUy_int_I_II += [dUy_int]
            dUz_int_I_II += [dUz_int]
        KIIItild = dKIII_tild / Norme_EL_III
        KIII_tild.append(KIIItild)
        dUx_int_I_II_III = []
        dUy_int_I_II_III = []       
        dUz_int_I_II_III = []
        drhoI = 0.
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dUx_int  = dUx_int_I_II[j] - KIIItild * Ux_EL_ref_III[j]
            dUy_int  = dUy_int_I_II[j] - KIIItild * Uy_EL_ref_III[j]
            dUz_int  = dUz_int_I_II[j] - KIIItild * Uz_EL_ref_III[j]
            drhoI   += (dUx_int * Ux_PL_ref_I[j]) + (dUy_int * Uy_PL_ref_I[j])  + (dUz_int * Uz_PL_ref_I[j])
            dUx_int_I_II_III += [dUx_int]
            dUy_int_I_II_III += [dUy_int]
            dUz_int_I_II_III += [dUz_int]
        rhoI = drhoI/Norme_PL_I
        RhoI.append(rhoI)
        dUx_PL_int_I = []
        dUy_PL_int_I = []       
        dUz_PL_int_I = []
        drhoII = 0.
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dUx_int  = dUx_int_I_II_III[j] - rhoI * Ux_PL_ref_I[j]
            dUy_int  = dUy_int_I_II_III[j] - rhoI * Uy_PL_ref_I[j]
            dUz_int  = dUz_int_I_II_III[j] - rhoI * Uz_PL_ref_I[j]
            drhoII  += (dUx_int * Ux_PL_ref_II[j]) + (dUy_int * Uy_PL_ref_II[j])  + (dUz_int * Uz_PL_ref_II[j])
            dUx_PL_int_I += [dUx_int]
            dUy_PL_int_I += [dUy_int]
            dUz_PL_int_I += [dUz_int]
        rhoII = drhoII/Norme_PL_II
        RhoII.append(rhoII)
        dUx_PL_int_I_II = []
        dUy_PL_int_I_II = []        
        dUz_PL_int_I_II = []
        drhoIII = 0.
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dUx_int  = dUx_PL_int_I[j] - rhoII * Ux_PL_ref_II[j]
            dUy_int  = dUy_PL_int_I[j] - rhoII * Uy_PL_ref_II[j]
            dUz_int  = dUz_PL_int_I[j] - rhoII * Uz_PL_ref_II[j]
            drhoIII += (dUx_int * Ux_PL_ref_III[j]) + (dUy_int * Uy_PL_ref_III[j])  + (dUz_int * Uz_PL_ref_III[j])
            dUx_PL_int_I_II += [dUx_int]
            dUy_PL_int_I_II += [dUy_int]
            dUz_PL_int_I_II += [dUz_int]
        rhoIII = drhoIII/Norme_PL_III
        RhoIII.append(rhoIII)
#       dUx_Res = []
#       dUy_Res = []        
#       dUz_Res = []
#       for j in range(listN_F_len):
#           dUx_int  = dUx_PL_int_I_II[j] - rhoIII * Ux_PL_ref_III[j]
#           dUy_int  = dUy_PL_int_I_II[j] - rhoIII * Uy_PL_ref_III[j]
#           dUz_int  = dUz_PL_int_I_II[j] - rhoIII * Uz_PL_ref_III[j]
#           dUx_Res += [dUx_int]
#           dUy_Res += [dUy_int]
#           dUz_Res += [dUz_int]
    return KI_tild, KII_tild, KIII_tild, RhoI, RhoII, RhoIII


def Mixed_Projection_on_reduced_zone_order_dependent(test, mode_order_list, Uref_EL, Uref_PL): 
    # Projection on full field for the elastic aprt, and on crack lips for the plastic part
    dUx_tot = test.dUx_tot
    dUy_tot = test.dUy_tot
    dUz_tot = test.dUz_tot
    # Refernce fields of the whole zone
    Ux_EL_ref_I   = eval('Uref_EL.%s.x' %mode_order_list[0])
    Uy_EL_ref_I   = eval('Uref_EL.%s.y' %mode_order_list[0])
    Uz_EL_ref_I   = eval('Uref_EL.%s.z' %mode_order_list[0])
    Ux_EL_ref_II  = eval('Uref_EL.%s.x' %mode_order_list[1])
    Uy_EL_ref_II  = eval('Uref_EL.%s.y' %mode_order_list[1])
    Uz_EL_ref_II  = eval('Uref_EL.%s.z' %mode_order_list[1])
    Ux_EL_ref_III = eval('Uref_EL.%s.x' %mode_order_list[2])
    Uy_EL_ref_III = eval('Uref_EL.%s.y' %mode_order_list[2])
    Uz_EL_ref_III = eval('Uref_EL.%s.z' %mode_order_list[2])
    Ux_PL_ref_I   = eval('Uref_PL.%s.x' %mode_order_list[0])
    Uy_PL_ref_I   = eval('Uref_PL.%s.y' %mode_order_list[0])
    Uz_PL_ref_I   = eval('Uref_PL.%s.z' %mode_order_list[0])
    Ux_PL_ref_II  = eval('Uref_PL.%s.x' %mode_order_list[1])
    Uy_PL_ref_II  = eval('Uref_PL.%s.y' %mode_order_list[1])
    Uz_PL_ref_II  = eval('Uref_PL.%s.z' %mode_order_list[1])
    Ux_PL_ref_III = eval('Uref_PL.%s.x' %mode_order_list[2])
    Uy_PL_ref_III = eval('Uref_PL.%s.y' %mode_order_list[2])
    Uz_PL_ref_III = eval('Uref_PL.%s.z' %mode_order_list[2])
    # Displacement jump field
    DUx_EL_Lips_I   = eval('Uref_EL.%s.Delta_x' %mode_order_list[0])
    DUy_EL_Lips_I   = eval('Uref_EL.%s.Delta_y' %mode_order_list[0])
    DUz_EL_Lips_I   = eval('Uref_EL.%s.Delta_z' %mode_order_list[0])
    DUx_EL_Lips_II  = eval('Uref_EL.%s.Delta_x' %mode_order_list[1])
    DUy_EL_Lips_II  = eval('Uref_EL.%s.Delta_y' %mode_order_list[1])
    DUz_EL_Lips_II  = eval('Uref_EL.%s.Delta_z' %mode_order_list[1])
    DUx_EL_Lips_III = eval('Uref_EL.%s.Delta_x' %mode_order_list[2])
    DUy_EL_Lips_III = eval('Uref_EL.%s.Delta_y' %mode_order_list[2])
    DUz_EL_Lips_III = eval('Uref_EL.%s.Delta_z' %mode_order_list[2])
    DUx_PL_Lips_I   = eval('Uref_PL.%s.Delta_x' %mode_order_list[0])
    DUy_PL_Lips_I   = eval('Uref_PL.%s.Delta_y' %mode_order_list[0])
    DUz_PL_Lips_I   = eval('Uref_PL.%s.Delta_z' %mode_order_list[0])
    DUx_PL_Lips_II  = eval('Uref_PL.%s.Delta_x' %mode_order_list[1])
    DUy_PL_Lips_II  = eval('Uref_PL.%s.Delta_y' %mode_order_list[1])
    DUz_PL_Lips_II  = eval('Uref_PL.%s.Delta_z' %mode_order_list[1])
    DUx_PL_Lips_III = eval('Uref_PL.%s.Delta_x' %mode_order_list[2])
    DUy_PL_Lips_III = eval('Uref_PL.%s.Delta_y' %mode_order_list[2])
    DUz_PL_Lips_III = eval('Uref_PL.%s.Delta_z' %mode_order_list[2])
    rad_min, rad_max = Uref_PL.I.Extraction_zone
    thet_len = len(Uref_PL.I.theta)
    time_len = len(test.time)
    Norme_EL_I   = pow(np.linalg.norm(DUx_EL_Lips_I[rad_min : rad_max])  ,2) + pow(np.linalg.norm(DUy_EL_Lips_I[rad_min : rad_max])  ,2) + pow(np.linalg.norm(DUz_EL_Lips_I[rad_min : rad_max])  ,2)
    Norme_EL_II  = pow(np.linalg.norm(DUx_EL_Lips_II[rad_min : rad_max]) ,2) + pow(np.linalg.norm(DUy_EL_Lips_II[rad_min : rad_max]) ,2) + pow(np.linalg.norm(DUz_EL_Lips_II[rad_min : rad_max]) ,2)
    Norme_EL_III = pow(np.linalg.norm(DUx_EL_Lips_III[rad_min : rad_max]),2) + pow(np.linalg.norm(DUy_EL_Lips_III[rad_min : rad_max]),2) + pow(np.linalg.norm(DUz_EL_Lips_III[rad_min : rad_max]),2)
    Norme_PL_I   = pow(np.linalg.norm(DUx_PL_Lips_I)  ,2) + pow(np.linalg.norm(DUy_PL_Lips_I)  ,2) + pow(np.linalg.norm(DUz_PL_Lips_I)  ,2)
    Norme_PL_II  = pow(np.linalg.norm(DUx_PL_Lips_II) ,2) + pow(np.linalg.norm(DUy_PL_Lips_II) ,2) + pow(np.linalg.norm(DUz_PL_Lips_II) ,2)
    Norme_PL_III = pow(np.linalg.norm(DUx_PL_Lips_III),2) + pow(np.linalg.norm(DUy_PL_Lips_III),2) + pow(np.linalg.norm(DUz_PL_Lips_III),2)
    KI_tild   =[]
    KII_tild  =[]
    KIII_tild =[]
    RhoI      =[]
    RhoII     =[]
    RhoIII    =[]
    for i in range(time_len-1):
        dKI_tild=0.
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dKI_tild   += (dUx_tot[j][i] * Ux_EL_ref_I[j])   + (dUy_tot[j][i] * Uy_EL_ref_I[j])   + (dUz_tot[j][i] * Uz_EL_ref_I[j])   #projection du champ elastique de reference sur le champ total
        KItild  = dKI_tild  / Norme_EL_I
        KI_tild.append(KItild)
        dKII_tild=0.
        dUx_int_I = []
        dUy_int_I = []
        dUz_int_I = []
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dUx_int   = ( dUx_tot[j][i] - KItild * Ux_EL_ref_I[j])  
            dUy_int   = ( dUy_tot[j][i] - KItild * Uy_EL_ref_I[j])  
            dUz_int   = ( dUz_tot[j][i] - KItild * Uz_EL_ref_I[j])  
            dKII_tild += (dUx_int * Ux_EL_ref_II[j]) + (dUy_int * Uy_EL_ref_II[j])  + (dUz_int * Uz_EL_ref_II[j])
            dUx_int_I += [dUx_int]
            dUy_int_I += [dUy_int]
            dUz_int_I += [dUz_int]
        KIItild = dKII_tild / Norme_EL_II
        KII_tild.append(KIItild)
        dUx_int_I_II = []
        dUy_int_I_II = []
        dUz_int_I_II = []
        dKIII_tild=0.
        for j in range(rad_min*thet_len, rad_max*thet_len):
            dUx_int   = ( dUx_int_I[j] - KIItild * Ux_EL_ref_II[j])  
            dUy_int   = ( dUy_int_I[j] - KIItild * Uy_EL_ref_II[j])  
            dUz_int   = ( dUz_int_I[j] - KIItild * Uz_EL_ref_II[j])  
            dKIII_tild  += (dUx_int * Ux_EL_ref_III[j]) + (dUy_int * Uy_EL_ref_III[j])  + (dUz_int * Uz_EL_ref_III[j])
            dUx_int_I_II += [dUx_int]
            dUy_int_I_II += [dUy_int]
            dUz_int_I_II += [dUz_int]
        KIIItild = dKIII_tild / Norme_EL_III
        KIII_tild.append(KIIItild)
        dUx_int_I_II_III = []
        dUy_int_I_II_III = []       
        dUz_int_I_II_III = []
        drhoI = 0.
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int  = dUx_int_I_II[j] - KIIItild * Ux_EL_ref_III[j]
            dUy_int  = dUy_int_I_II[j] - KIIItild * Uy_EL_ref_III[j]
            dUz_int  = dUz_int_I_II[j] - KIIItild * Uz_EL_ref_III[j]
            dUx_int_I_II_III += [dUx_int]
            dUy_int_I_II_III += [dUy_int]
            dUz_int_I_II_III += [dUz_int]
        for j in range(rad_max-rad_min):
            j1 = j*thet_len
            j2 = (j+1)*thet_len-1
            drhoI += ( (dUx_int_I_II_III[j2]-dUx_int_I_II_III[j1]) * DUx_PL_Lips_I[j] )  + ( (dUy_int_I_II_III[j2]-dUy_int_I_II_III[j1]) * DUy_PL_Lips_I[j] )  + ( (dUz_int_I_II_III[j2]-dUz_int_I_II_III[j1]) * DUz_PL_Lips_I[j] )
        rhoI = drhoI/Norme_PL_I
        RhoI.append(rhoI)
        dUx_PL_int_I = []
        dUy_PL_int_I = []       
        dUz_PL_int_I = []
        drhoII = 0.
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int  = dUx_int_I_II_III[j] - rhoI * Ux_PL_ref_I[j]
            dUy_int  = dUy_int_I_II_III[j] - rhoI * Uy_PL_ref_I[j]
            dUz_int  = dUz_int_I_II_III[j] - rhoI * Uz_PL_ref_I[j]
            dUx_PL_int_I += [dUx_int]
            dUy_PL_int_I += [dUy_int]
            dUz_PL_int_I += [dUz_int]
        for j in range(rad_max-rad_min):
            j1 = j*thet_len
            j2 = (j+1)*thet_len-1
            drhoII += ( (dUx_PL_int_I[j2]-dUx_PL_int_I[j1]) * DUx_PL_Lips_II[j] )  + ( (dUy_PL_int_I[j2]-dUy_PL_int_I[j1]) * DUy_PL_Lips_II[j] )  + ( (dUz_PL_int_I[j2]-dUz_PL_int_I[j1]) * DUz_PL_Lips_II[j] )
        rhoII = drhoII/Norme_PL_II
        RhoII.append(rhoII)
        dUx_PL_int_I_II = []
        dUy_PL_int_I_II = []        
        dUz_PL_int_I_II = []
        drhoIII = 0.
        for j in range(rad_min*thet_len,rad_max*thet_len):
            dUx_int  = dUx_PL_int_I[j] - rhoII * Ux_PL_ref_II[j]
            dUy_int  = dUy_PL_int_I[j] - rhoII * Uy_PL_ref_II[j]
            dUz_int  = dUz_PL_int_I[j] - rhoII * Uz_PL_ref_II[j]
            dUx_PL_int_I_II += [dUx_int]
            dUy_PL_int_I_II += [dUy_int]
            dUz_PL_int_I_II += [dUz_int]
        for j in range(rad_max-rad_min):
            j1 = j*thet_len
            j2 = (j+1)*thet_len-1
            drhoIII += ( (dUx_PL_int_I_II[j2]-dUx_PL_int_I_II[j1]) * DUx_PL_Lips_III[j] )  + ( (dUy_PL_int_I_II[j2]-dUy_PL_int_I_II[j1]) * DUy_PL_Lips_III[j] )  + ( (dUz_PL_int_I_II[j2]-dUz_PL_int_I_II[j1]) * DUz_PL_Lips_III[j] )
        rhoIII = drhoIII/Norme_PL_III
        RhoIII.append(rhoIII)
    #       dUx_Res = []
    #       dUy_Res = []        
    #       dUz_Res = []
    #       for j in range(listN_F_len):
    #           dUx_int  = dUx_PL_int_I_II[j] - rhoIII * Ux_PL_ref_III[j]
    #           dUy_int  = dUy_PL_int_I_II[j] - rhoIII * Uy_PL_ref_III[j]
    #           dUz_int  = dUz_PL_int_I_II[j] - rhoIII * Uz_PL_ref_III[j]
    #           dUx_Res += [dUx_int]
    #           dUy_Res += [dUy_int]
    #           dUz_Res += [dUz_int]
    return KI_tild, KII_tild, KIII_tild, RhoI, RhoII, RhoIII


