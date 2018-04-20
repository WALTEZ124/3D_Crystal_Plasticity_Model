# -*- coding: utf-8 -*-
def Extract_EL_Disp_Field_Output(odb, dimensions, coef):
	listN_F_unsorted = dimensions.listN_F_unsorted
	listN_F_sorted   = dimensions.listN_F_sorted
	print '   #: Extrait les deplacements des noeuds '
	step=odb.steps['Step-1']
	setname = 'POINTE-RIGHT'
	POINTE_RIGHT = odb.rootAssembly.nodeSets[setname]
	USubField = step.frames[-1].fieldOutputs['U'].getSubset(region=POINTE_RIGHT)
	Uxpointe = USubField.values[0].data[0] 
	Uypointe = USubField.values[0].data[1] 
	Uzpointe = USubField.values[0].data[2] 
	setname = 'FIELD-DISP-RIGHT'
	print '      #: Node Set Name=', setname
	FIELD_RIGHT = odb.rootAssembly.nodeSets[setname]
	USubField = step.frames[-1].fieldOutputs['U'].getSubset(region=FIELD_RIGHT)
	Ux_EL=[]
	Uy_EL=[]
	Uz_EL=[]
	for i,label in enumerate(listN_F_sorted):
		ind = listN_F_unsorted.index(label)
		Ux = USubField.values[ind].data[0] 
		Uy = USubField.values[ind].data[1] 
		Uz = USubField.values[ind].data[2] 
		Ux_EL += [ (Ux-Uxpointe)*coef ]			# !! if KII = -1 MP m-0.5 (left shear), the displacement field should be reversed.
		Uy_EL += [ (Uy-Uypointe)*coef ]
		Uz_EL += [ (Uz-Uzpointe)*coef ]
	return Ux_EL, Uy_EL, Uz_EL


def Extract_EL_Disp_History_Output(odb, dimensions, coef):
	listN_F_sorted   = dimensions.listN_F_sorted
	listN_TIP        = dimensions.listN_TIP
	print '   #: Extrait les deplacements des noeuds '
	step=odb.steps['Step-1']
	word='Node PART-1-1.%d' % listN_TIP[0]
	region=step.historyRegions[word]
	dep=region.historyOutputs['U1'].data
	Uxpointe=dep[-1][1]
	dep=region.historyOutputs['U2'].data
	Uypointe=dep[-1][1]
	dep=region.historyOutputs['U3'].data
	Uzpointe=dep[-1][1]
	#: Extracting Elastic displacement
	Ux_EL=[]
	Uy_EL=[]
	Uz_EL=[]
	for i,index in enumerate(listN_F_sorted):
	    word='Node PART-1-1.%d' % index
	    region=step.historyRegions[word]
	    dep=region.historyOutputs['U1'].data
	    ux=coef*(dep[-1][1]-Uxpointe)
	    dep=region.historyOutputs['U2'].data
	    uy=coef*(dep[-1][1]-Uypointe)
	    dep=region.historyOutputs['U3'].data
	    uz=coef*(dep[-1][1]-Uzpointe)
	    Ux_EL += [ ux ]			# !! if KII = -1 MP m-0.5 (left shear), the displacement field should be reversed.
	    Uy_EL += [ uy ]
	    Uz_EL += [ uz ]
#	odb.close()
	return Ux_EL, Uy_EL, Uz_EL

