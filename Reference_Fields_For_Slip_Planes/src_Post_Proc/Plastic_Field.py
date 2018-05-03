def Plastic_Field(test, UrefEL, dimensions):
	Ux_tot = test.dUx_tot
	Uy_tot = test.dUy_tot
	Uz_tot = test.dUz_tot
	listN_F_len = dimensions.listN_F_len
	time_len= len(test.time)
	Ux_EL_ref_I  = UrefEL.I.x
	Uy_EL_ref_I  = UrefEL.I.y
	Uz_EL_ref_I  = UrefEL.I.z
	Ux_EL_ref_II = UrefEL.II.x
	Uy_EL_ref_II = UrefEL.II.y
	Uz_EL_ref_II = UrefEL.II.z
	Ux_EL_ref_III = UrefEL.III.x
	Uy_EL_ref_III = UrefEL.III.y
	Uz_EL_ref_III = UrefEL.III.z
	Norme_EL_I   = UrefEL.I.norme
	Norme_EL_II  = UrefEL.II.norme
	Norme_EL_III  = UrefEL.III.norme
	KI_tild  =[]
	KII_tild =[]
	KIII_tild =[]
	for i in range(time_len-1):
		dKI_tild=0.
		dKII_tild=0.
		dKIII_tild=0.		
		for j in range(listN_F_len):
			dKI_tild   += (Ux_tot[j][i] * Ux_EL_ref_I[j])   + (Uy_tot[j][i] * Uy_EL_ref_I[j])   + (Uz_tot[j][i] * Uz_EL_ref_I[j])   #projection du champ elastique de reference sur le champ total
			dKII_tild  += (Ux_tot[j][i] * Ux_EL_ref_II[j])  + (Uy_tot[j][i] * Uy_EL_ref_II[j])  + (Uz_tot[j][i] * Uz_EL_ref_II[j])	
			dKIII_tild += (Ux_tot[j][i] * Ux_EL_ref_III[j]) + (Uy_tot[j][i] * Uy_EL_ref_III[j]) + (Uz_tot[j][i] * Uz_EL_ref_III[j])	
		KItild  = dKI_tild  / Norme_EL_I
		KI_tild.append(KItild)
		KIItild = dKII_tild / Norme_EL_II
		KII_tild.append(KIItild)
		KIIItild = dKIII_tild / Norme_EL_III
		KIII_tild.append(KIIItild)
	Ux_PL =[]
	Uy_PL =[]
	Uz_PL =[]
	for j in range(listN_F_len):
		dUx_PL=0.
		dUy_PL=0.
		dUz_PL=0.
		Ux_PLj=[]
		Uy_PLj=[]
		Uz_PLj=[]
		for i in range(time_len-1):
			dUx_PL = Ux_tot[j][i] - ( KI_tild[i] * Ux_EL_ref_I[j] + KII_tild[i] * Ux_EL_ref_II[j] +  KIII_tild[i] * Ux_EL_ref_III[j] ) #suppression du champ elastique au champ total
			dUy_PL = Uy_tot[j][i] - ( KI_tild[i] * Uy_EL_ref_I[j] + KII_tild[i] * Uy_EL_ref_II[j] +  KIII_tild[i] * Uy_EL_ref_III[j])
			dUz_PL = Uz_tot[j][i] - ( KI_tild[i] * Uz_EL_ref_I[j] + KII_tild[i] * Uz_EL_ref_II[j] +  KIII_tild[i] * Uz_EL_ref_III[j])	
			Ux_PLj.append(dUx_PL)
			Uy_PLj.append(dUy_PL)
			Uz_PLj.append(dUz_PL)
		Ux_PL.append(Ux_PLj) #champs plastiques totale
		Uy_PL.append(Uy_PLj)
		Uz_PL.append(Uz_PLj)
		del Ux_PLj, Uy_PLj, Uz_PLj
	return Ux_PL, Uy_PL, Uz_PL, KI_tild, KII_tild, KIII_tild


