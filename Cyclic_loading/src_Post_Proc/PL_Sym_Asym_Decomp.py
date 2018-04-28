def PL_Sym_Asym_Decomp(Ux_PL, Uy_PL, temps, radlong, half_thetalong):
	Ux_PL_SYM  =[]
	Uy_PL_SYM  =[]
	Ux_PL_ASYM =[]
	Uy_PL_ASYM =[]
	for i in range(len(temps)-1): 
		Ux_PL_I  =[]
		Uy_PL_I  =[]
		Ux_PL_II =[]
		Uy_PL_II =[]
		for r in range(radlong) :
			for j in range(half_thetalong) :
				pos_index = r*thetalong + j
				neg_index = (r+1)*thetalong - j -1
				UxI = ( Ux_PL[pos_index][i]  + Ux_PL[neg_index][i] )/2
				Ux_PL_I  += [UxI]	
				UyI = ( Uy_PL[pos_index][i]  - Uy_PL[neg_index][i] )/2	
				Uy_PL_I += [UyI]	
				UxII = ( Ux_PL[pos_index][i] - Ux_PL[neg_index][i] )/2
				Ux_PL_II += [UxII]	
				UyII = ( Uy_PL[pos_index][i] + Uy_PL[neg_index][i] )/2	
				Uy_PL_II += [UyII]	
			index = r*thetalong + half_thetalong
			UxI = Ux_PL[index][i]	
			Ux_PL_I  += [UxI]
			UyI = 0.0	
			Uy_PL_I += [UyI]
			UxII = 0.0	
			Ux_PL_II += [UxII]
			UyII = Uy_PL[index][i]
			Uy_PL_II += [UyII]
			for j in range(half_thetalong) :
				inv_index = r*thetalong + half_thetalong - j - 1 
				UxI  = Ux_PL_I[inv_index]
				Ux_PL_I += [UxI]	
				UyI  = - Uy_PL_I[inv_index]
				Uy_PL_I += [UyI]
				UxII = - Ux_PL_II[inv_index]
				Ux_PL_II += [UxII]	
				UyII = Uy_PL_II[inv_index]
				Uy_PL_II += [UyII]
		Ux_PL_SYM.append(Ux_PL_I)
		Uy_PL_SYM.append(Uy_PL_I)	
		Ux_PL_ASYM.append(Ux_PL_II)
		Uy_PL_ASYM.append(Uy_PL_II)	
	Ux_PL_SYM  = transpose(Ux_PL_SYM)
	Uy_PL_SYM  = transpose(Uy_PL_SYM)
	Ux_PL_ASYM = transpose(Ux_PL_ASYM)
	Uy_PL_ASYM = transpose(Uy_PL_ASYM)
	return Ux_PL_SYM, Uy_PL_SYM, Ux_PL_ASYM, Uy_PL_ASYM