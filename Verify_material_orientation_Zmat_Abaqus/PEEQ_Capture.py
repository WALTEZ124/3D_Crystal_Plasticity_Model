# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.11-2 replay file
# Internal Version: 2011_07_12-15.51.58 111859
# Run by tezeghdanti on Fri Nov 17 18:40:49 2017
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
import pickle




session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=290.105072021484, 
    height=112.095001220703)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup



R0        = 250.
C1        = 75000.
Gamma1    = 250.
loading_type   = 'Imposed_Force'

def_scale= 10
min_PEEQ = 1E-4

class Container(object):
    def __init__(self):
        pass



hkl = [1,1,0]
uvw = [1,-1,1]

Shkl = "%d%d%d" % (hkl[0], hkl[1], hkl[2])
Suvw = "%d%d%d" % (uvw[0], uvw[1], uvw[2])
if Shkl == '000' :
	suffix = 'isotropic'
else :
	suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)	


executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(referenceRepresentation=ON)

JobName = 'EL_Norm_%s_KI_1_KII_0_KIII_0' % suffix
o1 = session.openOdb(name=JobName+'.odb')

session.viewports['Viewport: 1'].setValues(displayedObject=o1)
leaf = dgo.LeafFromElementSets(elementSets=('FIELD-RIGHT', ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(renderStyle=WIREFRAME, deformationScaling=UNIFORM, uniformScaleFactor=10 )
session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='PEEQ', outputPosition=INTEGRATION_POINT, )
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues( maxAutoCompute=ON, minAutoCompute=ON , animationAutoLimits=ALL_FRAMES)
session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=100 )
session.viewports['Viewport: 1'].odbDisplay.contourOptions.setValues(
    			contourType=LINE, numIntervals=16, intervalLineAttributes=((SOLID, THICK), 
    			(SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (
    			SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (
    			SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, THICK), (SOLID, 
    			THICK)), maxAutoCompute=ON, minAutoCompute=OFF, minValue=min_PEEQ , animationAutoLimits=CURRENT_FRAME, intervalType=LOG)
session.viewports['Viewport: 1'].view.setValues(nearPlane=1.19977, 
    			farPlane=1.60871, cameraUpVector=(0.0323859, 0.998171, -0.0510526), cameraPosition=(9.82801, 0.00167994, 1.4499), cameraTarget=(10.1043, 
			-0.0813455, 0.0457892))

session.viewports['Viewport: 1'].view.setValues(nearPlane=1.17471, 
			farPlane=1.63298, width=1.32158, height=0.709307, viewOffsetX=0.00419085, 
		  	viewOffsetY=-0.00245054)
session.viewports['Viewport: 1'].view.setProjection(projection=PARALLEL)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legendFont='-*-bitstream vera sans-medium-r-normal-*-*-140-*-*-p-*-*-*')
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(legendMinMax=ON)
#session.animationController.animationOptions.setValues(mode=PLAY_ONCE, timeHistoryMode=TIME_BASED, timeIncrement=0.1, minTimeAutoCompute=False, 
#			minTime=0.1, maxTimeAutoCompute=False, maxTime=1, relativeScaling=FULL_CYCLE)
#session.animationController.play(duration=UNLIMITED)
#session.animationController.setValues(animationType=TIME_HISTORY, viewports=('Viewport: 1', ))
#session.imageAnimationOptions.setValues(vpDecorations=ON, vpBackground=OFF, compass=OFF, timeScale=1, frameRate=40)
session.writeImage(fileName=JobName, format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
#session.animationController.setValues(animationType=NONE)

o1.close()





