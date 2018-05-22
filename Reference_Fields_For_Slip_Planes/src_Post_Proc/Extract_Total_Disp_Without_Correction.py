# -*- coding: utf-8 -*-
def Extract_Total_Disp_Field_Output(odb, step, dimensions):
	listN_F_unsorted = dimensions.listN_F_unsorted
	listN_F_sorted   = dimensions.listN_F_sorted
	print '   #: Extrait les deplacements des noeuds '
	step=odb.steps[step]	
	setname = 'POINTE-RIGHT'
	POINTE_RIGHT = odb.rootAssembly.nodeSets[setname]
	setname = 'FIELD-DISP-RIGHT'
	FIELD_RIGHT = odb.rootAssembly.nodeSets[setname]
	Ux_tot=[]
	Uy_tot=[]
	Uz_tot=[]
	n_increments = step.frames[-1].frameId
	timePeriod   = step.timePeriod
	list_increments = np.linspace(0,timePeriod, timePeriod/dimensions.time_inc + 1)      #  Multiply by 10 because I extract results each 0.1 time increment
	time = []
	for f in range(n_increments+1) :
		frameValue = round(step.frames[f].frameValue,2)
		if frameValue in list_increments :
			time +=[frameValue]
			USubField = step.frames[f].fieldOutputs['U'].getSubset(region=POINTE_RIGHT)
			Uxpointe = USubField.values[0].data[0] 
			Uypointe = USubField.values[0].data[1] 
			Uzpointe = USubField.values[0].data[2] 
			USubField = step.frames[f].fieldOutputs['U'].getSubset(region=FIELD_RIGHT)
			elemx=[]
			elemy=[]
			elemz=[]
			for i,label in enumerate(listN_F_sorted):
				ind = listN_F_unsorted.index(label)
				Ux = USubField.values[ind].data[0] 
				Uy = USubField.values[ind].data[1] 
				Uz = USubField.values[ind].data[2] 
				elemx += [ Ux-Uxpointe ]			# !! if KII = -1 MP m-0.5 (left shear), the displacement field should be reversed.
				elemy += [ Uy-Uypointe ]
				elemz += [ Uz-Uzpointe ]
			Ux_tot.append(elemx)
			Uy_tot.append(elemy)
			Uz_tot.append(elemz)
	Ux_tot = np.asarray(Ux_tot)
	Uy_tot = np.asarray(Uy_tot)
	Uz_tot = np.asarray(Uz_tot)
	dUx_tot = [ Ux_tot[i+1][:] - Ux_tot[i][:] for i in range(len(time)-1) ]
	dUy_tot = [ Uy_tot[i+1][:] - Uy_tot[i][:] for i in range(len(time)-1) ]
	dUz_tot = [ Uz_tot[i+1][:] - Uz_tot[i][:] for i in range(len(time)-1) ]
	dUx_tot = np.transpose(dUx_tot)
	dUy_tot = np.transpose(dUy_tot)
	dUz_tot = np.transpose(dUz_tot)
	return time, dUx_tot, dUy_tot, dUz_tot



# -*- coding: utf-8 -*-
def Extract_Total_Disp_History_Output(odb, step, dimensions):
	listN_F_sorted   = dimensions.listN_F_sorted
	listN_TIP        = dimensions.listN_TIP
	step=odb.steps[step]
	#Extraction des deplacements dans la Zone d'etude
	print 'Extract total displacement fields'
	#: extraction du deplacement de la pointe
	word='Node PART-1-1.%d' % listN_TIP[0]
	#: U1, U2 pointe
	region=step.historyRegions[word]
	x0=region.historyOutputs['U1'].data
	y0=region.historyOutputs['U2'].data
	z0=region.historyOutputs['U3'].data
	time=[]
	dlong=len(x0)
	depxpointe=[]
	depypointe=[]
	depzpointe=[]
	for i in range(dlong):
		depxpointe += [x0[i][1]]
		depypointe += [y0[i][1]]
		depzpointe += [z0[i][1]]
		time       += [x0[i][0]]
	del x0, y0, z0, region,word
	#  Determination of the rotation correction using crack lips displacement
	dUx_tot=[]
	dUy_tot=[]
	dUz_tot=[]
	for j,index in enumerate(listN_F_sorted):
		#: extraction du deplacement des noeuds
		word='Node PART-1-1.%d' % index
		region=step.historyRegions[word]
		#: U1 noeud j
		x0=region.historyOutputs['U1'].data
		y0=region.historyOutputs['U2'].data
		z0=region.historyOutputs['U3'].data
		dlong=len(x0)
		depxp=[]
		depyp=[]
		depzp=[]
		for i in range(dlong):
			ux = x0[i][1] - depxpointe[i]							# Displacement on x direct of the node j
			uy = y0[i][1] - depypointe[i]							# Displacement on y direct of the node j
			uz = z0[i][1] - depzpointe[i]							# Displacement on y direct of the node j
			depxp += [ ux ]
			depyp += [ uy ]
			depzp += [ uz ]
		del x0, y0, z0, word, region
		#: enregistrement dans des tables Uxtot et Uytot des deplacements totaux
		elemx=[]
		elemy=[]
		elemz=[]
		for i in range(len(time)-1):
			uxp= ( depxp[i+1] - depxp[i] ) #Calcul des deplacements pour chaque pas de temps  
			uyp= ( depyp[i+1] - depyp[i] )	  	
			uzp= ( depzp[i+1] - depzp[i] )	  	
			elemx.append(uxp)
			elemy.append(uyp)
			elemz.append(uzp)
		dUx_tot.append(elemx)
		dUy_tot.append(elemy)
		dUz_tot.append(elemz)
	return time, dUx_tot, dUy_tot, dUz_tot