def Plastic_Field_Order_Dependent(test, mode_order, UrefEL, dimensions):
	dUx_tot = test.dUx_tot
	dUy_tot = test.dUy_tot
	dUz_tot = test.dUz_tot
	time_len= len(test.time)
	listN_F_len = dimensions.listN_F_len
	Ux_EL_ref_I   = eval('UrefEL.%s.x' % mode_order[0])
	Uy_EL_ref_I   = eval('UrefEL.%s.y' % mode_order[0])
	Uz_EL_ref_I   = eval('UrefEL.%s.z' % mode_order[0])
	Ux_EL_ref_II  = eval('UrefEL.%s.x' % mode_order[1])
	Uy_EL_ref_II  = eval('UrefEL.%s.y' % mode_order[1])
	Uz_EL_ref_II  = eval('UrefEL.%s.z' % mode_order[1])
	Ux_EL_ref_III = eval('UrefEL.%s.x' % mode_order[2])
	Uy_EL_ref_III = eval('UrefEL.%s.y' % mode_order[2])
	Uz_EL_ref_III = eval('UrefEL.%s.z' % mode_order[2])
	Norme_EL_I    = eval('UrefEL.%s.norme' % mode_order[0])
	Norme_EL_II   = eval('UrefEL.%s.norme' % mode_order[1])
	Norme_EL_III  = eval('UrefEL.%s.norme' % mode_order[2])
	KI_tild   =[]
	KII_tild  =[]
	KIII_tild =[]
	Ux_I_II_III = []
	Uy_I_II_III = []
	Uz_I_II_III = []
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
		for j in range(listN_F_len):
			dUx_int  = dUx_int_I_II[j] - KIIItild * Ux_EL_ref_III[j]
			dUy_int  = dUy_int_I_II[j] - KIIItild * Uy_EL_ref_III[j]
			dUz_int  = dUz_int_I_II[j] - KIIItild * Uz_EL_ref_III[j]
			dUx_int_I_II_III.append(dUx_int)
			dUy_int_I_II_III.append(dUy_int)
			dUz_int_I_II_III.append(dUz_int)
		Ux_I_II_III.append(dUx_int_I_II_III) #champs plastiques totale
		Uy_I_II_III.append(dUy_int_I_II_III)
		Uz_I_II_III.append(dUz_int_I_II_III)
	Ux_I_II_III = np.transpose(Ux_I_II_III)
	Uy_I_II_III = np.transpose(Uy_I_II_III)	
	Uz_I_II_III = np.transpose(Uz_I_II_III)
	'''
	Ux_PL =[]
	Uy_PL =[]
	Uz_PL =[]
	for j in range(listN_F_len):
		dUx_PL=0.
		dUy_PL=0.
		dUz_PL=0.
		Ux_PLj=[]
		Uy_PLj=[]
		Uz_PLj=[]
		for i in range(time_len-1):
			dUx_PL = dUx_tot[j][i] - ( KI_tild[i] * Ux_EL_ref_I[j] + KII_tild[i] * Ux_EL_ref_II[j] +  KIII_tild[i] * Ux_EL_ref_III[j]) #suppression du champ elastique au champ total
			dUy_PL = dUy_tot[j][i] - ( KI_tild[i] * Uy_EL_ref_I[j] + KII_tild[i] * Uy_EL_ref_II[j] +  KIII_tild[i] * Uy_EL_ref_III[j])
			dUz_PL = dUz_tot[j][i] - ( KI_tild[i] * Uz_EL_ref_I[j] + KII_tild[i] * Uz_EL_ref_II[j] +  KIII_tild[i] * Uz_EL_ref_III[j])
			Ux_PLj.append(dUx_PL)
			Uy_PLj.append(dUy_PL)
			Uz_PLj.append(dUz_PL)
		Ux_PL.append(Ux_PLj) #champs plastiques totale
		Uy_PL.append(Uy_PLj)
		Uz_PL.append(Uz_PLj)
		del Ux_PLj, Uy_PLj, Uz_PLj
	return Ux_PL, Uy_PL, Uz_PL, Ux_I_II_III, Uy_I_II_III, Uy_I_II_III, KI_tild, KII_tild, KIII_tild
	'''
	return Ux_I_II_III, Uy_I_II_III, Uz_I_II_III, KI_tild, KII_tild, KIII_tild



