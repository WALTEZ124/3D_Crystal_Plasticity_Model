def Projection(test, Uref , dimensions):
	dUx_tot = test.dUx_tot
	dUy_tot = test.dUy_tot	
	dUz_tot = test.dUz_tot
	time_len    = len(test.time)
	listN_F_len = dimensions.listN_F_len
	Ux_EL_ref_I  = Uref.EL.I.x
	Uy_EL_ref_I  = Uref.EL.I.y
	Uz_EL_ref_I  = Uref.EL.I.z
	Ux_EL_ref_II = Uref.EL.II.x
	Uy_EL_ref_II = Uref.EL.II.y
	Uz_EL_ref_II = Uref.EL.II.z
	Ux_EL_ref_III = Uref.EL.III.x
	Uy_EL_ref_III = Uref.EL.III.y
	Uz_EL_ref_III = Uref.EL.III.z
	Norme_EL_I   = Uref.EL.I.norme
	Norme_EL_II  = Uref.EL.II.norme
	Norme_EL_III = Uref.EL.III.norme
	Ux_PL_ref_I  = Uref.PL.I.x
	Uy_PL_ref_I  = Uref.PL.I.y
	Uz_PL_ref_I  = Uref.PL.I.z
	Ux_PL_ref_II = Uref.PL.II.x
	Uy_PL_ref_II = Uref.PL.II.y
	Uz_PL_ref_II = Uref.PL.II.z
	Ux_PL_ref_III = Uref.PL.III.x
	Uy_PL_ref_III = Uref.PL.III.y
	Uz_PL_ref_III = Uref.PL.III.z
	Norme_PL_I   = Uref.PL.I.norme
	Norme_PL_II  = Uref.PL.II.norme
	Norme_PL_III = Uref.PL.III.norme
	KI_tild   =[]
	KII_tild  =[]
	KIII_tild =[]
	RhoI_tild   =[]
	RhoII_tild  =[]
	RhoIII_tild =[]
	for i in range(time_len-1):
		dKI_tild=0.
		dKII_tild=0.
		dKIII_tild=0.
		dRhoI_tild=0.
		dRhoII_tild=0.
		dRhoIII_tild=0.
		for j in range(listN_F_len):
			dKI_tild   += (dUx_tot[j][i] * Ux_EL_ref_I[j])  + (dUy_tot[j][i] * Uy_EL_ref_I[j]) + (dUz_tot[j][i] * Uz_EL_ref_I[j])  #projection du champ elastique de reference sur le champ total
			dKII_tild  += (dUx_tot[j][i] * Ux_EL_ref_II[j]) + (dUy_tot[j][i] * Uy_EL_ref_II[j]) + (dUz_tot[j][i] * Uz_EL_ref_II[j])	
			dKIII_tild += (dUx_tot[j][i] * Ux_EL_ref_III[j]) + (dUy_tot[j][i] * Uy_EL_ref_III[j]) + (dUz_tot[j][i] * Uz_EL_ref_III[j])	
			#dRhoI_tild   += (dUx_tot[j][i] * Ux_PL_ref_I[j])  + (dUy_tot[j][i] * Uy_PL_ref_I[j]) + (dUz_tot[j][i] * Uz_PL_ref_I[j]) #projection du champ elastique de reference sur le champ total
			#dRhoII_tild  += (dUx_tot[j][i] * Ux_PL_ref_II[j]) + (dUy_tot[j][i] * Uy_PL_ref_II[j]) + (dUz_tot[j][i] * Uz_PL_ref_II[j])
			#dRhoIII_tild += (dUx_tot[j][i] * Ux_PL_ref_III[j]) + (dUy_tot[j][i] * Uy_PL_ref_III[j]) + (dUz_tot[j][i] * Uz_PL_ref_III[j])
			'''
			dUx_PL_I = dUx_tot[j][i] - dKI_tild * Ux_EL_ref_I[j]
			dUy_PL_I = dUy_tot[j][i] - dKI_tild * Uy_EL_ref_I[j]
			dUz_PL_I = dUz_tot[j][i] - dKI_tild * Uz_EL_ref_I[j]
			dUx_PL_II = dUx_tot[j][i] - dKII_tild * Ux_EL_ref_II[j]
			dUy_PL_II = dUy_tot[j][i] - dKII_tild * Uy_EL_ref_II[j]
			dUz_PL_II = dUz_tot[j][i] - dKII_tild * Uz_EL_ref_II[j]
			dUx_PL_III = dUx_tot[j][i] - dKIII_tild * Ux_EL_ref_III[j]
			dUy_PL_III = dUy_tot[j][i] - dKIII_tild * Uy_EL_ref_III[j]
			dUz_PL_III = dUz_tot[j][i] - dKIII_tild * Uz_EL_ref_III[j]
			dRhoI_tild  += (dUx_PL_I * Ux_PL_ref_I[j])  + (dUy_PL_I * Uy_PL_ref_I[j])   + (dUz_PL_I * Uz_PL_ref_I[j]) 
			dRhoII_tild += (dUx_PL_II * Ux_PL_ref_II[j]) + (dUy_PL_II * Uy_PL_ref_II[j]) + (dUz_PL_II * Uz_PL_ref_II[j])
			dRhoIII_tild += (dUx_PL_III * Ux_PL_ref_III[j]) + (dUy_PL_III * Uy_PL_ref_III[j]) + (dUz_PL_III * Uz_PL_ref_III[j])
			'''
			dUx_PL = dUx_tot[j][i] - ( dKI_tild * Ux_EL_ref_I[j] + dKII_tild * Ux_EL_ref_II[j] + dKIII_tild * Ux_EL_ref_III[j] )
			dUy_PL = dUy_tot[j][i] - ( dKI_tild * Uy_EL_ref_I[j] + dKII_tild * Uy_EL_ref_II[j] + dKIII_tild * Uy_EL_ref_III[j] )
			dUz_PL = dUz_tot[j][i] - ( dKI_tild * Uz_EL_ref_I[j] + dKII_tild * Uz_EL_ref_II[j] + dKIII_tild * Uz_EL_ref_III[j] )
			dRhoI_tild  += (dUx_PL * Ux_PL_ref_I[j])  + (dUy_PL * Uy_PL_ref_I[j])   + (dUz_PL * Uz_PL_ref_I[j]) 
			dRhoII_tild += (dUx_PL * Ux_PL_ref_II[j]) + (dUy_PL * Uy_PL_ref_II[j]) + (dUz_PL * Uz_PL_ref_II[j])
			dRhoIII_tild += (dUx_PL * Ux_PL_ref_III[j]) + (dUy_PL * Uy_PL_ref_III[j]) + (dUz_PL * Uz_PL_ref_III[j])
		KItild  = dKI_tild  / Norme_EL_I
		KI_tild.append(KItild)
		KIItild = dKII_tild / Norme_EL_II
		KII_tild.append(KIItild)
		KIIItild = dKIII_tild / Norme_EL_III
		KIII_tild.append(KIIItild)
		RhoItild  = dRhoI_tild  / Norme_PL_I
		RhoI_tild.append(RhoItild)
		RhoIItild = dRhoII_tild / Norme_PL_II
		RhoII_tild.append(RhoIItild)
		RhoIIItild = dRhoIII_tild / Norme_PL_III
		RhoIII_tild.append(RhoIIItild)
	return KI_tild, KII_tild, KIII_tild, RhoI_tild, RhoII_tild, RhoIII_tild



