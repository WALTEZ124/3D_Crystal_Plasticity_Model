# -*- coding: utf-8 -*-
def EL_Sym_Asym_Decomp(Ux_EL, Uy_EL, Uz_EL, rad_len, thet_len, z_len):
	Ux_I   = zeros([z_len, rad_len, thet_len])
	Uy_I   = zeros([z_len, rad_len, thet_len])	
	Uz_I   = zeros([z_len, rad_len, thet_len])
	Ux_II  = zeros([z_len, rad_len, thet_len])
	Uy_II  = zeros([z_len, rad_len, thet_len])	
	Uz_II  = zeros([z_len, rad_len, thet_len])
	Ux_III = zeros([z_len, rad_len, thet_len])
	Uy_III = zeros([z_len, rad_len, thet_len])	
	Uz_III = zeros([z_len, rad_len, thet_len])
	Ux_EL_array = np.asarray(Ux_EL)
	Uy_EL_array = np.asarray(Uy_EL)
	Uz_EL_array = np.asarray(Uz_EL)
	Ux_mat = Ux_EL_array.reshape(z_len, rad_len, thet_len)
	Uy_mat = Uy_EL_array.reshape(z_len, rad_len, thet_len)
	Uz_mat = Uz_EL_array.reshape(z_len, rad_len, thet_len)
	half_thet_len = int(thet_len/2) + 1
	for z in range(z_len):
		for r in range(rad_len) :
			for thet in range(half_thet_len) :
				# Mode I
				ux_sym = (Ux_mat[z][r][thet] + Ux_mat[z][r][-thet-1])/2
				Ux_I[z][r][thet] = ux_sym				
				Ux_I[z][r][-thet-1] = ux_sym
				uy_asym = (Uy_mat[z][r][thet] - Uy_mat[z][r][-thet-1])/2
				Uy_I[z][r][thet] = uy_asym
				Uy_I[z][r][-thet-1] = -uy_asym
				# Mode II
				ux_asym = (Ux_mat[z][r][thet] - Ux_mat[z][r][-thet-1])/2
				Ux_II[z][r][thet] = ux_asym
				Ux_II[z][r][-thet-1] = -ux_asym				
				uy_sym = (Uy_mat[z][r][thet] + Uy_mat[z][r][-thet-1])/2
				Uy_II[z][r][thet] = uy_sym
				Uy_II[z][r][-thet-1] = uy_sym
				# Mode III
				uz_aplan = (Uz_mat[z][r][thet] - Uz_mat[z][r][-thet-1])/2
				Uz_III[z][r][thet] = uz_aplan
				Uz_III[z][r][-thet-1] = -uz_aplan
	print 'Symmetric/Skew-Symmetric/Anti-plane decomposition done'
	return Ux_I, Uy_I, Uz_I, Ux_II, Uy_II, Uz_II, Ux_III, Uy_III, Uz_III
