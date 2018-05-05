# -*- coding: mbcs -*-

def Fields_Capture(odb,OdbSrc, JobName):
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)
    o1 = session.openOdb(name='%s/%s.odb' % (OdbSrc, JobName) )
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
    leaf = dgo.LeafFromElementSets(elementSets=('FIELD-RIGHT', ))
    session.viewports['Viewport: 1'].odbDisplay.displayGroup.replace(leaf=leaf)
    session.viewports['Viewport: 1'].odbDisplay.commonOptions.setValues(deformationScaling=UNIFORM, uniformScaleFactor=10)
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(10.0615, 0.0871453, 6.8511), cameraUpVector=(0, 1, 0))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Mises'), )
    session.printToFile(fileName='%s/Mises_%s' %(OdbSrc, JobName) , format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(variableLabel='E', outputPosition=INTEGRATION_POINT, refinement=(INVARIANT, 'Max. Principal'), )
    session.printToFile(fileName='%s/E_Max_Prple_%s' %(OdbSrc, JobName), format=PNG, canvasObjects=(session.viewports['Viewport: 1'], ))
