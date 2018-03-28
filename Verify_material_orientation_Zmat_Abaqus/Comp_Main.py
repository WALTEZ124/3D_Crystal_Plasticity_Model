# -*- coding: utf-8 -*-


srcFile =os.path.join(compSrc,'Model_Circular_Partition.py')
execfile(srcFile)
#openmdb = openMdb(pathName='3D_Model.cae')

# Pour l'affichage des masques dans le fichier rpy
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

#----------------------------------------------------------------------------------
# Job parameters :
#----------------------------------------------------------------------------------

n_tot_steps = 3

EL_Job      = { 'n_tot_steps' : n_tot_steps, 'n_act_steps' : 1 , 'time_steps' : [  1 ] ,
				'max_num_inc': 100, 'ini_inc' : 1.0 , 'min_inc' : 1e-3, 'max_inc' : 1 }


#----------------------------------------------------------------------------------
#          Determination of parameters relating loading to nominals SIF 
#----------------------------------------------------------------------------------


elastic = Elastic( eType = elasticity_type)
plastic = Plastic( pType = 'none')


mdb = Material_Config(mdb, 'Model-1', elastic, plastic)


file2=open(os.path.join(compSrc, 'Parameters_F_To_K_nominals_%s.p' %  suffix ),'rb')
Param = pickle.load(file2)
file2.close()


elastic = Elastic( eType = elasticity_type)
plastic = Plastic( pType = 'none')


# Mode I

ELTest_I 	= { 'name' : 'EL_Norm', 'loading_type' : loading_type, 'KI_range' : [1.], 
				'KII_range' : [0.], 'KIII_range' : [0.], 'NLGEOM': False }
EL_Norm_JobName_I = compute(mdb, ELTest_I, EL_Job, Param, elastic, odbSrcEL)

file2=open('last_job_file','w') 
file2.write(EL_Norm_JobName_I) 
file2.close()


