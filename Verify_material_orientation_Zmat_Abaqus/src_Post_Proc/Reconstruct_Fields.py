def Reconstruct_Fields(test , Uref , dimensions ):

	dUx_tot = test.dUx_tot
	dUy_tot = test.dUy_tot
	dUz_tot = test.dUz_tot

	dKI_tild   = test.dKI_tild
	dKII_tild  = test.dKII_tild
	dKIII_tild = test.dKIII_tild

	dRhoI      = test.dRhoI
	dRhoII     = test.dRhoII
	dRhoIII    = test.dRhoIII

	listN_F_len = dimensions.listN_F_len
	time_len = dimensions.time_len

	Ux_EL_ref_I  = Uref.EL.I.x
	Uy_EL_ref_I  = Uref.EL.I.y
	Uz_EL_ref_I  = Uref.EL.I.z

	Ux_EL_ref_II = Uref.EL.II.x
	Uy_EL_ref_II = Uref.EL.II.y
	Uz_EL_ref_II = Uref.EL.II.z

	Ux_EL_ref_III = Uref.EL.III.x
	Uy_EL_ref_III = Uref.EL.III.y
	Uz_EL_ref_III = Uref.EL.III.z

	Ux_PL_ref_I  = Uref.PL.I.x
	Uy_PL_ref_I  = Uref.PL.I.y
	Uz_PL_ref_I  = Uref.PL.I.z

	Ux_PL_ref_II = Uref.PL.II.x
	Uy_PL_ref_II = Uref.PL.II.y
	Uz_PL_ref_II = Uref.PL.II.z

	Ux_PL_ref_III = Uref.PL.III.x
	Uy_PL_ref_III = Uref.PL.III.y
	Uz_PL_ref_III = Uref.PL.III.z

	CeR_tmp = []
	CcR_tmp = []
	Sum_EL  = 0
	Sum  = 0
	Norme_tot = 0

	for t in range(time_len-1):
		Sum_tmp_I   = 0
		Sum_tmp_II  = 0
		Sum_tmp_III = 0
		Sum_EL_tmp_I   = 0
		Sum_EL_tmp_II  = 0
		Sum_EL_tmp_III = 0
		Norme_tot_tmp  = 0
		for j in range(listN_F_len):
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
			
			Sum_EL_tmp_I   += pow(dUx_tot[j][t] - Ux_decomp_EL_I - Ux_decomp_EL_II - Ux_decomp_EL_III  , 2) + pow(dUy_tot[j][t] - Uy_decomp_EL_I - Uy_decomp_EL_II - Uy_decomp_EL_III  , 2) + pow(dUz_tot[j][t] - Uz_decomp_EL_I - Uz_decomp_EL_II - Uz_decomp_EL_III  , 2)
			#Sum_EL_tmp_II  += pow(dUx_tot[j][t] - Ux_decomp_EL_II  , 2) + pow(dUy_tot[j][t] - Uy_decomp_EL_II  , 2) + pow(dUz_tot[j][t] - Uz_decomp_EL_II  , 2)
			#Sum_EL_tmp_III += pow(dUx_tot[j][t] - Ux_decomp_EL_III , 2) + pow(dUy_tot[j][t] - Uy_decomp_EL_III , 2) + pow(dUz_tot[j][t] - Uz_decomp_EL_III , 2)
			
			Sum_tmp_I     += pow(dUx_tot[j][t] - Ux_decomp_I -Ux_decomp_II - Ux_decomp_III   , 2) + pow(dUy_tot[j][t] - Uy_decomp_I - Uy_decomp_II - Uy_decomp_III   , 2) + pow(dUz_tot[j][t] - Uz_decomp_I - Uz_decomp_II - Uz_decomp_III    , 2)
			#Sum_tmp_II    += pow(dUx_tot[j][t] - Ux_decomp_II  , 2) + pow(dUy_tot[j][t] - Uy_decomp_II  , 2) + pow(dUz_tot[j][t] - Uz_decomp_II  , 2)
			#Sum_tmp_III   += pow(dUx_tot[j][t] - Ux_decomp_III , 2) + pow(dUy_tot[j][t] - Uy_decomp_III , 2) + pow(dUz_tot[j][t] - Uz_decomp_III , 2)
			Norme_tot_tmp += pow(dUx_tot[j][t]  , 2) + pow(dUy_tot[j][t]  , 2) + pow(dUz_tot[j][t]  , 2)
			#Sum_EL_tmp += pow(dUx_tot[j][t] - Ux_decomp_EL_I   + dUy_tot[j][t] - Uy_decomp_EL_I   + dUz_tot[j][t] - Uz_decomp_EL_I   , 2)
			#Sum_EL_tmp += pow(dUx_tot[j][t] - Ux_decomp_EL_II  + dUy_tot[j][t] - Uy_decomp_EL_II  + dUz_tot[j][t] - Uz_decomp_EL_II  , 2)
			#Sum_EL_tmp += pow(dUx_tot[j][t] - Ux_decomp_EL_III + dUy_tot[j][t] - Uy_decomp_EL_III + dUz_tot[j][t] - Uz_decomp_EL_III , 2)
			#Sum_tmp_I   += pow(dUx_tot[j][t] - Ux_decomp_I   + dUy_tot[j][t] - Uy_decomp_I   + dUz_tot[j][t] - Uz_decomp_I   , 2)
			#Sum_tmp_II  += pow(dUx_tot[j][t] - Ux_decomp_II  + dUy_tot[j][t] - Uy_decomp_II  + dUz_tot[j][t] - Uz_decomp_II  , 2)
			#Sum_tmp_III += pow(dUx_tot[j][t] - Ux_decomp_III + dUy_tot[j][t] - Uy_decomp_III + dUz_tot[j][t] - Uz_decomp_III , 2)
			#Norme_tot_tmp  += pow(dUx_tot[j][t]  + dUy_tot[j][t] + dUz_tot[j][t]  , 2)
		Norme_tot += Norme_tot_tmp 
		Sum_EL    += Sum_EL_tmp_I + Sum_EL_tmp_II + Sum_EL_tmp_III
		Sum       += Sum_tmp_I + Sum_tmp_II + Sum_tmp_III
		CeR_tmp   += [sqrt( ( Sum_EL_tmp_I + Sum_EL_tmp_II + Sum_EL_tmp_III) /  Norme_tot_tmp )]
		CcR_tmp   += [sqrt( ( Sum_tmp_I    + Sum_tmp_II    + Sum_tmp_III   ) /  Norme_tot_tmp )]
	CeR = sqrt(Sum_EL / Norme_tot)
	CcR = sqrt(Sum / Norme_tot)
	return CeR, CcR, CeR_tmp, CcR_tmp


