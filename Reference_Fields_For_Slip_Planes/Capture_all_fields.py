# -*- coding: mbcs -*-
#
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=258.635131835938, 
    height=68.2087478637695)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)

import pickle
import os
from os.path import *


class Container(object):
    def __init__(self):
        pass

hkl = [0,1,0]
uvw = [1,0,0]

Shkl = "%d%d%d" % (hkl[0], hkl[1], hkl[2])
Suvw = "%d%d%d" % (uvw[0], uvw[1], uvw[2])
if Shkl == '000' :
	suffix = 'isotropic'
else :
	suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)	


odbSrc = os.path.join('Results_Odb' ,'Imposed_Force', 'src_Odb_%s_octahedral' % (suffix ),'Loading_Range')

captureSrc = os.path.join(odbSrc, 'Capture')
if not os.path.exists(captureSrc):
    os.makedirs(captureSrc)

# Load Job parameters:
file2=open(os.path.join( odbSrc,'Job_Parameters_%s.p' %  suffix ),'rb')
Job = pickle.load(file2)
file2.close()


session.Viewport(name='Viewport: 2', origin=(6.34687471389771, 
    -208.856246948242), width=545.831237792969, height=270.720001220703)

session.Viewport(name='Viewport: 3', origin=(6.34687471389771, 
    -208.856246948242), width=545.831237792969, height=270.720001220703)


slip_systems_list = ['b4','b2','b5','d4','d1','d6','a2','a6','a3','c5','c3','c1']

#slip_systems_list = ['b4']

