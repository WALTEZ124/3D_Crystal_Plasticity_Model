# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.14-1 replay file
# Internal Version: 2014_06_04-21.37.49 134264
# Run by tezeghdanti on Tue Apr 24 09:24:33 2018
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=256.255065917969, 
    height=61.3349990844727)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)





class Container(object):
    def __init__(self):
        pass



hkl = [1,1,0]
uvw = [1,-1,0]

Shkl = "%d%d%d" % (hkl[0], hkl[1], hkl[2])
Suvw = "%d%d%d" % (uvw[0], uvw[1], uvw[2])
if Shkl == '000' :
	suffix = 'isotropic'
else :
	suffix = 'hkl_%s_uvw_%s' %(Shkl, Suvw)	

#JobName = 'EP_Mon_%s_KI_12_KII_0_KIII_0' % suffix
#JobName = 'EP_Mon_%s_KI_0_KII_7_KIII_0' % suffix
#JobName = 'EP_Mon_%s_KI_0_KII_0_KIII_7' % suffix
JobName = 'EP_Mon_%s_KI_10_KII_6_KIII_4' % suffix

OdbSrc = '/utmp/cremant/tezeghdanti/3D_Model_Crystal_Plasticity/Computation/Reference_Fields/Results_Odb/Imposed_Force/src_Odb_%s_octahedral/Loading_Range/LGEOM' % suffix

o1 = session.openOdb(
    name='%s/%s.odb' % (OdbSrc, JobName) )

session.viewports['Viewport: 1'].setValues(displayedObject=o1)
#: Model: /utmp/cremant/tezeghdanti/3D_Model_Crystal_Plasticity/Computation/Reference_Fields/Results_Odb/Imposed_Force/src_Odb_hkl_010_uvw_100_octahedral/Loading_Range/LGEOM/EP_Mon_hkl_010_uvw_100_KI_12_KII_0_KIII_0.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     6
#: Number of Meshes:             6
#: Number of Element Sets:       21
#: Number of Node Sets:          28
#: Number of Steps:              1

session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
leaf = dgo.LeafFromElementSets(elementSets=('FIELD-RIGHT', ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(
    deformationScaling=UNIFORM, uniformScaleFactor=10)
session.viewports['Viewport: 1'].view.setValues(cameraPosition=(10.0615, 
    0.0871453, 6.8511), cameraUpVector=(0, 1, 0))
session.viewports['Viewport: 1'].view.fitView()

session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Mises'), )

session.printToFile(fileName='%s/Mises_%s' %(OdbSrc, JobName) , format=PNG, canvasObjects=(
    session.viewports['Viewport: 1'], ))

session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
    variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 
    'Max. Principal'), )

session.printToFile(fileName='%s/E_Max_Prple_%s' %(OdbSrc, JobName), format=PNG, canvasObjects=(
    session.viewports['Viewport: 1'], ))


o1.close()