def Plastic_Field_Faces_Projection(test, UrefEL, dimensions):
	dUx_tot = test.dUx_tot
	dUy_tot = test.dUy_tot
	dUz_tot = test.dUz_tot
	listN_F_len = dimensions.listN_F_len
	rad_len     = dimensions.rad_len
	thet_len    = dimensions.thet_len
	time_len    = len(test.time)
	Ux_EL_ref_I     = UrefEL.I.x
	Uy_EL_ref_I     = UrefEL.I.y
	Uz_EL_ref_I     = UrefEL.I.z
	Ux_EL_ref_II    = UrefEL.II.x
	Uy_EL_ref_II    = UrefEL.II.y
	Uz_EL_ref_II    = UrefEL.II.z
	Ux_EL_ref_III   = UrefEL.III.x
	Uy_EL_ref_III   = UrefEL.III.y
	Uz_EL_ref_III   = UrefEL.III.z
	DUx_EL_Faces_I   = UrefEL.I.Delta_x
	DUy_EL_Faces_I   = UrefEL.I.Delta_y
	DUz_EL_Faces_I   = UrefEL.I.Delta_z
	DUx_EL_Faces_II  = UrefEL.II.Delta_x
	DUy_EL_Faces_II  = UrefEL.II.Delta_y
	DUz_EL_Faces_II  = UrefEL.II.Delta_z
	DUx_EL_Faces_III = UrefEL.III.Delta_x
	DUy_EL_Faces_III = UrefEL.III.Delta_y
	DUz_EL_Faces_III = UrefEL.III.Delta_z
	Norme_EL_I   = UrefEL.I.DU_norme
	Norme_EL_II  = UrefEL.II.DU_norme
	Norme_EL_III  = UrefEL.III.DU_norme
	KI_tild  =[]
	KII_tild =[]
	KIII_tild =[]
	for i in range(time_len-1):
		dKI_tild=0.
		dKII_tild=0.
		dKIII_tild=0.		
		for j in range(rad_len):
			j1 = j*thet_len
			j2 = (j+1)*thet_len-1
			dKI_tild   += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Faces_I[j] )   + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Faces_I[j] )   + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Faces_I[j] )   #projection du saut de deplacement totatl sur le saut de deplacement de reference
			dKII_tild  += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Faces_II[j] )  + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Faces_II[j] )  + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Faces_II[j] )
			dKIII_tild += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Faces_III[j] ) + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Faces_III[j] ) + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Faces_III[j] )
		KItild  = dKI_tild  / Norme_EL_I
		KI_tild.append(KItild)
		KIItild = dKII_tild / Norme_EL_II
		KII_tild.append(KIItild)
		KIIItild = dKIII_tild / Norme_EL_III
		KIII_tild.append(KIIItild)
	Ux_PL =[]
	Uy_PL =[]
	Uz_PL =[]
	for j in range(listN_F_len):
		dUx_PL=0.
		dUy_PL=0.
		dUz_PL=0.
		Ux_PLj=[]
		Uy_PLj=[]
		Uz_PLj=[]
		for i in range(time_len-1):
			dUx_PL = dUx_tot[j][i] - ( KI_tild[i] * Ux_EL_ref_I[j] + KII_tild[i] * Ux_EL_ref_II[j] +  KIII_tild[i] * Ux_EL_ref_III[j] ) #suppression du champ elastique au champ total
			dUy_PL = dUy_tot[j][i] - ( KI_tild[i] * Uy_EL_ref_I[j] + KII_tild[i] * Uy_EL_ref_II[j] +  KIII_tild[i] * Uy_EL_ref_III[j])
			dUz_PL = dUz_tot[j][i] - ( KI_tild[i] * Uz_EL_ref_I[j] + KII_tild[i] * Uz_EL_ref_II[j] +  KIII_tild[i] * Uz_EL_ref_III[j])	
			Ux_PLj.append(dUx_PL)
			Uy_PLj.append(dUy_PL)
			Uz_PLj.append(dUz_PL)
		Ux_PL.append(Ux_PLj) #champs plastiques totale
		Uy_PL.append(Uy_PLj)
		Uz_PL.append(Uz_PLj)
		del Ux_PLj, Uy_PLj, Uz_PLj
	return Ux_PL, Uy_PL, Uz_PL, KI_tild, KII_tild, KIII_tild




