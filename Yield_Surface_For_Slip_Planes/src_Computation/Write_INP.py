def Create_INP_Initial_Loading(mdb, Model , test, job, Param, elastic):
# Test parameters:
	name          = test.get('name')		 #: EL_Rand, EL_Norm, EP	
	loading_type  = test.get('loading_type')         #: Loading type: imposed Force or Displacement
	test_type     = test.get('test_type')            
	KI_init_range   = test.get('KI_init_range')	         #: Range of KI nom
	KII_init_range  = test.get('KII_init_range')	         #: Range of KII nom
	KIII_init_range = test.get('KIII_init_range')	         #: Range of KII nom
	NLGEOM          = test.get('NLGEOM')
# Job parameters:
	time_steps    = job.get('time_steps')
	max_Num_Inc   = job.get('max_num_inc')
	ini_inc       = job.get('ini_inc')
	min_inc       = job.get('min_inc')
	max_inc       = job.get('max_inc')         
	n_tot_steps   = job.get('n_tot_steps')
	n_init_steps   = job.get('n_init_steps')
	Shkl = "%d%d%d" % (elastic.hkl[0],elastic.hkl[1],elastic.hkl[2])
	Suvw = "%d%d%d" % (elastic.uvw[0],elastic.uvw[1],elastic.uvw[2])
	suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)
	JobName = '%s_%s_%s_Init_KI_%d_KII_%d_KIII_%d' %(name, test_type, suffix, KI_init_range[-1], KII_init_range[-1], KIII_init_range[-1] )
	JobDescrip='%s plastic, cubic, %s, KI: %d , KII: %d , KIII: %d,loading type: %s' % ( test_type, suffix,  KI_init_range[-1], KII_init_range[-1], KIII_init_range[-1] , loading_type)
	if loading_type == 'Imposed_Force':
		for load in ['SUP_LEFT','SUP_RIGHT','INF_LEFT','INF_RIGHT']:
			mdb.models[Model].loads[load].resume()
			mdb.models[Model].boundaryConditions[load].suppress()
		mdb.models[Model].boundaryConditions['Pointe-LEFT'].resume()
		mdb.models[Model].boundaryConditions['Pointe-RIGHT'].resume()
		mdb.models[Model].boundaryConditions['Ligament-RIGHT'].suppress()
		mdb.models[Model].boundaryConditions['Line-LEFT'].suppress()
		mdb.models[Model].boundaryConditions['Line-RIGHT'].resume()
		for stp in range(n_init_steps):
			dF1, dF2, dF3 = SIF_To_Force(KI_init_range[stp], KII_init_range[stp], KIII_init_range[stp], Param )
			step = 'Step-%d' %(stp+1)
			mdb.models[Model].steps[step].resume()
			mdb.models[Model].loads['SUP_RIGHT'].setValuesInStep(stepName=step , cf1=  dF1 , cf2=  dF1, cf3= -dF3 )
			mdb.models[Model].loads['INF_LEFT'].setValuesInStep( stepName=step , cf1= -dF1 , cf2= -dF1, cf3=  dF3 )
			mdb.models[Model].loads['SUP_LEFT'].setValuesInStep( stepName=step , cf1= -dF2 , cf2=  dF2, cf3= -dF3 )
			mdb.models[Model].loads['INF_RIGHT'].setValuesInStep(stepName=step , cf1=  dF2 , cf2= -dF2, cf3=  dF3 )
			if NLGEOM :
				mdb.models[Model].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = ON)
			else :
				mdb.models[Model].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = OFF)
	mdb.models[Model].historyOutputRequests['LINE-DISP-RIGHT'].suppress()
	mdb.models[Model].historyOutputRequests['FIELD-DISP-RIGHT'].suppress()
	mdb.models[Model].historyOutputRequests['FACES-DISP-RIGHT'].suppress()
	mdb.models[Model].historyOutputRequests['LIPS-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	mdb.models[Model].historyOutputRequests['POINTE-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	mdb.models[Model].historyOutputRequests['SECTION-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	#mdb.save()
	#: Create the Job
	mdb.Job(name=JobName, model=Model, description=JobDescrip, type=ANALYSIS, 
		atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
		memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
		explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
		modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
		scratch='', multiprocessingMode=DEFAULT, numCpus=8, numDomains=8)
	#: Cree le fichier .inp
	mdb.jobs[JobName].writeInput()
	os.system('echo inp file %s Successfully written'  % (JobName))
	return JobName, JobDescrip



def Create_INP_Sec_Loading(mdb, Model , OldJobName, test, job, Param, elastic):
# Test parameters:
	name          = test.get('name')		 #: EL_Rand, EL_Norm, EP	
	loading_type  = test.get('loading_type')         #: Loading type: imposed Force or Displacement
	test_type     = test.get('test_type')            
	KI_sec  	  = test.get('KI_sec')	         #: Range of KI nom
	KII_sec 	  = test.get('KII_sec')	         #: Range of KII nom
	KIII_sec 	  = test.get('KIII_sec')	         #: Range of KII nom
	NLGEOM        = test.get('NLGEOM')
# Job parameters:
	time_steps    = job.get('time_steps')
	max_Num_Inc   = job.get('max_num_inc')
	ini_inc       = job.get('ini_inc')
	min_inc       = job.get('min_inc')
	max_inc       = job.get('max_inc')         
	n_tot_steps   = job.get('n_tot_steps')
	n_init_steps   = job.get('n_init_steps')
	Shkl = "%d%d%d" % (elastic.hkl[0],elastic.hkl[1],elastic.hkl[2])
	Suvw = "%d%d%d" % (elastic.uvw[0],elastic.uvw[1],elastic.uvw[2])
	suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)
	NewJobName = '%s_%s_%s_Sec_KI_%d_KII_%d_KIII_%d' %(name, test_type, suffix, KI_sec, KII_sec, KIII_sec )
	NewJobDescrip='Restart %s plastic, cubic, %s, KI: %d , KII: %d , KIII: %d,loading type: %s' % ( test_type, suffix,  KI_sec, KII_sec, KIII_sec , loading_type)
	if loading_type == 'Imposed_Force':
		for load in ['SUP_LEFT','SUP_RIGHT','INF_LEFT','INF_RIGHT']:
			mdb.models[Model].loads[load].resume()
			mdb.models[Model].boundaryConditions[load].suppress()
		mdb.models[Model].boundaryConditions['Pointe-LEFT'].resume()
		mdb.models[Model].boundaryConditions['Pointe-RIGHT'].resume()
		mdb.models[Model].boundaryConditions['Ligament-RIGHT'].suppress()
		mdb.models[Model].boundaryConditions['Line-LEFT'].suppress()
		mdb.models[Model].boundaryConditions['Line-RIGHT'].resume()
		dF1, dF2, dF3 = SIF_To_Force(KI_sec, KII_sec, KIII_sec, Param )
		step = 'Step-%d' %( n_init_steps + 1 )
		mdb.models[Model].steps[step].resume()
		mdb.models[Model].loads['SUP_RIGHT'].setValuesInStep(stepName=step , cf1=  dF1 , cf2=  dF1, cf3= -dF3 )
		mdb.models[Model].loads['INF_LEFT'].setValuesInStep( stepName=step , cf1= -dF1 , cf2= -dF1, cf3=  dF3 )
		mdb.models[Model].loads['SUP_LEFT'].setValuesInStep( stepName=step , cf1= -dF2 , cf2=  dF2, cf3= -dF3 )
		mdb.models[Model].loads['INF_RIGHT'].setValuesInStep(stepName=step , cf1=  dF2 , cf2= -dF2, cf3=  dF3 )
		if NLGEOM :
			mdb.models[Model].steps[step].setValues(timePeriod=time_steps[-1], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = ON)
		else :
			mdb.models[Model].steps[step].setValues(timePeriod=time_steps[-1], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = OFF)
	mdb.models[Model].historyOutputRequests['LINE-DISP-RIGHT'].suppress()
	mdb.models[Model].historyOutputRequests['FIELD-DISP-RIGHT'].suppress()
	mdb.models[Model].historyOutputRequests['FACES-DISP-RIGHT'].suppress()
	mdb.models[Model].historyOutputRequests['LIPS-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	mdb.models[Model].historyOutputRequests['POINTE-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	mdb.models[Model].historyOutputRequests['SECTION-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
	#mdb.save()
	#: Create the Job
	last_step = 'Step-%d' % n_init_steps
	mdb.models[ Model ].setValues(restartJob=OldJobName , restartStep= last_step )
	mdb.Job(name=NewJobName, model=Model, description=NewJobDescrip, type=RESTART, 
		atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
		memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
		explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
		modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
		scratch='', multiprocessingMode=DEFAULT, numCpus=8, numDomains=8)
	#: Cree le fichier .inp
	mdb.jobs[NewJobName].writeInput()
	os.system('echo inp file %s Successfully written'  % (NewJobName))
	return NewJobName, NewJobDescrip
