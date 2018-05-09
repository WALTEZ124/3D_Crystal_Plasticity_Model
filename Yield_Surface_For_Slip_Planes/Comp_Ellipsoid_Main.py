# -*- coding: utf-8 -*-


#---------------------------------------------------------------------------------
#          Call functions
#---------------------------------------------------------------------------------

srcFile = os.path.join(compSrc, 'moveFiles_func.py')
execfile(srcFile)

srcFile = os.path.join(compSrc,'Material_Config.py')
execfile(srcFile)

srcFile = os.path.join(compSrc,'SIF_To_Force.py')
execfile(srcFile)

#---------------------------------------------------------------------------------
#          Create model
#---------------------------------------------------------------------------------

srcFile =os.path.join(compSrc,'Model_Circular_Partition.py')
execfile(srcFile)
# Pour l'affichage des masques dans le fichier rpy
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

#----------------------------------------------------------------------------------
# Job parameters :
#----------------------------------------------------------------------------------

Pi=np.arccos(-1.)

n_increment = 40		# number of increments by step

KI_Center  = [ 2, 2, 2, 2, 4, 4, 4, 4, 6., 6., 6., 6.]
KII_Center = np.zeros(len(KI_Center)).tolist()
KIII_Center = np.zeros(len(KI_Center)).tolist()

KI_Yield = KI_Center
n_tot_steps = len(KI_Center)


#Ellip_ratio_I_II  = 2.08  # For isotropic materials and nu_poisson = 0.3
#Ellip_ratio_I_III = 2.56  # For isotropic materials and nu_poisson = 0.3

Ellip_ratio_I_II  = 2.1  # For 010 100
Ellip_ratio_I_III = 2.5  # For 010 100

PL_Ellipse_Job  = {  'n_tot_steps' :  n_tot_steps, 'time_steps' : [ 10 for i in range(n_tot_steps) ] , 'max_num_inc': 800, 'ini_inc' : dimensions.time_inc , 'min_inc' : 1e-7, 'max_inc' : 4 }

Job = Container()
Job.Ellipse = Container()


#----------------------------------------------------------------------------------
#                Parameters relating loading to nominals SIF 
#----------------------------------------------------------------------------------

file2=open(os.path.join(compSrc, 'Parameters_F_To_K_nominals_%s.p' %  suffix ),'rb')
Param = pickle.load(file2)
file2.close()


#:------------------------------------
# Defining plasticity
#:------------------------------------

elastic = Elastic( eType = elasticity_type)
plastic = Plastic (pType = hardening_type)
mdb = Material_Config(mdb, 'Model-1',  elastic, plastic)


# Test parameters:
PL_Ellipse_Test  = { 'name' : 'EP', 'test_type' : 'Ellipse', 'loading_type' : loading_type, 
					'KI_Center' : KI_Center , 'KII_Center' : KII_Center, 
					'KIII_Center' : KIII_Center, 'KI_Yield' : KI_Yield, 
					'Ellip_ratio_I_II' : Ellip_ratio_I_II, 'Ellip_ratio_I_III' : Ellip_ratio_I_III, 
					'n_increment': n_increment, 'NLGEOM': False }


a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[13], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='SUP_RIGHT_III', createStepName='Step-1', region=region, cf1= 0., cf2= 0., cf3 =-1.0 )
refPoints1=(r1[15], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='INF_LEFT_III', createStepName='Step-1', region=region, cf1= 0., cf2= 0., cf3 = 1.0 )
refPoints1=(r1[12], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='SUP_LEFT_III', createStepName='Step-1', region=region, cf1= 0., cf2= 0., cf3 =-1.0 )
refPoints1=(r1[14], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='INF_RIGHT_III', createStepName='Step-1', region=region, cf1= 0., cf2= 0., cf3 = 1.0 )



test = PL_Ellipse_Test
job  = PL_Ellipse_Job