# -*- coding: utf-8 -*-
def Extract_Cumulated_Strain_Field_Output(odb, step, dimensions):
	listN_F_unsorted = dimensions.listN_F_unsorted
	listN_F_sorted   = dimensions.listN_F_sorted
	listN_F_len      = dimensions.listN_F_len
	print '   #: Extrait les deplacements des noeuds '
	step=odb.steps[step]	
	setname = 'POINTE-RIGHT'
	POINTE_RIGHT = odb.rootAssembly.nodeSets[setname]
	setname = 'SECTION-RIGHT'
	SECTION_RIGHT = odb.rootAssembly.elementSets[setname]
	n_increments = step.frames[-1].frameId
	timePeriod   = step.timePeriod
	list_increments = np.linspace(0,timePeriod, timePeriod/dimensions.time_inc + 1)      #  Multiply by 10 because I extract results each 0.1 time increment
	time = []
	EV1_Cum_moy = []
	EV1_Cum_quad = []	
	EV1_Cum_tot = []
	for f in range(n_increments+1) :
		frameValue = round(step.frames[f].frameValue,2)
		if frameValue in list_increments :
			time +=[frameValue]
			USubField = step.frames[f].fieldOutputs['SDV14'].getSubset(region=SECTION_RIGHT)
			EV1_Cum=[]
			for i,label in enumerate(listN_F_sorted):
				ind = listN_F_unsorted.index(label)
				EV1_Cum += [ USubField.values[ind].data]
			EV1_Cum_moy+= [np.mean(EV1_Cum)]
			EV1_Cum_quad += [np.linalg.norm(EV1_Cum)/np.sqrt(listN_F_len)]
			#os.system('echo %f' % moy )
			EV1_Cum_tot.append(EV1_Cum)
	EV1_Cum_tot = np.asarray(EV1_Cum_tot)
	EV1_Cum_tot = np.transpose(EV1_Cum_tot)
	return time, EV1_Cum_tot, EV1_Cum_moy, EV1_Cum_quad

def Extract_All_Cumulated_Strain_Field_Output(odb, step, dimensions):
	listN_F_unsorted = dimensions.listN_F_unsorted
	listN_F_sorted   = dimensions.listN_F_sorted
	listN_F_len      = dimensions.listN_F_len
	print '   #: Extrait les deplacements des noeuds '
	step=odb.steps[step]	
	setname = 'POINTE-RIGHT'
	POINTE_RIGHT = odb.rootAssembly.nodeSets[setname]
	setname = 'SECTION-RIGHT'
	SECTION_RIGHT = odb.rootAssembly.elementSets[setname]
	n_increments = step.frames[-1].frameId
	timePeriod   = step.timePeriod
	list_increments = np.linspace(0,timePeriod, timePeriod/dimensions.time_inc + 1)      #  Multiply by 10 because I extract results each 0.1 time increment
	EV_Cum_tot_moy  = []
	EV_Cum_tot_quad = []
	for s in range(12):
		time = []
		EV_Cum_moy = []
		EV_Cum_quad = []	
		for f in range(n_increments+1) :
			frameValue = round(step.frames[f].frameValue,2)
			if frameValue in list_increments :
				time +=[frameValue]
				var = 'SDV%d' % (25+s)
				USubField = step.frames[f].fieldOutputs[var].getSubset(region=SECTION_RIGHT)
				EV_Cum=[]
				for i,label in enumerate(listN_F_sorted):
					ind = listN_F_unsorted.index(label)
					EV_Cum += [ USubField.values[ind].data]
				EV_Cum_moy+= [np.mean(EV_Cum)]
				EV_Cum_quad += [np.linalg.norm(EV_Cum)/np.sqrt(listN_F_len)]
				#os.system('echo %f' % moy )
		EV_Cum_tot_moy.append(EV_Cum_moy)
		EV_Cum_tot_quad.append(EV_Cum_quad)
	EV_Cum_tot_moy  = np.asarray(EV_Cum_tot_moy)
	EV_Cum_tot_moy = np.transpose(EV_Cum_tot_moy)
	EV_Cum_tot_quad = np.asarray(EV_Cum_tot_quad)
	EV_Cum_tot_quad = np.transpose(EV_Cum_tot_quad)	
	return time, EV_Cum_tot_moy, EV_Cum_tot_quad