def Plastic_Field_Faces_Projection_Order_Dependent(test, mode_order, UrefEL, dimensions):
	dUx_tot = test.dUx_tot
	dUy_tot = test.dUy_tot
	dUz_tot = test.dUz_tot
	listN_F_len = dimensions.listN_F_len
	rad_len     = dimensions.rad_len
	thet_len    = dimensions.thet_len
	time_len    = len(test.time)
	Ux_EL_ref_I   = eval('UrefEL.%s.x' % mode_order[0])
	Uy_EL_ref_I   = eval('UrefEL.%s.y' % mode_order[0])
	Uz_EL_ref_I   = eval('UrefEL.%s.z' % mode_order[0])
	Ux_EL_ref_II  = eval('UrefEL.%s.x' % mode_order[1])
	Uy_EL_ref_II  = eval('UrefEL.%s.y' % mode_order[1])
	Uz_EL_ref_II  = eval('UrefEL.%s.z' % mode_order[1])
	Ux_EL_ref_III = eval('UrefEL.%s.x' % mode_order[2])
	Uy_EL_ref_III = eval('UrefEL.%s.y' % mode_order[2])
	Uz_EL_ref_III = eval('UrefEL.%s.z' % mode_order[2])
	DUx_EL_Faces_I   = eval('UrefEL.%s.Delta_x' % mode_order[0])
	DUy_EL_Faces_I   = eval('UrefEL.%s.Delta_y' % mode_order[0])
	DUz_EL_Faces_I   = eval('UrefEL.%s.Delta_z' % mode_order[0])
	DUx_EL_Faces_II  = eval('UrefEL.%s.Delta_x' % mode_order[1])
	DUy_EL_Faces_II  = eval('UrefEL.%s.Delta_y' % mode_order[1])
	DUz_EL_Faces_II  = eval('UrefEL.%s.Delta_z' % mode_order[1])
	DUx_EL_Faces_III = eval('UrefEL.%s.Delta_x' % mode_order[2])
	DUy_EL_Faces_III = eval('UrefEL.%s.Delta_y' % mode_order[2])
	DUz_EL_Faces_III = eval('UrefEL.%s.Delta_z' % mode_order[2])
	Norme_EL_I    = eval('UrefEL.%s.DU_norme' % mode_order[0])
	Norme_EL_II   = eval('UrefEL.%s.DU_norme' % mode_order[1])
	Norme_EL_III  = eval('UrefEL.%s.DU_norme' % mode_order[2])
	KI_tild   =[]
	KII_tild  =[]
	KIII_tild =[]
	Ux_I_II_III = []
	Uy_I_II_III = []
	Uz_I_II_III = []
	for i in range(time_len-1):
		dKI_tild=0.
		for j in range(rad_len):
			j1 = j*thet_len
			j2 = (j+1)*thet_len-1
			dKI_tild   += ( (dUx_tot[j2][i]-dUx_tot[j1][i]) * DUx_EL_Faces_I[j] )   + ( (dUy_tot[j2][i]-dUy_tot[j1][i]) * DUy_EL_Faces_I[j] )   + ( (dUz_tot[j2][i]-dUz_tot[j1][i]) * DUz_EL_Faces_I[j] )   #projection du saut de deplacement totatl sur le saut de deplacement de reference
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
			dUx_int_I += [dUx_int]
			dUy_int_I += [dUy_int]
			dUz_int_I += [dUz_int]
 		for j in range(rad_len):
			j1 = j*thet_len
			j2 = (j+1)*thet_len-1
			dKII_tild  += ( (dUx_int_I[j2]-dUx_int_I[j1]) * DUx_EL_Faces_II[j] )  + ( (dUy_int_I[j2]-dUy_int_I[j1]) * DUy_EL_Faces_II[j] )  + ( (dUz_int_I[j2]-dUz_int_I[j1]) * DUz_EL_Faces_II[j] )
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
			dUx_int_I_II += [dUx_int]
			dUy_int_I_II += [dUy_int]
			dUz_int_I_II += [dUz_int]
 		for j in range(rad_len):
			j1 = j*thet_len
			j2 = (j+1)*thet_len-1
			dKIII_tild += ( (dUx_int_I_II[j2]-dUx_int_I_II[j1]) * DUx_EL_Faces_III[j] )  + ( (dUy_int_I_II[j2]-dUy_int_I_II[j1]) * DUy_EL_Faces_III[j] )  + ( (dUz_int_I_II[j2]-dUz_int_I_II[j1]) * DUz_EL_Faces_III[j] )
		KIIItild = dKIII_tild / Norme_EL_III
		KIII_tild.append(KIIItild)
		dUx_int_I_II_III = []
		dUy_int_I_II_III = []		
		dUz_int_I_II_III = []
		for j in range(listN_F_len):
			dUx_int  = dUx_int_I_II[j] - KIIItild * Ux_EL_ref_III[j]
			dUy_int  = dUy_int_I_II[j] - KIIItild * Uy_EL_ref_III[j]
			dUz_int  = dUz_int_I_II[j] - KIIItild * Uz_EL_ref_III[j]
			dUx_int_I_II_III.append(dUx_int)
			dUy_int_I_II_III.append(dUy_int)
			dUz_int_I_II_III.append(dUz_int)
		Ux_I_II_III.append(dUx_int_I_II_III) #champs plastiques totale
		Uy_I_II_III.append(dUy_int_I_II_III)
		Uz_I_II_III.append(dUz_int_I_II_III)
	Ux_I_II_III = np.transpose(Ux_I_II_III)
	Uy_I_II_III = np.transpose(Uy_I_II_III)	
	Uz_I_II_III = np.transpose(Uz_I_II_III)
	return Ux_I_II_III, Uy_I_II_III, Uz_I_II_III, KI_tild, KII_tild, KIII_tild

