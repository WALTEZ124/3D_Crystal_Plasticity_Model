# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------------
#          Test configuration
#---------------------------------------------------------------------------------

loading_type   = 'Imposed_Force'
#loading_type  = 'Imposed_Displacement'

# Geometry:

class Container(object):
    def __init__(self):
        pass

dimensions = Container()

dimensions.rad_len  = 37	# rad_len-1 should be a multiple of 2
dimensions.thet_len = 81	# thet_len-1 should be a multiple of 4
dimensions.z_len    = 9		# z_len-1 should be a multiple of 2
dimensions.time_inc = 0.1
#---------------------------> rad_len * (thet_len+1) * z_len * 6(dof)  < 10*max_history_output = 100,000

############################
#          Material
############################

#elasticity_type = 'isotropic'
elasticity_type = 'orthotropic'

#hardening_type_list = ['linear-isotropic-hardening','linear-kinematic-hardening','nonlinear-kinematic-hardening','nonlinear-combined-hardening']

#hardening_type = 'nonlinear-kinematic-hardening'
hardening_type = 'nonlinear-combined-hardening'

if elasticity_type == 'orthotropic' :
	#-------------------------------------
	# Miller indices: Input variables
	hkl = np.asarray([ 0, 1, 0])
	uvw = np.asarray([ 1, 0, 0])
	#-------------------------------------
	qrs = np.cross(hkl, uvw)
	Nhkl = np.linalg.norm(hkl)
	Nuvw = np.linalg.norm(uvw)
	Nqrs = np.linalg.norm(qrs)
	g_prime_transpose = np.array([[ uvw[0]/Nuvw,  uvw[1]/Nuvw, uvw[2]/Nuvw ],
								  [ hkl[0]/Nhkl,  hkl[1]/Nhkl, hkl[2]/Nhkl ],
								  [-qrs[0]/Nqrs, -qrs[1]/Nqrs, -qrs[2]/Nqrs] ])  					# Transfomation matrix from crack coordinates to crystal coordinates
	NormalAxis  = np.dot( g_prime_transpose, np.array([1,0,0]) )								# First crystal axis 
	PrimaryAxis = np.dot( g_prime_transpose, np.array([0,1,0]) )
	AdditionalRotationAngle = 0.


# Parameters used by Walid
'''
EYoung = 210000.0
nuPoisson = 0.3
EYoung_Rigid = 100 * EYoung 

C11 = 197000.0
C12 = 144000.0
C44 = 90000.0

R0 = 770.0
# Kinematic Hardening
C1 = 7500.0
Gamma1 = 250.0

# Isotropic Hardening
Qinf = 0.0
b    = 0.0

'''
# Parameters used by Flavien Frémy
EYoung       = 200000.
EYoung_Rigid = 100 * EYoung 
nuPoisson = 0.3


C11 = 197000.0
C12 = 144000.0
C44 = 90000.0


R0        = 250.
C1        = 75000.
Gamma1    = 250.
Qinf 	  = 5.
b 	  = 25.

'''
# Parameters used by François Brugier

EYoung       = 206000.
EYoung_Rigid = 100 * EYoung 
nuPoisson = 0.3
R0        = 1411.
C1        = 4080.
Gamma1    = 8.
Qinf 	  = 1.
b 	  = 1.



# Parameters used by Pierre-Yves Decreuses

EYoung       = 182000.
EYoung_Rigid = 100 * EYoung 
nuPoisson = 0.3
R0        = 230.
C1        = 76000.
Gamma1    = 390.
Qinf 	  = -50.
b 	  = 300.

'''
#
#      classes used to save parameters
#

class Elastic():
	def __init__(self, eType = 'orthotropic'):
		self.eType = eType
		self.ElasticRigidValue = (EYoung_Rigid,nuPoisson)
		if self.eType == 'orthotropic':
			self.ElasticValue = (C11,C12,C11,C12,C12,C11,C44,C44,C44)
			self.hkl = hkl.tolist()
			self.uvw = uvw.tolist()
			self.NormalAxis  = NormalAxis.tolist()
			self.PrimaryAxis = PrimaryAxis.tolist()
			self.AdditionalRotationAngle = AdditionalRotationAngle
		elif self.eType == 'isotropic':
			self.ElasticValue = (EYoung, nuPoisson)
		else:
			print('Error in Elasticity Type')

class Plastic():
	def __init__(self, pType = 'nonlinear-combined-hardening'):
		self.pType = pType
		if self.pType == 'nonlinear-combined-hardening':
			self.NonLinKinHardValue = (R0, C1, Gamma1)
			self.NonLinIsoHardValue = (R0, Qinf,  b  )
		elif self.pType == 'nonlinear-kinematic-hardening':
			self.NonLinKinHardValue = (R0, C1, Gamma1)
		elif self.pType == 'linear-isotropic-hardening':
			self.LinIsoHardValue = ((R0, 0.0), (R0+20, 0.2))
		elif self.pType == 'linear-kinematic-hardening':
			self.LinKinHardValue = ((R0, 0.0), (R0+20, 0.2))
		elif self.pType != 'none' :
			print ('Error in Plasticity Type')


