def Compute(mdb, test, job, Param, elastic, odbSrc):
# Test parameters:
	name          = test.get('name')		 #: EL_Rand, EL_Norm, EP	
	loading_type  = test.get('loading_type')         #: Loading type: imposed Force or Displacement
	KI_range      = test.get('KI_range')	         #: Range of KI nom
	KII_range     = test.get('KII_range')	         #: Range of KII nom
	KIII_range    = test.get('KIII_range')	         #: Range of KII nom
	NLGEOM        = test.get('NLGEOM')
# Job parameters:
	time_steps    = job.get('time_steps')
	max_Num_Inc   = job.get('max_num_inc')
	ini_inc       = job.get('ini_inc')
	min_inc       = job.get('min_inc')
	max_inc       = job.get('max_inc')         
	n_tot_steps   = job.get('n_tot_steps')
	n_act_steps   = job.get('n_act_steps')
	jobName, jobDescrip = Generate_names(test, elastic, odbSrc)
	if loading_type == 'Imposed_Force':
		for load in ['SUP_LEFT','SUP_RIGHT','INF_LEFT','INF_RIGHT']:
			mdb.models['Model-1'].loads[load].resume()
			mdb.models['Model-1'].boundaryConditions[load].suppress()
		mdb.models['Model-1'].boundaryConditions['Pointe-LEFT'].resume()
		mdb.models['Model-1'].boundaryConditions['Pointe-RIGHT'].resume()
		mdb.models['Model-1'].boundaryConditions['Ligament-RIGHT'].suppress()
		mdb.models['Model-1'].boundaryConditions['Line-LEFT'].suppress()
		mdb.models['Model-1'].boundaryConditions['Line-RIGHT'].resume()
		for stp in range(n_act_steps):
			dF1, dF2, dF3 = SIF_To_Force(KI_range[stp], KII_range[stp], KIII_range[stp], Param )
			step = 'Step-%d' %(stp+1)
			mdb.models['Model-1'].steps[step].resume()
			mdb.models['Model-1'].loads['SUP_RIGHT'].setValuesInStep(stepName=step , cf1=  dF1 , cf2=  dF1, cf3= -dF3 )
			mdb.models['Model-1'].loads['INF_LEFT'].setValuesInStep( stepName=step , cf1= -dF1 , cf2= -dF1, cf3=  dF3 )
			mdb.models['Model-1'].loads['SUP_LEFT'].setValuesInStep( stepName=step , cf1= -dF2 , cf2=  dF2, cf3= -dF3 )
			mdb.models['Model-1'].loads['INF_RIGHT'].setValuesInStep(stepName=step , cf1=  dF2 , cf2= -dF2, cf3=  dF3 )
			if NLGEOM :
				mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = ON)
			else :
				mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = OFF)
	elif loading_type == 'Imposed_Displacement':
		for load in ['SUP_LEFT','SUP_RIGHT','INF_LEFT','INF_RIGHT']:
			mdb.models['Model-1'].loads[load].suppress()
			mdb.models['Model-1'].boundaryConditions[load].resume()
		mdb.models['Model-1'].boundaryConditions['Pointe-LEFT'].suppress()
		mdb.models['Model-1'].boundaryConditions['Ligament-RIGHT'].suppress()
		mdb.models['Model-1'].boundaryConditions['Line-LEFT'].suppress()
		mdb.models['Model-1'].boundaryConditions['Line-RIGHT'].suppress()
		mdb.models['Model-1'].boundaryConditions['Pointe-RIGHT'].suppress()
		for stp in range(n_act_steps):
			dF1, dF2, dF3 = SIF_To_Force(KI_range[stp], KII_range[stp], KIII_range[stp], Param )
			step = 'Step-%d' %(stp+1)
			mdb.models['Model-1'].steps[step].resume()
			mdb.models['Model-1'].boundaryConditions['SUP_RIGHT'].setValuesInStep(stepName=step, u1=  dF1 , u2=  dF1 ,u3= -dF3 , ur1=FREED, ur2=FREED, ur3=FREED)
			mdb.models['Model-1'].boundaryConditions['INF_LEFT'].setValuesInStep( stepName=step, u1= -dF1 , u2= -dF1 ,u3=  dF3 , ur1=FREED, ur2=FREED, ur3=FREED)
			mdb.models['Model-1'].boundaryConditions['SUP_LEFT'].setValuesInStep( stepName=step, u1= -dF2 , u2=  dF2 ,u3= -dF3 , ur1=FREED, ur2=FREED, ur3=FREED)
			mdb.models['Model-1'].boundaryConditions['INF_RIGHT'].setValuesInStep(stepName=step, u1=  dF2 , u2= -dF2 ,u3=  dF3 , ur1=FREED, ur2=FREED, ur3=FREED)
			if NLGEOM :
				mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = ON)
			else :
				mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = OFF)
	for stp in range(n_act_steps+1,n_tot_steps+1):
		step = 'Step-%d' %stp
		mdb.models['Model-1'].steps[step].suppress()
	#: Crach history output for SIF determination
	#if name == 'EL_Norm':
	#	mdb.models['Model-1'].historyOutputRequests['CRACK-RIGHT-SIF'].resume()
	#else :
	#	mdb.models['Model-1'].historyOutputRequests['CRACK-RIGHT-SIF'].suppress()
	mdb.models['Model-1'].historyOutputRequests['LINE-DISP-RIGHT'].suppress()
	mdb.models['Model-1'].historyOutputRequests['FIELD-DISP-RIGHT'].suppress()
	mdb.models['Model-1'].historyOutputRequests['FACES-DISP-RIGHT'].suppress()
	mdb.models['Model-1'].historyOutputRequests['LIPS-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	mdb.models['Model-1'].historyOutputRequests['POINTE-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	mdb.models['Model-1'].historyOutputRequests['SECTION-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	#mdb.save()
	#: Create the Job
	print 'Create the Job'
	mdb.Job(name=jobName, model='Model-1', description=jobDescrip, type=ANALYSIS, 
		atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
		memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
		explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
		modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
		scratch='', multiprocessingMode=DEFAULT, numCpus=4, numDomains=4)
	#: Cree le fichier .inp
	mdb.jobs[jobName].writeInput()
	print '#: INP file generated'
	#print '#: Launch calculation'
	#: Lance le calcul et attends qu'il soit fini
	#mdb.jobs[jobName].submit()
	#mdb.jobs[jobName].waitForCompletion()
	#print '#: Simulation finished'
	#moveFiles(jobName, odbSrc)
	#if name == 'EP':
	#	odb=openOdb(path=os.path.join(odbSrc,jobName) + '.odb')
	#	Field_Capture(odb, odbSrc, jobName, 'PEEQ', 10, n_act_steps)    			# Capture and save the crack tip at each step end with a magnification factor = 10
	#	odb.close()
	#print 'Computation successfully finished '
	return jobName

