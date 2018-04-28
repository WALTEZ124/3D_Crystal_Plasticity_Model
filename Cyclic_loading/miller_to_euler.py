import numpy as np ;
hkl = [ ${hkl_list[0]}, ${hkl_list[1]}, ${hkl_list[2]}]; 
uvw = [ ${uvw_list[0]}, ${uvw_list[1]}, ${uvw_list[2]}];

def miller_to_euler(hkl, uvw):	
	hkl = np.asarray(hkl); 
	uvw = np.asarray(uvw);
	qrs = np.cross(hkl, uvw) ;
	Nhkl = np.linalg.norm(hkl) ;
	Nuvw = np.linalg.norm(uvw) ;
	Nqrs = np.linalg.norm(qrs) ;
	g = np.array([[ uvw[0]/Nuvw,  qrs[0]/Nqrs, hkl[0]/Nhkl ],
	                [ uvw[1]/Nuvw, qrs[1]/Nqrs, hkl[1]/Nhkl ],
	                [ uvw[2]/Nuvw, qrs[2]/Nqrs, hkl[2]/Nhkl] ])     ;  
	print(g)     
	if abs(g[2][2]-1)<1e-6 :
	        phi1 = np.arctan(g[0][1]/g[0][0])*180/np.pi ;
	        psi  = 0.;
	        phi2 = 0.;
	else :
	        phi1 = np.arctan(-g[2][0]/g[2][1])*180/np.pi;
	        psi  = np.arccos(g[2][2])*180/np.pi;
	        phi2 = np.arctan(g[0][2]/g[1][2])*180/np.pi;
	print(g)
	print('%f %f %f' % (phi1, psi, phi2));

def miller_to_euler_1(hkl, uvw):	
	h,k,l = hkl;
	u, v, w = uvw;
	Nhkl = np.linalg.norm(hkl) ;
	Nuvw = np.linalg.norm(uvw) ;
	psi = np.arccos(l/Nhkl)*180/np.pi;
	phi2 = np.arccos(k/np.sqrt(h**2+k**2))*180/np.pi;
	phi1 = np.arcsin(w*Nhkl/(Nuvw*np.sqrt(h**2+k**2)))*180/np.pi;
	print('%f %f %f' % (phi1, psi, phi2));

def miller_to_matrix(hkl, uvw):
	hkl = np.asarray(hkl); 
	uvw = np.asarray(uvw);
	qrs = np.cross(hkl, uvw) ;
	Nhkl = np.linalg.norm(hkl) ;
	Nuvw = np.linalg.norm(uvw) ;
	Nqrs = np.linalg.norm(qrs) ;
	g = np.array([[ uvw[0]/Nuvw,  qrs[0]/Nqrs, hkl[0]/Nhkl ],
			[ uvw[1]/Nuvw, qrs[1]/Nqrs, hkl[1]/Nhkl ],
			[ uvw[2]/Nuvw, qrs[2]/Nqrs, hkl[2]/Nhkl] ]) 	;
	R = np.array([[1,0,0],[0,0,1],[0,-1,0]]);
	g_prime = np.matmul(g, R )
	X1 = np.dot( g_prime, np.array([1,0,0]) )	;					
	X2 = np.dot( g_prime, np.array([0,1,0]) )	;
	X1_txt = '%f %f %f' % (X1[0],X1[1],X1[2]) ;
	X2_txt = '%f %f %f' % (X2[0],X2[1],X2[2]) ;
	print(g)
	print( 'x1 %s x2 %s' %(X1_txt, X2_txt) ) ;

miller_to_matrix(hkl, uvw)

