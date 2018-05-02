def Compute_cyclic(mdb, test, job, Param, elastic, odbSrc):
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
	n_cylces      = job.get('n_cycles')
	jobName, jobDescrip = Generate_names(test, elastic, odbSrc)
	for load in ['SUP_LEFT','SUP_RIGHT','INF_LEFT','INF_RIGHT']:
		mdb.models['Model-1'].loads[load].resume()
		mdb.models['Model-1'].boundaryConditions[load].suppress()
	mdb.models['Model-1'].boundaryConditions['Pointe-LEFT'].resume()
	mdb.models['Model-1'].boundaryConditions['Pointe-RIGHT'].resume()
	mdb.models['Model-1'].boundaryConditions['Ligament-RIGHT'].suppress()
	mdb.models['Model-1'].boundaryConditions['Line-LEFT'].suppress()
	mdb.models['Model-1'].boundaryConditions['Line-RIGHT'].resume()
	## Initial Step
	dF1_init, dF2_init, dF3_init = SIF_To_Force(KI_range[0], KII_range[0], KIII_range[0], Param )
	step = 'Step-1'
	mdb.models['Model-1'].steps[step].resume()
	mdb.models['Model-1'].loads['SUP_RIGHT'].setValuesInStep(stepName=step , cf1=  dF1_init , cf2=  dF1_init, cf3= -dF3_init )
	mdb.models['Model-1'].loads['INF_LEFT'].setValuesInStep( stepName=step , cf1= -dF1_init , cf2= -dF1_init, cf3=  dF3_init )
	mdb.models['Model-1'].loads['SUP_LEFT'].setValuesInStep( stepName=step , cf1= -dF2_init , cf2=  dF2_init, cf3= -dF3_init )
	mdb.models['Model-1'].loads['INF_RIGHT'].setValuesInStep(stepName=step , cf1=  dF2_init , cf2= -dF2_init, cf3=  dF3_init )
	if NLGEOM :
		mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[0], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = ON)
	else :
		mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[0], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = OFF)
	## Cyclic step
	dF1_cyc, dF2_cyc, dF3_cyc = SIF_To_Force(KI_range[1], KII_range[1], KIII_range[1], Param )
	#a0_dF1, a0_dF2, a0_dF3 = SIF_To_Force(sum(KI_range), sum(KII_range), sum(KIII_range), Param )
	step = 'Step-2'
	mdb.models['Model-1'].steps[step].resume()
	a = mdb.models['Model-1'].rootAssembly
	r1 = a.referencePoints
	refPoints1=(r1[13], )
	region = regionToolset.Region(referencePoints=refPoints1)
	mdb.models['Model-1'].ConcentratedForce(name='SUP_RIGHT_III', createStepName='Step-2', region=region, cf1= 0., cf2= 0., cf3 =-1.0 )
	refPoints1=(r1[15], )
	region = regionToolset.Region(referencePoints=refPoints1)
	mdb.models['Model-1'].ConcentratedForce(name='INF_LEFT_III', createStepName='Step-2', region=region, cf1= 0., cf2= 0., cf3 = 1.0 )
	refPoints1=(r1[12], )
	region = regionToolset.Region(referencePoints=refPoints1)
	mdb.models['Model-1'].ConcentratedForce(name='SUP_LEFT_III', createStepName='Step-2', region=region, cf1= 0., cf2= 0., cf3 =-1.0 )
	refPoints1=(r1[14], )
	region = regionToolset.Region(referencePoints=refPoints1)
	mdb.models['Model-1'].ConcentratedForce(name='INF_RIGHT_III', createStepName='Step-2', region=region, cf1= 0., cf2= 0., cf3 = 1.0 )
	T = float(time_steps[1])/float(n_cylces)
	circular_freq = 2*np.pi/T
	a0_dF1 = dF1_init + dF1_cyc
	a0_dF2 = dF2_init + dF2_cyc
	a0_dF3 = dF3_init + dF3_cyc
	mdb.models['Model-1'].PeriodicAmplitude(name='Amp_F1', timeSpan=STEP, frequency=circular_freq , start=0. , a_0=a0_dF1 , data=((0., dF1_cyc), ))
	mdb.models['Model-1'].PeriodicAmplitude(name='Amp_F2', timeSpan=STEP, frequency=circular_freq , start=0. , a_0=a0_dF2 , data=((0., dF2_cyc), ))		
	mdb.models['Model-1'].PeriodicAmplitude(name='Amp_F3', timeSpan=STEP, frequency=circular_freq , start=0. , a_0=a0_dF3 , data=((0., dF3_cyc), ))		
	mdb.models['Model-1'].loads['SUP_RIGHT'].setValuesInStep(     stepName=step , cf1=  1. , cf2=  1. , cf3= 0. , amplitude='Amp_F1' )
	mdb.models['Model-1'].loads['SUP_RIGHT_III'].setValuesInStep( stepName=step , cf1=  0. , cf2=  0. , cf3=-1. , amplitude='Amp_F3' )
	mdb.models['Model-1'].loads['INF_LEFT'].setValuesInStep(      stepName=step , cf1= -1. , cf2= -1. , cf3= 0. , amplitude='Amp_F1' )
	mdb.models['Model-1'].loads['INF_LEFT_III'].setValuesInStep(  stepName=step , cf1=  0. , cf2=  0. , cf3= 1. , amplitude='Amp_F3' )
	mdb.models['Model-1'].loads['SUP_LEFT'].setValuesInStep(      stepName=step , cf1= -1. , cf2=  1. , cf3= 0. , amplitude='Amp_F2' )
	mdb.models['Model-1'].loads['SUP_LEFT_III'].setValuesInStep(  stepName=step , cf1=  0. , cf2=  0. , cf3=-1. , amplitude='Amp_F3' )
	mdb.models['Model-1'].loads['INF_RIGHT'].setValuesInStep(     stepName=step , cf1=  1. , cf2= -1. , cf3= 0. , amplitude='Amp_F2' )
	mdb.models['Model-1'].loads['INF_RIGHT_III'].setValuesInStep( stepName=step , cf1=  0. , cf2=  0. , cf3= 1. , amplitude='Amp_F3' )
	if NLGEOM :
		mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[1], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = ON)
	else :
		mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[1], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = OFF)
	for stp in range(n_act_steps+1,n_tot_steps+1):
		step = 'Step-%d' %stp
		mdb.models['Model-1'].steps[step].suppress()
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
		scratch='', multiprocessingMode=DEFAULT, numCpus=12, numDomains=12)
	#: Cree le fichier .inp
	mdb.jobs[jobName].writeInput()
	print '#: INP file generated'
	return jobName, jobDescrip
