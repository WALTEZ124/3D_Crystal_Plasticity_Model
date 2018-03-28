def Generate_names(test, elastic, odbSrc):
# Test parameters:
	name     = test.get('name')				 #: EL_Rand, EL_Norm, EP
	loading_type  = test.get('loading_type')         #: Loading type: imposed Force or Displacement
	eType = elastic.eType
	if eType== 'isotropic' :
		EYoung    = elastic.ElasticValue[0]
		nuPoisson = elastic.ElasticValue[1]
		if  name== 'EL_Rand' :
			F1 =  test.get('F1')
			F2 =  test.get('F2')
			F3 =  test.get('F3')
			test_nbr = test.get('test_nbr')
			jobDescrip ='%s Analysis isotropic case, EYoung = %d, nuPoisson = %d, F1 = %d, F2 = %d, F3 = %d,  %s ' % ( name, EYoung, nuPoisson, F1, F2, F3, loading_type )
			jobName   = '%s_isotropic_test_%d' %(name, test_nbr )
		elif name== 'EL_Norm' :
			KI_range	  = test.get('KI_range')	         #: Range of KI nom
			KII_range	  = test.get('KII_range')	         #: Range of KII nom	
			KIII_range	  = test.get('KIII_range')	         #: Range of KIII nom	
			jobDescrip ='%s Analysis isotropic case, EYoung = %d, nuPoisson = %d, KI = %d, KII = %d, KIII = %d,  %s ' % ( name, EYoung, nuPoisson, KI_range[-1], KII_range[-1], KIII_range[-1], loading_type )
			jobName    = '%s_isotropic_KI_%d_KII_%d_KIII_%d' %(name,KI_range[-1], KII_range[-1], KIII_range[-1] )
		elif name == 'EP':
			test_type     = test.get('test_type')            #: Mon or Cyc or Star
			KI_range	  = test.get('KI_range')	         #: Range of KI nom
			KII_range	  = test.get('KII_range')	         #: Range of KII nom
			KIII_range	  = test.get('KIII_range')	         #: Range of KIII nom	
			stI_range = ''
			stII_range= ''
			stIII_range= ''
			for i in range(len(KI_range)):
				stI_range   += '_%d' %KI_range[i]
				stII_range  += '_%d' %KII_range[i]
				stIII_range += '_%d' %KIII_range[i]
			jobDescrip='%s plastic, isotropic, KI: %s , KII: %s , KIII: %s ,loading type: %s' % ( test_type, stI_range, stII_range, stIII_range, loading_type)
			if test_type == 'Cyc' :
				stI_range   = '_%d' % max(KI_range)
				stII_range  = '_%d' % max(KII_range)
				stIII_range = '_%d' % max(KIII_range)
				#PathShape = test.get('PathShape')
			if test_type == 'Star' :
				KCenter    = test.get('KCenter')
				init_prop_angle = test.get('init_prop_angle')
				jobName = '%s_%s_isotropic_Prop_%d_KCenter_%d' %(name, test_type,  init_prop_angle, KCenter )		
			else :
				jobName = '%s_%s_isotropic_KI%s_KII%s_KIII%s' %(name, test_type, stI_range, stII_range, stIII_range)
	elif eType == 'orthotropic'	:
		Shkl = "%d%d%d" % (elastic.hkl[0],elastic.hkl[1],elastic.hkl[2])
		Suvw = "%d%d%d" % (elastic.uvw[0],elastic.uvw[1],elastic.uvw[2])
		suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)
		if  name== 'EL_Rand' :
			F1 =  test.get('F1')
			F2 =  test.get('F2')
			F3 =  test.get('F3')
			test_nbr = test.get('test_nbr')
			jobDescrip ='%s Analysis cubic case, %s, F1 = %d, F2 = %d, F3 = %d,  %s ' % ( name, suffix, F1, F2, F3, loading_type )
			jobName   = '%s_%s_test_%d' %(name, suffix, test_nbr )
		elif name== 'EL_Norm' :
			KI_range	  = test.get('KI_range')	         #: Range of KI nom
			KII_range	  = test.get('KII_range')	         #: Range of KII nom	
			KIII_range	  = test.get('KIII_range')	         #: Range of KIII nom	
			jobDescrip ='%s Analysis cubic case, %s , KI = %d, KII = %d, KIII = %d,  %s ' % ( name, suffix,KI_range[-1], KII_range[-1], KIII_range[-1], loading_type )
			jobName   = '%s_%s_KI_%d_KII_%d_KIII_%d' %(name, suffix, KI_range[-1], KII_range[-1], KIII_range[-1] )
		elif name == 'EP':
			test_type     = test.get('test_type')            #: Mon or Cyc or Star
			KI_range	  = test.get('KI_range')	         #: Range of KI nom
			KII_range	  = test.get('KII_range')	         #: Range of KII nom
			KIII_range	  = test.get('KIII_range')	         #: Range of KIII nom	
			stI_range = ''
			stII_range= ''
			stIII_range= ''
			for i in range(len(KI_range)):
				stI_range   += '_%d' %KI_range[i]
				stII_range  += '_%d' %KII_range[i]
				stIII_range += '_%d' %KIII_range[i]
			jobDescrip='%s plastic, cubic, %s, KI: %s , KII: %s , KIII: %s,loading type: %s' % ( test_type, suffix, stI_range, stII_range, stIII_range, loading_type)
			if test_type == 'Cyc' :
				stI_range   = '_%d' % max(KI_range)
				stII_range  = '_%d' % max(KII_range)
				stIII_range = '_%d' % max(KIII_range)
				#PathShape = test.get('PathShape')
			if test_type == 'Star' :
				KCenter    = test.get('KCenter')
				init_prop_angle = test.get('init_prop_angle')
				jobName = '%s_%s_%s_Prop_%d_KCenter_%d' %(name, test_type, suffix, init_prop_angle, KCenter )		
			else :
				jobName = '%s_%s_%s_KI%s_KII%s_KIII%s' %(name, test_type, suffix, stI_range, stII_range, stIII_range)	
	return jobName, jobDescrip
