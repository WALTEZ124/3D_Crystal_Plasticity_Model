# -*- coding: utf-8 -*-
def Reconstruct_Fields(test , Uref_EL, Uref_PL ):
    dUx_tot = test.dUx_tot
    dUy_tot = test.dUy_tot
    dUz_tot = test.dUz_tot
    dKI_tild   = test.dKI_tild
    dKII_tild  = test.dKII_tild
    dKIII_tild = test.dKIII_tild
    dRhoI      = test.dRhoI
    dRhoII     = test.dRhoII
    dRhoIII    = test.dRhoIII
    rad_min, rad_max = Uref_PL.I.Extraction_zone
    thet_len         = len(Uref_PL.I.theta)
    time_len         = len(test.time)
    Ux_EL_ref_I  = Uref_EL.I.x
    Uy_EL_ref_I  = Uref_EL.I.y
    Uz_EL_ref_I  = Uref_EL.I.z
    Ux_EL_ref_II = Uref_EL.II.x
    Uy_EL_ref_II = Uref_EL.II.y
    Uz_EL_ref_II = Uref_EL.II.z
    Ux_EL_ref_III = Uref_EL.III.x
    Uy_EL_ref_III = Uref_EL.III.y
    Uz_EL_ref_III = Uref_EL.III.z
    Ux_PL_ref_I  = Uref_PL.I.x
    Uy_PL_ref_I  = Uref_PL.I.y
    Uz_PL_ref_I  = Uref_PL.I.z
    Ux_PL_ref_II = Uref_PL.II.x
    Uy_PL_ref_II = Uref_PL.II.y
    Uz_PL_ref_II = Uref_PL.II.z
    Ux_PL_ref_III = Uref_PL.III.x
    Uy_PL_ref_III = Uref_PL.III.y
    Uz_PL_ref_III = Uref_PL.III.z
    CeR_tmp = []
    CcR_tmp = []
    Plastic_ratio = []
    for t in range(time_len-1):
        Sum_tmp   = 0
        Sum_EL_tmp   = 0
        Sum_PL_field_tmp = 0
        Norme_tot_tmp  = 0
        Norme_tot_decomp_tmp = 0
        for j in range(rad_min*thet_len,rad_max*thet_len):
            Ux_decomp_EL_I  = dKI_tild[t]    * Ux_EL_ref_I[j]           
            Uy_decomp_EL_I  = dKI_tild[t]    * Uy_EL_ref_I[j]
            Uz_decomp_EL_I  = dKI_tild[t]    * Uz_EL_ref_I[j]
            Ux_decomp_EL_II = dKII_tild[t]   * Ux_EL_ref_II[j]
            Uy_decomp_EL_II = dKII_tild[t]   * Uy_EL_ref_II[j]  
            Uz_decomp_EL_II = dKII_tild[t]   * Uz_EL_ref_II[j]  
            Ux_decomp_EL_III = dKIII_tild[t]  * Ux_EL_ref_III[j]
            Uy_decomp_EL_III = dKIII_tild[t]  * Uy_EL_ref_III[j]    
            Uz_decomp_EL_III = dKIII_tild[t]  * Uz_EL_ref_III[j]  
            Ux_decomp_PL_I  = dRhoI[t]  * Ux_PL_ref_I[j] 
            Uy_decomp_PL_I  = dRhoI[t]  * Uy_PL_ref_I[j]
            Uz_decomp_PL_I  = dRhoI[t]  * Uz_PL_ref_I[j]
            Ux_decomp_PL_II = dRhoII[t] * Ux_PL_ref_II[j] 
            Uy_decomp_PL_II = dRhoII[t] * Uy_PL_ref_II[j]   
            Uz_decomp_PL_II = dRhoII[t] * Uz_PL_ref_II[j]   
            Ux_decomp_PL_III = dRhoIII[t] * Ux_PL_ref_III[j] 
            Uy_decomp_PL_III = dRhoIII[t] * Uy_PL_ref_III[j]    
            Uz_decomp_PL_III = dRhoIII[t] * Uz_PL_ref_III[j]    
            Ux_decomp_I  = Ux_decomp_EL_I  + Ux_decomp_PL_I
            Uy_decomp_I  = Uy_decomp_EL_I  + Uy_decomp_PL_I
            Uz_decomp_I  = Uz_decomp_EL_I  + Uz_decomp_PL_I
            Ux_decomp_II = Ux_decomp_EL_II + Ux_decomp_PL_II
            Uy_decomp_II = Uy_decomp_EL_II + Uy_decomp_PL_II
            Uz_decomp_II = Uz_decomp_EL_II + Uz_decomp_PL_II
            Ux_decomp_III = Ux_decomp_EL_III + Ux_decomp_PL_III
            Uy_decomp_III = Uy_decomp_EL_III + Uy_decomp_PL_III
            Uz_decomp_III = Uz_decomp_EL_III + Uz_decomp_PL_III
            ### Sum of the residual field after elastic part extraction
            Sum_EL_tmp  += pow(dUx_tot[j][t] - Ux_decomp_EL_I - Ux_decomp_EL_II - Ux_decomp_EL_III  , 2) + pow(dUy_tot[j][t] - Uy_decomp_EL_I - Uy_decomp_EL_II - Uy_decomp_EL_III  , 2) + pow(dUz_tot[j][t] - Uz_decomp_EL_I - Uz_decomp_EL_II - Uz_decomp_EL_III  , 2)
            ### Sum of the residual field after elastic and plastic parts extraction
            Sum_tmp     += pow( dUx_tot[j][t] - Ux_decomp_I - Ux_decomp_II - Ux_decomp_III, 2) + pow( dUy_tot[j][t] - Uy_decomp_I - Uy_decomp_II - Uy_decomp_III, 2) + pow( dUz_tot[j][t] - Uz_decomp_I - Uz_decomp_II - Uz_decomp_III, 2)
            ### Sum of the reconstracted plastic field
            Sum_PL_field_tmp  += pow( Ux_decomp_PL_I + Ux_decomp_PL_II + Ux_decomp_PL_III  , 2) + pow( Uy_decomp_PL_I + Uy_decomp_PL_II + Uy_decomp_PL_III  , 2) + pow( Uz_decomp_PL_I + Uz_decomp_PL_II + Uz_decomp_PL_III  , 2)
            ### Norme of the total numerical field
            Norme_tot_tmp        += pow( dUx_tot[j][t], 2) + pow( dUy_tot[j][t], 2) + pow( dUz_tot[j][t], 2)
            ### Norme of the total reconstructed field
            Norme_tot_decomp_tmp += pow( Ux_decomp_I + Ux_decomp_II + Ux_decomp_III, 2) + pow( Uy_decomp_I + Uy_decomp_II + Uy_decomp_III, 2) + pow( Uz_decomp_I + Uz_decomp_II + Uz_decomp_III, 2)
        CeR_tmp   += [sqrt( Sum_EL_tmp /  Norme_tot_tmp )]
        CcR_tmp   += [sqrt( Sum_tmp    /  Norme_tot_tmp )]
        Plastic_ratio += [ sqrt( Sum_PL_field_tmp /  Norme_tot_decomp_tmp ) ]
    return CeR_tmp, CcR_tmp , Plastic_ratio