def Projection_Order_Dependent(test, mode_order, Uref, dimensions):
	dUx_tot = test.dUx_tot
	dUy_tot = test.dUy_tot
	dUz_tot = test.dUz_tot
	time_len    = len(test.time)
	listN_F_len = dimensions.listN_F_len
	Ux_EL_ref_I   = eval('Uref.EL.%s.x' %mode_order[0])
	Uy_EL_ref_I   = eval('Uref.EL.%s.y' %mode_order[0])
	Uz_EL_ref_I   = eval('Uref.EL.%s.z' %mode_order[0])
	Ux_EL_ref_II  = eval('Uref.EL.%s.x' %mode_order[1])
	Uy_EL_ref_II  = eval('Uref.EL.%s.y' %mode_order[1])
	Uz_EL_ref_II  = eval('Uref.EL.%s.z' %mode_order[1])
	Ux_EL_ref_III = eval('Uref.EL.%s.x' %mode_order[2])
	Uy_EL_ref_III = eval('Uref.EL.%s.y' %mode_order[2])
	Uz_EL_ref_III = eval('Uref.EL.%s.z' %mode_order[2])
	Norme_EL_I    = eval('Uref.EL.%s.norme' %mode_order[0])
	Norme_EL_II   = eval('Uref.EL.%s.norme' %mode_order[1])
	Norme_EL_III  = eval('Uref.EL.%s.norme' %mode_order[2])
	Ux_PL_ref_I   = eval('Uref.PL.%s.x' %mode_order[0])
	Uy_PL_ref_I   = eval('Uref.PL.%s.y' %mode_order[0])
	Uz_PL_ref_I   = eval('Uref.PL.%s.z' %mode_order[0])
	Ux_PL_ref_II  = eval('Uref.PL.%s.x' %mode_order[1])
	Uy_PL_ref_II  = eval('Uref.PL.%s.y' %mode_order[1])
	Uz_PL_ref_II  = eval('Uref.PL.%s.z' %mode_order[1])
	Ux_PL_ref_III = eval('Uref.PL.%s.x' %mode_order[2])
	Uy_PL_ref_III = eval('Uref.PL.%s.y' %mode_order[2])
	Uz_PL_ref_III = eval('Uref.PL.%s.z' %mode_order[2])
	Norme_PL_I    = eval('Uref.PL.%s.norme' %mode_order[0])
	Norme_PL_II   = eval('Uref.PL.%s.norme' %mode_order[1])
	Norme_PL_III  = eval('Uref.PL.%s.norme' %mode_order[2])
	KI_tild   =[]
	KII_tild  =[]
	KIII_tild =[]
	RhoI      =[]
	RhoII     =[]
	RhoIII    =[]
	for i in range(time_len-1):
		dKI_tild=0.
		for j in range(listN_F_len):
			dKI_tild   += (dUx_tot[j][i] * Ux_EL_ref_I[j])   + (dUy_tot[j][i] * Uy_EL_ref_I[j])   + (dUz_tot[j][i] * Uz_EL_ref_I[j])   #projection du champ elastique de reference sur le champ total
		KItild  = dKI_tild  / Norme_EL_I
		KI_tild.append(KItild)
		dKII_tild=0.
		dUx_int_I = []
 		dUy_int_I = []
		dUz_int_I = []
		for j in range(listN_F_len):
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
		for j in range(listN_F_len):
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
		for j in range(listN_F_len):
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
		for j in range(listN_F_len):
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
		for j in range(listN_F_len):
			dUx_int  = dUx_PL_int_I[j] - rhoII * Ux_PL_ref_II[j]
			dUy_int  = dUy_PL_int_I[j] - rhoII * Uy_PL_ref_II[j]
			dUz_int  = dUz_PL_int_I[j] - rhoII * Uz_PL_ref_II[j]
			drhoIII += (dUx_int * Ux_PL_ref_III[j]) + (dUy_int * Uy_PL_ref_III[j])  + (dUz_int * Uz_PL_ref_III[j])
			dUx_PL_int_I_II += [dUx_int]
			dUy_PL_int_I_II += [dUy_int]
			dUz_PL_int_I_II += [dUz_int]
		rhoIII = drhoIII/Norme_PL_III
		RhoIII.append(rhoIII)