# Test parameters:
name          = test.get('name')		 #: EL_Rand, EL_Norm, EP	
loading_type  = test.get('loading_type')         #: Loading type: imposed Force or Displacement
KI_Center     = test.get('KI_Center')	         #: Range of KI Centers
KII_Center    = test.get('KII_Center')	         #: Range of KII Centers
KIII_Center   = test.get('KIII_Center')	         #: Range of KII Centers
KI_Yield      = test.get('KI_Yield')	         #: Range of KI Yield
r_I_II        = test.get('Ellip_ratio_I_II')
r_I_III       = test.get('Ellip_ratio_I_III')
NLGEOM        = test.get('NLGEOM')
n_increment	  = test.get('n_increment')
test_type     = test.get('test_type')
# Job parameters:
time_steps    = job.get('time_steps')
max_Num_Inc   = job.get('max_num_inc')
ini_inc       = job.get('ini_inc')
min_inc       = job.get('min_inc')
max_inc       = job.get('max_inc')         
n_tot_steps   = job.get('n_tot_steps')
jobName = '%s_%s_%s_Center_I_%d_II_%d_III_%d' %(name, test_type, suffix, KI_Center[-1], KII_Center[-1], KIII_Center[-1] )
jobDescrip='%s plastic, material orientation : %s, loading type: %s' % ( test_type, suffix, loading_type)
if loading_type == 'Imposed_Force':
	for load in ['SUP_LEFT','SUP_RIGHT','INF_LEFT','INF_RIGHT']:
		mdb.models['Model-1'].loads[load].resume()
		mdb.models['Model-1'].boundaryConditions[load].suppress()
	mdb.models['Model-1'].boundaryConditions['Pointe-LEFT'].resume()
	mdb.models['Model-1'].boundaryConditions['Pointe-RIGHT'].resume()
	mdb.models['Model-1'].boundaryConditions['Ligament-RIGHT'].suppress()
	mdb.models['Model-1'].boundaryConditions['Line-LEFT'].suppress()
	mdb.models['Model-1'].boundaryConditions['Line-RIGHT'].resume()	
	KI_nom   = []
	KII_nom  = []
	KIII_nom = []
	r_II_III = r_I_III/r_I_II
	e_II_III = cm.sqrt(1 - pow(r_II_III ,2))		
	II_III_angles = [0., Pi/4, Pi/2, 3*Pi/4]
	ang_index = 0
	for stp in range(n_tot_steps):
		#   setting the angle of the ellipse in the II-III plane :
		if	(stp % 4 == 0) :
			ang_index = 0
		eq_angle = II_III_angles[ang_index]
		ang_index += 1			
		F1_data = []
		F2_data = []
		F3_data = []
		time_inc = float(time_steps[stp])/float(n_increment)
		a_I     = KI_Yield[stp] # big radius of the ellipse:
		a_II  = a_I/r_I_II     # small radius of the ellipse in the plane I-II
		a_III = a_I/r_I_III    # small radius of the ellipse in the plane I-III
		coef = np.real( e_II_III*np.cos(eq_angle)*e_II_III*np.cos(eq_angle) ).tolist()
		a_eq = a_II/np.sqrt(1-coef)
		r_I_eq = a_I/a_eq
		e    = cm.sqrt(1 - pow(r_I_eq ,2))
		for i in range(n_increment):
			incr_angle = 2*Pi*(i+1)/n_increment - Pi/2				
			coef = np.real( e*np.cos(incr_angle)*e*np.cos(incr_angle) ).tolist()
			r0 = a_I/np.sqrt(1-coef)
			KI_pos   = KI_Center[stp]  + r0*np.sin(incr_angle)
			Keq_pos  = r0*np.cos(incr_angle)
			KII_pos  = KII_Center[stp]  + Keq_pos*np.cos(eq_angle)
			KIII_pos = KIII_Center[stp] + Keq_pos*np.sin(eq_angle)
			KI_nom   += [round(KI_pos,4)]
			KII_nom  += [round(KII_pos,4)]
			KIII_nom += [round(KIII_pos,4)]
			F1, F2, F3 = SIF_To_Force(KI_pos, KII_pos, KIII_pos, Param )
			F1_data += [[time_inc*(i+1), round(F1,1)]]
			F2_data += [[time_inc*(i+1), round(F2,1)]]
			F3_data += [[time_inc*(i+1), round(F3,1)]]
		step = 'Step-%d' %(stp+1)
		if stp != 0:
			prev_step = 'Step-%d' % stp
			mdb.models['Model-1'].StaticStep(name=step , previous=prev_step)
		Amp_name_F1 = 'Amp_F1_%d' %(stp+1)
		Amp_name_F2 = 'Amp_F2_%d' %(stp+1)
		Amp_name_F3 = 'Amp_F3_%d' %(stp+1)
		mdb.models['Model-1'].TabularAmplitude(name=Amp_name_F1, timeSpan=STEP, smooth=SOLVER_DEFAULT, data=F1_data)
		mdb.models['Model-1'].TabularAmplitude(name=Amp_name_F2, timeSpan=STEP, smooth=SOLVER_DEFAULT, data=F2_data)
		mdb.models['Model-1'].TabularAmplitude(name=Amp_name_F3, timeSpan=STEP, smooth=SOLVER_DEFAULT, data=F3_data)
		mdb.models['Model-1'].steps[step].resume()
		mdb.models['Model-1'].loads['SUP_RIGHT'].setValuesInStep(    stepName=step , cf1=  1. , cf2=  1. , cf3= 0. , amplitude=Amp_name_F1 )
		mdb.models['Model-1'].loads['SUP_RIGHT_III'].setValuesInStep(stepName=step , cf1=  0. , cf2=  0. , cf3=-1. , amplitude=Amp_name_F3 )
		mdb.models['Model-1'].loads['INF_LEFT'].setValuesInStep(    stepName=step , cf1= -1. , cf2= -1. , cf3= 0. , amplitude=Amp_name_F1 )
		mdb.models['Model-1'].loads['INF_LEFT_III'].setValuesInStep(stepName=step , cf1=  0. , cf2=  0. , cf3= 1. , amplitude=Amp_name_F3 )
		mdb.models['Model-1'].loads['SUP_LEFT'].setValuesInStep(     stepName=step , cf1=-1. , cf2= 1. , cf3= 0. , amplitude=Amp_name_F2 )
		mdb.models['Model-1'].loads['SUP_LEFT_III'].setValuesInStep( stepName=step , cf1= 0. , cf2= 0. , cf3=-1. , amplitude=Amp_name_F3 )
		mdb.models['Model-1'].loads['INF_RIGHT'].setValuesInStep(     stepName=step , cf1= 1. , cf2=-1. , cf3= 0. , amplitude=Amp_name_F2 )
		mdb.models['Model-1'].loads['INF_RIGHT_III'].setValuesInStep( stepName=step , cf1= 0. , cf2= 0. , cf3= 1. , amplitude=Amp_name_F3 )
		if NLGEOM :
			mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = ON)
		else :
			mdb.models['Model-1'].steps[step].setValues(timePeriod=time_steps[stp], maxNumInc = max_Num_Inc, initialInc=ini_inc, minInc=min_inc, maxInc=max_inc, nlgeom = OFF)
	#: Crach history output for SIF determination