for slip_suffix in slip_systems_list :
	src_folder = os.path.join(odbSrc, slip_suffix )
	JobName_I   = '%s_%s' % (Job.I.PL.MonName , slip_suffix)
	JobName_II  = '%s_%s' % (Job.II.PL.MonName , slip_suffix)
	JobName_III = '%s_%s' % (Job.III.PL.MonName , slip_suffix)
	o1 = session.openOdb( name= os.path.join(src_folder, JobName_I + '.odb' ) )
	session.viewports['Viewport: 1'].setValues(displayedObject=o1)
	session.viewports['Viewport: 1'].makeCurrent()
	leaf = dgo.LeafFromElementSets(elementSets=('FIELD-RIGHT', ))
	session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
	o2 = session.openOdb( name= os.path.join(src_folder, JobName_II + '.odb' ) )
	session.viewports['Viewport: 2'].setValues(displayedObject=o2)
	session.viewports['Viewport: 2'].makeCurrent()
	leaf = dgo.LeafFromElementSets(elementSets=('FIELD-RIGHT', ))
	session.viewports['Viewport: 2'].odbDisplay.displayGroup.replace(leaf=leaf)
	o3 = session.openOdb( name= os.path.join(src_folder, JobName_III + '.odb' ) )
	session.viewports['Viewport: 3'].setValues(displayedObject=o3)
	session.viewports['Viewport: 3'].makeCurrent()
	leaf = dgo.LeafFromElementSets(elementSets=('FIELD-RIGHT', ))
	session.viewports['Viewport: 3'].odbDisplay.displayGroup.replace(leaf=leaf)
	session.viewports['Viewport: 1'].makeCurrent()	
	session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
	session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, uniformScaleFactor=10)
	session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legendFont='-*-bitstream vera sans-medium-r-normal-*-*-120-*-*-p-*-*-*')
	session.viewports['Viewport: 2'].makeCurrent()
	session.viewports['Viewport: 1'].restore()
	session.viewports['Viewport: 2'].makeCurrent()
	session.viewports['Viewport: 2'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
	session.viewports['Viewport: 2'].viewportAnnotationOptions.setValues(legendFont='-*-bitstream vera sans-medium-r-normal-*-*-120-*-*-p-*-*-*')
	session.viewports['Viewport: 3'].makeCurrent()
	session.viewports['Viewport: 3'].viewportAnnotationOptions.setValues(legendFont='-*-bitstream vera sans-medium-r-normal-*-*-120-*-*-p-*-*-*')
	session.viewports['Viewport: 3'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
	session.viewports['Viewport: 1'].view.setValues(nearPlane=1.19977, farPlane=1.60871, cameraUpVector=(0.0323859, 0.998171, -0.0510526), cameraPosition=(9.82801, 0.00167994, 1.4499), cameraTarget=(10.1043, -0.0813455, 0.0457892))
	#session.viewports['Viewport: 1'].view.setValues(nearPlane=1.17471, farPlane=1.63298, width=1.32158, height=0.709307, viewOffsetX=0.00419085, viewOffsetY=-0.00245054)
	session.viewports['Viewport: 1'].view.setValues(nearPlane=1.13797, farPlane=1.66443, width=0.668295, height=0.888177, viewOffsetX=-0.0483358, viewOffsetY=0.0556042)
	session.viewports['Viewport: 2'].view.setValues(nearPlane=1.19977, farPlane=1.60871, cameraUpVector=(0.0323859, 0.998171, -0.0510526), cameraPosition=(9.82801, 0.00167994, 1.4499), cameraTarget=(10.1043, -0.0813455, 0.0457892))
	session.viewports['Viewport: 2'].view.setValues(nearPlane=1.17471, farPlane=1.63298, width=1.32158, height=0.709307, viewOffsetX=0.00419085, viewOffsetY=-0.00245054)
	session.viewports['Viewport: 2'].view.setValues(nearPlane=1.13797, farPlane=1.66443, width=0.668295, height=0.888177, viewOffsetX=-0.0483358, viewOffsetY=0.0556042)
	session.viewports['Viewport: 3'].view.setValues(nearPlane=1.19977, farPlane=1.60871, cameraUpVector=(0.0323859, 0.998171, -0.0510526), cameraPosition=(9.82801, 0.00167994, 1.4499), cameraTarget=(10.1043, -0.0813455, 0.0457892))
	session.viewports['Viewport: 3'].view.setValues(nearPlane=1.17471, farPlane=1.63298, width=1.32158, height=0.709307, viewOffsetX=0.00419085, viewOffsetY=-0.00245054)
	session.viewports['Viewport: 3'].view.setValues(nearPlane=1.13797, farPlane=1.66443, width=0.668295, height=0.888177, viewOffsetX=-0.0483358, viewOffsetY=0.0556042)
	session.viewports['Viewport: 1'].setValues(origin=(0.0, -208.856262207031),width=204.951156616211, height=277.065002441406)
	session.viewports['Viewport: 2'].setValues(origin=(204.951156616211,-208.856262207031), width=204.951156616211, height=277.065002441406)
	session.viewports['Viewport: 3'].setValues(origin=(409.902313232422, -208.856262207031), width=204.951156616211, height=277.065002441406)
	### Von Mises
	session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Mises'), )
	session.viewports['Viewport: 2'].odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Mises'), )
	session.viewports['Viewport: 3'].odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Mises'), )	
	session.printToFile(fileName=os.path.join(captureSrc, "Mises_%s" % (JobName_I) ), format=PNG, canvasObjects=(session.viewports['Viewport: 3'], session.viewports['Viewport: 2'], session.viewports['Viewport: 1']))
	### Max strain
	session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Max. Principal'), )
	session.viewports['Viewport: 2'].odbDisplay.setPrimaryVariable(variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Max. Principal'), )
	session.viewports['Viewport: 3'].odbDisplay.setPrimaryVariable(variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Max. Principal'), )
	session.printToFile(fileName=os.path.join(captureSrc, "E_Max_Prple_%s" % (JobName_I) ), format=PNG, canvasObjects=(session.viewports['Viewport: 3'], session.viewports['Viewport: 2'], session.viewports['Viewport: 1']))
	### Cumulated plastic sliding	
	session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='SDV14', outputPosition=INTEGRATION_POINT, )
	session.viewports['Viewport: 2'].odbDisplay.setPrimaryVariable(variableLabel='SDV14', outputPosition=INTEGRATION_POINT, )
	session.viewports['Viewport: 3'].odbDisplay.setPrimaryVariable(variableLabel='SDV14', outputPosition=INTEGRATION_POINT, )
	session.printToFile(fileName=os.path.join(captureSrc, "EV1_Cum_%s" % (JobName_I) ), format=PNG, canvasObjects=(session.viewports['Viewport: 3'], session.viewports['Viewport: 2'], session.viewports['Viewport: 1']))
	### Cumulated plastic sliding LOG	
	session.viewports['Viewport: 1'].makeCurrent()
	session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(contourType=LINE, numIntervals=13, intervalLineAttributes=((SOLID, THICK), 
    			(SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (
    			SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), 
			(SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK)), maxAutoCompute=ON, minAutoCompute=OFF, minValue=0.0001, intervalType=LOG)
	session.viewports['Viewport: 2'].makeCurrent()
	session.viewports['Viewport: 2'].odbDisplay.contourOptions.setValues(contourType=LINE, numIntervals=13, intervalLineAttributes=((SOLID, THICK), 
    			(SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (
    			SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), 
			(SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK)), maxAutoCompute=ON, minAutoCompute=OFF, minValue=0.0001, intervalType=LOG)
	session.viewports['Viewport: 3'].makeCurrent()
	session.viewports['Viewport: 3'].odbDisplay.contourOptions.setValues(contourType=LINE, numIntervals=13, intervalLineAttributes=((SOLID, THICK), 
    			(SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (
    			SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), 
			(SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK)), maxAutoCompute=ON, minAutoCompute=OFF, minValue=0.0001, intervalType=LOG)
	session.printToFile(fileName=os.path.join(captureSrc, "EV1_Cum_LOG_%s" % (JobName_I) ), format=PNG, canvasObjects=(session.viewports['Viewport: 3'], session.viewports['Viewport: 2'], session.viewports['Viewport: 1']))
	o1.close()
	o2.close()
	o3.close()
	session.viewports['Viewport: 1'].makeCurrent()
	session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(contourType=BANDED, minAutoCompute=ON, intervalType=UNIFORM)
	session.viewports['Viewport: 2'].makeCurrent()
	session.viewports['Viewport: 2'].odbDisplay.contourOptions.setValues(contourType=BANDED, minAutoCompute=ON, intervalType=UNIFORM)
	session.viewports['Viewport: 3'].makeCurrent()
	session.viewports['Viewport: 3'].odbDisplay.contourOptions.setValues(contourType=BANDED, minAutoCompute=ON, intervalType=UNIFORM)