#		dUx_Res = []
#		dUy_Res = []		
#		dUz_Res = []
#		for j in range(listN_F_len):
#			dUx_int  = dUx_PL_int_I_II[j] - rhoIII * Ux_PL_ref_III[j]
#			dUy_int  = dUy_PL_int_I_II[j] - rhoIII * Uy_PL_ref_III[j]
#			dUz_int  = dUz_PL_int_I_II[j] - rhoIII * Uz_PL_ref_III[j]
#			dUx_Res += [dUx_int]
#			dUy_Res += [dUy_int]
#			dUz_Res += [dUz_int]
	return KI_tild, KII_tild, KIII_tild, RhoI, RhoII, RhoIII


def EL_Projection(Ux_EL, Uy_EL, Uref , listN_F_len):
	Ux_EL_ref_I  = Uref.EL.I.x
	Uy_EL_ref_I  = Uref.EL.I.y
	Ux_EL_ref_II = Uref.EL.II.x
	Uy_EL_ref_II = Uref.EL.II.y
	Norme_EL_I   = Uref.EL.I.norme
	Norme_EL_II  = Uref.EL.II.norme
	dKI_nom  = 0.
	dKII_nom = 0.
	for j in range(listN_F_len):
		dKI_nom  += (Ux_EL[j] * Ux_EL_ref_I[j])  + (Uy_EL[j] * Uy_EL_ref_I[j])  #projection du champ elastique de reference sur le champ total
		dKII_nom += (Ux_EL[j] * Ux_EL_ref_II[j]) + (Uy_EL[j] * Uy_EL_ref_II[j])	
	KI_nom = dKI_nom / Norme_EL_I
	KII_nom = dKII_nom / Norme_EL_II
	return KI_nom, KII_nom 