if name == 'EL_Norm':
	mdb.models['Model-1'].historyOutputRequests['CRACK-RIGHT-SIF'].resume()
else :
	mdb.models['Model-1'].historyOutputRequests['CRACK-RIGHT-SIF'].suppress()

mdb.models['Model-1'].historyOutputRequests['LINE-DISP-RIGHT'].suppress()
mdb.models['Model-1'].historyOutputRequests['FIELD-DISP-RIGHT'].suppress()
mdb.models['Model-1'].historyOutputRequests['FACES-DISP-RIGHT'].suppress()
mdb.models['Model-1'].historyOutputRequests['LIPS-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
mdb.models['Model-1'].historyOutputRequests['POINTE-DISP-RIGHT'].setValues(timeInterval=ini_inc) 
mdb.models['Model-1'].historyOutputRequests['SECTION-DISP-RIGHT'].setValues(timeInterval=ini_inc) 

# Prepare a restart computation:
new_step = 'Step-%d' % (n_tot_steps+1)
last_stp = 'Step-%d' % n_tot_steps

mdb.models['Model-1'].StaticStep(name=new_step, previous=last_stp, description='Loading step')
mdb.Model(name='Model-1-Restart', objectToCopy=mdb.models['Model-1'])

mdb.models['Model-1'].steps[last_stp].Restart(frequency=4, numberIntervals=0, overlay=ON, timeMarks=OFF)
mdb.models['Model-1-Restart'].steps[new_step].Restart(frequency=4, numberIntervals=0, overlay=ON, timeMarks=OFF)

mdb.models['Model-1'].steps[new_step].suppress()
mdb.models['Model-1-Restart'].steps[new_step].suppress()

#mdb.save()
#: Create the Job
print 'Create the Job'
mdb.Job(name=jobName, model='Model-1', description=jobDescrip, type=ANALYSIS, 
	atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
	memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
	explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
	modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
	scratch='', multiprocessingMode=DEFAULT, numCpus=16, numDomains=16)
#: Cree le fichier .inp
mdb.jobs[jobName].writeInput()
print '#: Launch calculation'
#: Lance le calcul et attends qu'il soit fini
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()
print '#: Simulation finished'
moveFiles(jobName, odbSrc)
#if name == 'EP':
#	odb=openOdb(path=os.path.join(odbSrc,jobName) + '.odb')
#	Field_Capture(odb, odbSrc, jobName, 'PEEQ', 10, n_steps)    			# Capture and save the crack tip at each step end with a magnification factor = 10
#	odb.close()
print 'Computation successfully finished '
#return jobName, KI_nom, KII_nom

mdb.close()


#: Saving Job parameters:

Ellipse_JobName = jobName

Job.Ellipse.JobName 		= Ellipse_JobName
Job.Ellipse.II_III_angles	= II_III_angles
Job.Ellipse.KI_Center 		= KI_Center
Job.Ellipse.KII_Center 		= KII_Center
Job.Ellipse.KIII_Center 	= KIII_Center
Job.Ellipse.KI_Yield 		= KI_Yield

Job.Ellipse.Ellip_ratio_I_II  = Ellip_ratio_I_II
Job.Ellipse.Ellip_ratio_I_III = Ellip_ratio_I_III

Job.Ellipse.KI_nom 			= KI_nom
Job.Ellipse.KII_nom 		= KII_nom
Job.Ellipse.KIII_nom 		= KIII_nom



file2=open(os.path.join( odbSrc,'plot_K_nom_Ellipsoid_%s' % ( suffix )),'w') 
for t in range(len(KI_nom)):
	file2.write('%30.30E   ' % KI_nom[t])
	file2.write('%30.30E   ' % KII_nom[t])
	file2.write('%30.30E   ' % KIII_nom[t])
	file2.write(' \n' )

file2.close()

file2=open(os.path.join( odbSrc,'Job_Parameters_Ellipsoid_%s.p' % ( suffix )),'wb')
pickle.dump(Job, file2)
file2.close()