def Reconstruct_Fields_Flavien_Fremy(temps,Ux_tot, Uy_tot, KI_tild, KII_tild, RhoI_tild, RhoII_tild, Uref , listN_F_len, radlong, half_thetalong ):
	Ux_EL_ref_I  = Uref.EL.I.x
	Uy_EL_ref_I  = Uref.EL.I.y
	Ux_EL_ref_II = Uref.EL.II.x
	Uy_EL_ref_II = Uref.EL.II.y
	Ux_PL_ref_I  = Uref.PL.I.x
	Uy_PL_ref_I  = Uref.PL.I.y
	Ux_PL_ref_II = Uref.PL.II.x
	Uy_PL_ref_II = Uref.PL.II.y
	Ux_I, Uy_I, Ux_II, Uy_II = PL_Sym_Asym_Decomp(Ux_tot, Uy_tot, temps, radlong, half_thetalong)
	CeR_tmp = []
	CcR_tmp = []
	Norme_tot = []
	for t in range(len(temps)-1):
		Sum_tmp  = 0
		Sum_EL_tmp  = 0
		Norme_tot_tmp  = 0
		for j in range(listN_F_len):
			Ux_decomp_EL_I  = KI_tild[t]    * Ux_EL_ref_I[j] 
			Uy_decomp_EL_I  = KI_tild[t]    * Uy_EL_ref_I[j]
			Ux_decomp_EL_II = KII_tild[t]   * Ux_EL_ref_II[j]
			Uy_decomp_EL_II = KII_tild[t]   * Uy_EL_ref_II[j]	

			Ux_decomp_PL_I  = RhoI_tild[t]  * Ux_PL_ref_I[j] 
			Uy_decomp_PL_I  = RhoI_tild[t]  * Uy_PL_ref_I[j]
			Ux_decomp_PL_II = RhoII_tild[t] * Ux_PL_ref_II[j] 
			Uy_decomp_PL_II = RhoII_tild[t] * Uy_PL_ref_II[j]	

			Ux_decomp_I  = Ux_decomp_EL_I  + Ux_decomp_PL_I
			Uy_decomp_I  = Uy_decomp_EL_I  + Uy_decomp_PL_I
			Ux_decomp_II = Ux_decomp_EL_II + Ux_decomp_PL_II
			Uy_decomp_II = Uy_decomp_EL_II + Uy_decomp_PL_II

			Sum_EL_tmp  += pow( (Ux_I[j][t]  - Ux_decomp_EL_I) + (Ux_II[j][t] - Ux_decomp_EL_II) , 2)
			Sum_EL_tmp  += pow( (Uy_I[j][t]  - Uy_decomp_EL_I) + (Uy_II[j][t] - Uy_decomp_EL_II) , 2)

			Sum_tmp  += pow( (Ux_I[j][t]  - Ux_decomp_I) + (Ux_II[j][t] - Ux_decomp_II) , 2)
			Sum_tmp  += pow( (Uy_I[j][t]  - Uy_decomp_I) + (Uy_II[j][t] - Uy_decomp_II) , 2)

			Norme_tot_tmp  += pow(Ux_I[j][t] + Ux_II[j][t] , 2)
			Norme_tot_tmp  += pow(Uy_I[j][t] + Uy_II[j][t] , 2)

		Norme_tot_tmp = 1000.*sqrt(Norme_tot_tmp/listN_F_len)
		Sum_EL_tmp    = 1000.*sqrt(Sum_EL_tmp/listN_F_len)
		Sum_tmp       = 1000.*sqrt(Sum_tmp/listN_F_len)

		if ( Norme_tot_tmp < 0.00005 ) :
			CeR = 0.
			CcR = 0.
		else :
			CeR = Sum_EL_tmp / Norme_tot_tmp
			CcR = Sum_tmp / Norme_tot_tmp

		CeR_tmp  += [ CeR ]
		CcR_tmp  += [ CcR ]
		Norme_tot+= [Norme_tot_tmp]

	return CeR_tmp, CcR_tmp, Norme_tot
