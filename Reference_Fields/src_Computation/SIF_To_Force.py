def SIF_To_Force(KI, KII, KIII, Param ):
	m = Param.m_mat
	K = np.asarray([KI,KII,KIII]) * np.sqrt(1000)
	F = np.dot(m,K)	
	return F[0], F[1], F[2]
