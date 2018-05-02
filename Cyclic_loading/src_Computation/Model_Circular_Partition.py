# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.11-2 replay file
# Internal Version: 2011_07_12-15.51.58 111859
# Run by tezeghdanti on Mon Feb  6 10:30:13 2017
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE) 


###########################################
# Create rigid wires for corners:
###########################################

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=2500.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.ArcByCenterEnds(center=(-900.0, -900.0), point1=(-900.0, -1000.0), point2=(
    -1000.0, -900.0), direction=CLOCKWISE)
s1.Line(point1=(-900.0, -1000.0), point2=(-750.0, -1000.0))
s1.HorizontalConstraint(entity=g[3], addUndoState=False)
s1.ArcByCenterEnds(center=(-750.0, -1100.0), point1=(-750.0, -1000.0), point2=(
    -650.0, -1100.0), direction=CLOCKWISE)
s1.Line(point1=(-1000.0, -900.0), point2=(-1000.0, -750.0))
s1.ArcByCenterEnds(center=(-1100.0, -750.0), point1=(-1100.0, -650.0), point2=(
    -1000.0, -750.0), direction=CLOCKWISE)
s1.VerticalConstraint(entity=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[3])
s1.TangentConstraint(entity1=g[3], entity2=g[4])
s1.TangentConstraint(entity1=g[5], entity2=g[6])
p = mdb.models['Model-1'].Part(name='Arc_INF_LEFT', 
    dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Arc_INF_LEFT']
p.BaseShellExtrude(sketch=s1, depth=0.1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Arc_INF_LEFT']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=2500.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.ArcByCenterEnds(center=(900.0, 900.0), point1=(900.0, 1000.0), point2=(
    1000.0, 900.0), direction=CLOCKWISE)
s1.Line(point1=(900.0, 1000.0), point2=(750.0, 1000.0))
s1.HorizontalConstraint(entity=g[3], addUndoState=False)
s1.ArcByCenterEnds(center=(750.0, 1100.0), point1=(750.0, 1000.0), point2=(
    650.0, 1100.0), direction=CLOCKWISE)
s1.Line(point1=(1000.0, 900.0), point2=(1000.0, 750.0))
s1.ArcByCenterEnds(center=(1100.0, 750.0), point1=(1100.0, 650.0), point2=(
    1000.0, 750.0), direction=CLOCKWISE)
s1.VerticalConstraint(entity=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[3])
s1.TangentConstraint(entity1=g[3], entity2=g[4])
s1.TangentConstraint(entity1=g[5], entity2=g[6])
p = mdb.models['Model-1'].Part(name='Arc_SUP_RIGHT', 
    dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Arc_SUP_RIGHT']
p.BaseShellExtrude(sketch=s1, depth=0.1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Arc_SUP_RIGHT']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']


s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=2500.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.ArcByCenterEnds(center=(-900.0, 900.0), point1=(
    -1000.0, 900.0),point2=(-900.0, 1000.0), direction=CLOCKWISE)
s1.Line(point1=(-900.0, 1000.0), point2=(-750.0, 1000.0))
s1.HorizontalConstraint(entity=g[3], addUndoState=False)
s1.ArcByCenterEnds(center=(-750.0, 1100.0), point1=(
    -650.0, 1100.0), point2=(-750.0, 1000.0), direction=CLOCKWISE)
s1.Line(point1=(-1000.0, 900.0), point2=(-1000.0, 750.0))
s1.ArcByCenterEnds(center=(-1100.0, 750.0), point1=(
    -1000.0, 750.0), point2=(-1100.0, 650.0),  direction=CLOCKWISE)
s1.VerticalConstraint(entity=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[3])
s1.TangentConstraint(entity1=g[3], entity2=g[4])
s1.TangentConstraint(entity1=g[5], entity2=g[6])
p = mdb.models['Model-1'].Part(name='Arc_SUP_LEFT', 
    dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Arc_SUP_LEFT']
p.BaseShellExtrude(sketch=s1, depth=0.1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Arc_SUP_LEFT']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=2500.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.ArcByCenterEnds(center=(900.0, -900.0), point1=(
    1000.0, -900.0),point2=(900.0, -1000.0), direction=CLOCKWISE)
s1.Line(point1=(900.0, -1000.0), point2=(750.0, -1000.0))
s1.HorizontalConstraint(entity=g[3], addUndoState=False)
s1.ArcByCenterEnds(center=(750.0, -1100.0), point1=(
    650.0, -1100.0), point2=(750.0, -1000.0), direction=CLOCKWISE)
s1.Line(point1=(1000.0, -900.0), point2=(1000.0, -750.0))
s1.ArcByCenterEnds(center=(1100.0, -750.0), point1=(
    1000.0, -750.0), point2=(1100.0, -650.0),  direction=CLOCKWISE)
s1.VerticalConstraint(entity=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[5], addUndoState=False)
s1.TangentConstraint(entity1=g[2], entity2=g[3])
s1.TangentConstraint(entity1=g[3], entity2=g[4])
s1.TangentConstraint(entity1=g[5], entity2=g[6])
p = mdb.models['Model-1'].Part(name='Arc_INF_RIGHT', 
    dimensionality=THREE_D, type=DISCRETE_RIGID_SURFACE)
p = mdb.models['Model-1'].parts['Arc_INF_RIGHT']
p.BaseShellExtrude(sketch=s1, depth=0.1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Arc_INF_RIGHT']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

#####################################
# Create the deformable body
#####################################

s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=2500.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(point1=(-1000.0, -1000.0), point2=(1000.0, 1000.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=1863.82, 
    farPlane=2850.23, width=2729.45, height=3514.08, cameraPosition=(-103.834, 
    418.147, 2357.02), cameraTarget=(-103.834, 418.147, 0))
s1.FilletByRadius(radius=100.0, curve1=g[2], nearPoint1=(-997.161987304688, 
    805.044250488281), curve2=g[3], nearPoint2=(-857.488525390625, 
    997.038391113281))
s1.FilletByRadius(radius=100.0, curve1=g[2], nearPoint1=(-1002.98168945312, 
    -791.998229980469), curve2=g[5], nearPoint2=(-784.742065429688, 
    -1010.17352294922))
s1.FilletByRadius(radius=100.0, curve1=g[5], nearPoint1=(806.952758789062, 
    -989.810485839844), curve2=g[4], nearPoint2=(1007.73327636719, 
    -710.546325683594))
s1.FilletByRadius(radius=100.0, curve1=g[4], nearPoint1=(999.003540039062, 
    787.590148925781), curve2=g[3], nearPoint2=(772.034301757812, 
    994.129211425781))
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseSolidExtrude(sketch=s1, depth=0.1)
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']

#######################
# Draw partitions:
#######################

# Corners partition


p = mdb.models['Model-1'].parts['Part-1']
f, e, d1 = p.faces, p.edges, p.datums

pickedFaces = f.findAt(((0.0,0.0,0.0) ,))
pickedEdges = e.findAt(((1000.0, 10.0, 0.0),))
t = p.MakeSketchTransform(sketchPlane=pickedFaces[0], sketchPlaneSide=SIDE1,sketchUpEdge=pickedEdges[0], origin=(0.0, 
    0.0, 0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=5656.85, gridSpacing=141.42, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.ArcByCenterEnds(center=(-1000.0, -1000.0), point1=(-1000.0, -750.0), point2=(
    -750.0, -1000.0), direction=CLOCKWISE)
s.ArcByCenterEnds(center=(-1000.0, 1000.0), point1=(-750.0, 1000.0), point2=(
    -1000.0, 750.0), direction=CLOCKWISE)
s.ArcByCenterEnds(center=(1000.0, 1000.0), point1=(1000.0, 750.0), point2=(
    750.0, 1000.0), direction=CLOCKWISE)
s.ArcByCenterEnds(center=(1000.0, -1000.0), point1=(750.0, -1000.0), point2=(
    1000.0, -750.0), direction=CLOCKWISE)
edges1 = e.findAt(  ((-970.710678,-970.710678,0.), ) )
p.projectEdgesOntoSketch(sketch=s, edges=(edges1[0],))
edges1 = e.findAt(  ((970.710678,-970.710678,0.), ) )
p.projectEdgesOntoSketch(sketch=s, edges=(edges1[0],))
edges1 = e.findAt(  ((970.710678,970.710678,0.), ) )
p.projectEdgesOntoSketch(sketch=s, edges=(edges1[0],))
edges1 = e.findAt(  ((-970.710678,970.710678,0.), ) )
p.projectEdgesOntoSketch(sketch=s, edges=(edges1[0],))
s.Line(point1=(750.0, 1000.0), point2=(900.0, 1000.0))
s.Line(point1=(1000.0, 750.0), point2=(1000.0, 900.0))
s.Line(point1=(-750.0, 1000.0), point2=(-900.0, 1000.0))
s.Line(point1=(-1000.0, 750.0), point2=(-1000.0, 900.0))
s.Line(point1=(750.0, -1000.0), point2=(900.0, -1000.0))
s.Line(point1=(1000.0, -750.0), point2=(1000.0, -900.0))
s.Line(point1=(-750.0, -1000.0), point2=(-900.0, -1000.0))
s.Line(point1=(-1000.0, -750.0), point2=(-1000.0, -900.0))
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
pickedFaces = f.findAt(  ((800.0, 800.0, 0.0), ) )
c , f, e, d = p.cells, p.faces, p.edges, p.datums
pickedCells = c.findAt((( 0.0, 0.0, 0.0), ) )
pickedFaces = f.findAt(((0.0,0.0,0.0) ,))
pickedEdges = e.findAt(((1000.0,10.0,0.0) ,))

p.PartitionCellBySketch(sketchPlane=pickedFaces[0], sketchUpEdge=pickedEdges[0], 
    cells=pickedCells, sketch=s)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

c, e, d = p.cells, p.edges, p.datums

pickedCells = c.findAt(  ((10.0, 10.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(904.329142, -769.030117, 0.0)), e.findAt(
    coordinates=(1000.0, -787.5, 0.0)), e.findAt(coordinates=(938.268343, 
    -992.387953, 0.0)), e.findAt(coordinates=(862.5, -1000.0, 0.0)))

p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, 900.0, 0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

pickedCells = c.findAt(  ((10.0, 10.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(1000.0, 862.5, 0.0)), e.findAt(
    coordinates=(769.030117, 904.329142, 0.0)), e.findAt(coordinates=(787.5, 
    1000.0, 0.0)), e.findAt(coordinates=(992.387953, 938.268343, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, 900.0, 0.025)), 
    cells=pickedCells, edges=pickedEdges, sense=FORWARD)

pickedCells = c.findAt(  ((10.0, 10.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(-862.5, 1000.0, 0.0)), e.findAt(
    coordinates=(-904.329142, 769.030117, 0.0)), e.findAt(coordinates=(
    -1000.0, 787.5, 0.0)), e.findAt(coordinates=(-992.387953, 938.268343, 
    0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, 900.0, 
    0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

pickedCells = c.findAt(  ((10.0, 10.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(-1000.0, -862.5, 0.0)), e.findAt(
    coordinates=(-769.030117, -904.329142, 0.0)), e.findAt(coordinates=(-787.5, 
    -1000.0, 0.0)), e.findAt(coordinates=(-992.387953, -938.268343, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, -900.0, 
    0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)


# Elastic-Plastic partition
p = mdb.models['Model-1'].parts['Part-1']
f, e, d = p.faces, p.edges, p.datums
pickedFaces = f.findAt(((0.0,0.0,0.0) ,))
pickedEdges = e.findAt(((1000.0, 10.0, 0.0),))
t = p.MakeSketchTransform(sketchPlane=pickedFaces[0], sketchPlaneSide=SIDE1,sketchUpEdge=pickedEdges[0], origin=(0.0, 
    0.0, 0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=5656.85, gridSpacing=141.42, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(850.0, 0.0))
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
pickedFaces = f.findAt(  ((400.0, 400.0, 0.0), ) )
c, f, e, d = p.cells, p.faces, p.edges, p.datums
pickedCells = c.findAt((( 0.0, 0.0, 0.0), ) )
pickedFaces = f.findAt(((0.0,0.0,0.0) ,))
pickedEdges = e.findAt(((1000.0,10.0,0.0) ,))
p.PartitionCellBySketch(sketchPlane=pickedFaces[0], sketchUpEdge=pickedEdges[0], cells=pickedCells, sketch=s)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

c, e, d = p.cells, p.edges, p.datums
pickedCells = c.findAt(  ((10.0, 10.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(850.0, 0.0, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, -900.0, 0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

# Crack Partition
p = mdb.models['Model-1'].parts['Part-1']
f, e, d = p.faces, p.edges, p.datums
pickedFaces = f.findAt(((0.0,0.0,0.0) ,))
pickedEdges = e.findAt(((1000.0, 10.0, 0.0),))
t = p.MakeSketchTransform(sketchPlane=pickedFaces[0], sketchPlaneSide=SIDE1,sketchUpEdge=pickedEdges[0], origin=(0.0, 
    0.0, 0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=5656.85, gridSpacing=141.42, transform=t)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['Part-1']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(150.0, 0.0))
#s.Line(point1=(-10.0, 0.0), point2=(10.0, 0.0))
s.CircleByCenterPerimeter(center=(10.0, 0.0), point1=(11.0, 0.0))
s.CircleByCenterPerimeter(center=(10.0, 0.0), point1=(10.25, 0.0))
s.CircleByCenterPerimeter(center=(10.0, 0.0), point1=(10.03, 0.0))
s.CircleByCenterPerimeter(center=(-10.0, 0.0), point1=(-10.03, 0.0))
session.viewports['Viewport: 1'].view.setValues(nearPlane=4808.13, 
    farPlane=4808.52, width=1.25268, height=1.61278, cameraPosition=(9.95239, 
    0.0435036, 4808.33), cameraTarget=(9.95239, 0.0435036, 0))
#s.Line(point1=(10.0, 0.03), point2=(10.0, -0.03))
#s.VerticalConstraint(entity=g[40], addUndoState=False)
#s.Line(point1=(10.0, 0.0), point2=(10.03, 0.0))
#s.HorizontalConstraint(entity=g[41], addUndoState=False)
p = mdb.models['Model-1'].parts['Part-1']
c, f, e, d = p.cells, p.faces, p.edges, p.datums
pickedFaces = f.findAt(  ((200.0, 200.0, 0.0), ) )
pickedCells = c.findAt((( 0.0, 0.0, 0.0), ) )
pickedFaces = f.findAt(((0.0,0.0,0.0) ,))
pickedEdges = e.findAt(((1000.0,10.0,0.0) ,))
p.PartitionCellBySketch(sketchPlane=pickedFaces[0], sketchUpEdge=pickedEdges[0], cells=pickedCells, sketch=s)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

c, e, d = p.cells, p.edges, p.datums
pickedCells = c.findAt(  ((100.0, 0.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(150.0, 0.0, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, -900.0, 0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

c, e, d = p.cells, p.edges, p.datums
pickedCells = c.findAt(  ((100.0, 0.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(-10.03, 0.0, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, -900.0, 0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

c, e, d = p.cells, p.edges, p.datums
pickedCells = c.findAt(  ((10.0, 10.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(11.0, 0.0, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, -900.0, 0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

c, e, d = p.cells, p.edges, p.datums
pickedCells = c.findAt(  ((9.0, 0.0, 0.033), ) )
pickedEdges =( e.findAt(coordinates=(10.25, 0.0, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, -900.0, 0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

c, e, d = p.cells, p.edges, p.datums
pickedCells = c.findAt(  ((10.02, 0.0, 0.033), ) )
pickedEdges =(e.findAt(coordinates=(10.03, 0.0, 0.0)))
p.PartitionCellByExtrudeEdge(line=e.findAt(coordinates=(1000.0, -900.0, 0.025)), cells=pickedCells, edges=pickedEdges, sense=FORWARD)

pickedCells = c.findAt(((0.0, 0.0, 0.1), ), ((10, 0, 0.1), ),((-10, 0, 0.1), ), ((10.1, 0, 0.1), ),((10.3, 0, 0.1), ))
e1, v1, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlaneNormalToEdge(edge=e1.findAt(coordinates=(-1000.0, -375.0, 
    0.0)), cells=pickedCells, point=p.InterestingPoint(edge=e1.findAt(
    coordinates=(-1000.0, -375.0, 0.0)), rule=MIDDLE))


pickedCells = c.findAt(((10, 0.01, 0.1), ), ((10, -0.01, 0.1), ) )
e1, v1, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlaneNormalToEdge(edge=e1.findAt(coordinates=( 10.02, 0.0, 
    0.0)), cells=pickedCells, point=p.InterestingPoint(edge=e1.findAt(
    coordinates=( 10.0, 0.0, 0.0)), rule=MIDDLE))

pickedCells = c.findAt(((-10, 0.01, 0.1), ),((-10, -0.01, 0.1), ) )
e1, v1, d1 = p.edges, p.vertices, p.datums
p.PartitionCellByPlaneNormalToEdge(edge=e1.findAt(coordinates=( -10.02, 0.0, 
    0.0)), cells=pickedCells, point=p.InterestingPoint(edge=e1.findAt(
    coordinates=( -10.0, 0.0, 0.0)), rule=MIDDLE))

###########################
# Create Region Sets
###########################

p = mdb.models['Model-1'].parts['Part-1']
Rigid_cells = p.cells.findAt( ((900.0, 900.0, 0.0), ), ((-900.0, 900.0, 0.0), ), ((900.0, -900.0, 0.0), ), ((-900.0, -900.0, 0.0), ) )
p.Set(cells=Rigid_cells, name='Rigid-Elastic_Region')
#: The set 'Rigid-Elastic_Region' has been created (4 faces).
Elastic_cells = p.cells.findAt( ((900.0, 0.0, 0.0), ) )
p.Set(cells=Elastic_cells, name='Elastic_Region')
#: The set 'Elastic_Region' has been created (1 face).
Elastic_Plastic_cells = p.cells.findAt( ((10.02, 0.02, 0.0), ), ((10.02, -0.02, 0.0), ),((-10.02, 0.02, 0.0), ), ((-10.02, -0.02, 0.0), ),((9.98, 0.02, 0.0), ), ((9.98, -0.02, 0.0), ), ((-9.98, 0.02, 0.0), ), ((-9.98, -0.02, 0.0), ), ((10.05, 0.05, 0.0), ), ((10.05, -0.05, 0.0), ), ((10.5, 0.5, 0.0), ),((10.5, -0.5, 0.0), ), ((50.0, 1.0, 0.0), ),((50.0, -1.0, 0.0), ), ((400.0, 0.0, 0.0), ) )
p.Set(cells=Elastic_Plastic_cells, name='Elastic-Plastic_Region')
#: The set 'Elastic-Plastic_Region' has been created (9 faces).


###########################
# Material
###########################


mdb.models['Model-1'].Material(name='Elastic')
mdb.models['Model-1'].Material(name='Elastic-Plastic')
mdb.models['Model-1'].Material(name='Elastic-Rigid')


mdb.models['Model-1'].materials['Elastic'].Elastic(table=((1.0, 1.0), ))
mdb.models['Model-1'].materials['Elastic-Plastic'].Elastic(table=((1.0, 1.0), ))
mdb.models['Model-1'].materials['Elastic-Plastic'].Plastic(hardening=COMBINED, dataType=PARAMETERS, table=((1.0, 1.0, 1.0), ))
mdb.models['Model-1'].materials['Elastic-Plastic'].plastic.CyclicHardening(parameters=ON, table=((1.0, 1.0, 1.0), ))
mdb.models['Model-1'].materials['Elastic-Rigid'].Elastic(table=((10000000.0, .3), ))


###########################
#  Assembly
###########################

# instances

a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['Part-1']
p.DatumCsysByThreePoints(name='Datum csys-2', coordSysType=CARTESIAN, origin=(0.0, 0.0, 0.0), point1=(1.0, 0.0, 0.0), point2=(1.0, 1.0, 0.0))
a.Instance(name='Part-1-1', part=p, dependent=OFF)

p = mdb.models['Model-1'].parts['Arc_INF_LEFT']
a.Instance(name='Arc_INF_LEFT-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Arc_INF_RIGHT']
a.Instance(name='Arc_INF_RIGHT-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Arc_SUP_LEFT']
a.Instance(name='Arc_SUP_LEFT-1', part=p, dependent=OFF)
p = mdb.models['Model-1'].parts['Arc_SUP_RIGHT']
a.Instance(name='Arc_SUP_RIGHT-1', part=p, dependent=OFF)

# Refernce points

a.ReferencePoint(point=(-1000.0, 1000.0, 0.05))
a.ReferencePoint(point=(1000.0, 1000.0, 0.05))
a.ReferencePoint(point=(1000.0, -1000.0, 0.05))
a.ReferencePoint(point=(-1000.0, -1000.0, 0.05))

# Sets

a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Part-1-1'].edges
f1 = a.instances['Part-1-1'].faces
v1 = a.instances['Part-1-1'].vertices
c1 = a.instances['Part-1-1'].cells

faces1 = f1.findAt( ((9.98, 0.0, 0.05), ), ((9.96, 0.0, 0.05), ), ((9.6, 0.0, 0.05), ), ((8.1, 0.0, 0.05), ), ((-9.98, 0.0, 0.05), ) )
a.Set(faces=faces1, name='CRACK_SEAM')
#: The set 'CRACK_SEAM' has been created (4 edges).

cells1 = c1.findAt(  ((9.96, 0.1, 0.0), ), ((9.96, -0.1, 0.0), ) )
a.Set(cells=cells1, name='FIELD-RIGHT')
#: The set 'FIELD-RIGHT' has been created (1 face).

cells1 = c1.findAt(  ((9.96, 0.1, 0.0), ), ((9.96, -0.1, 0.0), ), ((9.99, 0.01, 0.0), ), ((9.99, -0.01, 0.0), ), ((10.01, 0.01, 0.0), ), ((10.01, -0.01, 0.0), ) )
a.Set(cells=cells1, name='FULL-CRACK-FIELD-RIGHT')
#: The set 'FULL-CRACK-FIELD-RIGHT' has been created (1 face).

faces1 = f1.findAt(  ((9.96, 0.0, 0.05), ) )
a.Set(faces=faces1, name='FACES-RIGHT')
#: The set 'FACES-RIGHT' has been created (1 edge).
edges1 = e1.findAt(  ((10, 0.0, 0.05), ) )
a.Set(edges=edges1, name='LINE-RIGHT')
#: The set 'PONIT-RIGHT' has been created (1 vertex).
edges1 = e1.findAt(  ((-10, 0.0, 0.05), ) )
a.Set(edges=edges1, name='LINE-LEFT')
#: The set 'PONIT-RIGHT' has been created (1 vertex).

faces1 = f1.findAt( ((-1000, -850, 0.05), ), ((-850, -1000, 0.05), ), ((-970.710678,-970.710678,0.05), ) )
a.Set(faces=faces1, name='Model_IL')
#: The set 'Model_IL' has been created (3 edges).

faces1 = f1.findAt( ((1000, -850, 0.05), ), ((850, -1000, 0.05), ), ((970.710678,-970.710678,0.05), ) )
a.Set(faces=faces1, name='Model_IR')
#: The set 'Model_IR' has been created (3 edges).

faces1 = f1.findAt( ((1000, 850, 0.05), ), ((850, 1000, 0.05), ), ((970.710678,970.710678,0.05), ) )
a.Set(faces=faces1, name='Model_SR')
#: The set 'Model_SR' has been created (3 edges).

faces1 = f1.findAt( ((-1000, 850, 0.05), ), ((-850, 1000, 0.05), ), ((-970.710678,970.710678, 0.05), ) )
a.Set(faces=faces1, name='Model_SL')
#: The set 'Model_SL' has been created (3 edges).

f1 = a.instances['Arc_INF_LEFT-1'].faces
faces1 = f1.findAt( ((-1000, -850, 0.05), ), ((-850, -1000, 0.05), ), ((-970.710678,-970.710678,0.05), ))
a.Set(faces=faces1, name='Rig_IL')
#: The set 'Rig_IL' has been created (3 edges).

f1 = a.instances['Arc_SUP_LEFT-1'].faces
faces1 = f1.findAt( ((-1000, 850, 0.05), ), ((-850, 1000, 0.05), ), ((-970.710678, 970.710678,0.05), ))
a.Set(faces=faces1, name='Rig_SL')
#: The set 'Rig_SL' has been created (3 edges).

f1 = a.instances['Arc_SUP_RIGHT-1'].faces
faces1 = f1.findAt( ((1000, 850, 0.05), ), ((850, 1000, 0.05), ), ((970.710678, 970.710678,0.05), ))
a.Set(faces=faces1, name='Rig_SR')
#: The set 'Rig_SR' has been created (3 edges).

f1 = a.instances['Arc_INF_RIGHT-1'].faces
faces1 = f1.findAt( ((1000, -850, 0.05), ), ((850, -1000, 0.05), ), ((970.710678, -970.710678,0.05), ))
a.Set(faces=faces1, name='Rig_IR')
#: The set 'Rig_IR' has been created (3 edges).


# Interaction: create Seam

a = mdb.models['Model-1'].rootAssembly
pickedRegions = a.sets['CRACK_SEAM']
mdb.models['Model-1'].rootAssembly.engineeringFeatures.assignSeam(regions=pickedRegions)

# Crack creation ( In order to extract stress intensity factors in elastic computations

c1 = a.instances['Part-1-1'].cells
cells1 = c1.findAt(  ((9.98, 0.02, 0.05), ) ,((9.98, -0.02, 0.05), ),((10.02, 0.02, 0.05), ),((10.02, -0.02, 0.05), ))
crackFront = regionToolset.Region(cells=cells1)
a = mdb.models['Model-1'].rootAssembly
crackTip = a.sets['LINE-RIGHT']
a.engineeringFeatures.ContourIntegral(name='Crack_RIGHT', symmetric=OFF, 
    crackFront=crackFront, crackTip=crackTip, 
    extensionDirectionMethod=Q_VECTORS, qVectors=(((10.0, 0.0, 0.0), (10.01, 
    0.0, 0.0)), ), midNodePosition=0.5, collapsedElementAtTip=NONE)


# Create Seam Surfaces

f1 = a.instances['Part-1-1'].faces
Face1 = f1.findAt( ((9.98, 0.0, 0.05), ),((-9.98, 0.0, 0.05), ), ((9.96, 0.0, 0.05), ), ((9.6, 0.0, 0.05), ), ((8.1, 0.0, 0.05), ) )
a.Surface(side2Faces=Face1, name='Surf_Seam_SUP')
#: The surface 'Surf_Seam_INF' has been created (4 edges).

a.Surface(side1Faces=Face1, name='Surf_Seam_INF')
#: The surface 'Surf_Seam_SUP' has been created (4 edges).


# Contact properties

mdb.models['Model-1'].ContactProperty('IntProp_Crack')
mdb.models['Model-1'].interactionProperties['IntProp_Crack'].TangentialBehavior(formulation=FRICTIONLESS)
mdb.models['Model-1'].interactionProperties['IntProp_Crack'].NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON, constraintEnforcementMethod=DEFAULT)
#: The interaction property "IntProp_Crack" has been created.


mdb.models['Model-1'].ContactStd(name='Crack_Contact', createStepName='Initial')
r11=a.surfaces['Surf_Seam_INF']
r12=a.surfaces['Surf_Seam_SUP']
mdb.models['Model-1'].interactions['Crack_Contact'].includedPairs.setValuesInStep(stepName='Initial', useAllstar=OFF, addPairs=((r11, r12), ))
mdb.models['Model-1'].interactions['Crack_Contact'].contactPropertyAssignments.appendInStep(
    stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp_Crack'), (r11, 
    r12, 'IntProp_Crack')))
#: The interaction "Crack_Contact" has been created.


#####################################
#       Sections Assignement
#####################################


a = mdb.models['Model-1'].parts['Part-1']
mdb.models['Model-1'].HomogeneousSolidSection(material='Elastic-Rigid', name='Section_Elastic-Rigid', thickness=None)
#mdb.models[Model].PEGSection(name='Section_Elastic-Rigid', material='Elastic-Rigid', thickness=1.0, wedgeAngle1=0.0, wedgeAngle2=0.0)
Rigid_region = a.sets['Rigid-Elastic_Region']
a.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Rigid_region , sectionName='Section_Elastic-Rigid', thicknessAssignment=FROM_SECTION)
#
# : Elastic region creation, Section creation and assignment
#
Elastic_region = a.sets['Elastic_Region']
mdb.models['Model-1'].HomogeneousSolidSection(material='Elastic', name='Section_Elastic', thickness=None)
#mdb.models[Model].PEGSection(name='Section_Elastic', material='Elastic', thickness=1.0, wedgeAngle1=0.0, wedgeAngle2=0.0)
a.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Elastic_region , sectionName='Section_Elastic', thicknessAssignment=FROM_SECTION)
#
# : Elastic Plastic region creation, Section creation and assignment
#
Elastic_Plastic_region = a.sets['Elastic-Plastic_Region']
mdb.models['Model-1'].HomogeneousSolidSection(material='Elastic-Plastic', name='Section_Elastic-Plastic', thickness=None)
#mdb.models[Model].PEGSection(name='Section_Elastic-Plastic', material='Elastic-Plastic', thickness=1.0, wedgeAngle1=0.0, wedgeAngle2=0.0)
a.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Elastic_Plastic_region , sectionName='Section_Elastic-Plastic', thicknessAssignment=FROM_SECTION)
#a.SectionAssignment(offset=0.0, offsetField='', offsetType=MIDDLE_SURFACE, region=Elastic_region , sectionName='Section_Elastic-Plastic', thicknessAssignment=FROM_SECTION)  # to test with a full model elastic-plastic


#####################################
#              Step
#####################################

mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
mdb.models['Model-1'].StaticStep(name='Step-2', previous='Step-1')
mdb.models['Model-1'].StaticStep(name='Step-3', previous='Step-2')

#####################################
#  Field outputs request
#####################################

mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].suppress()

regionDef=mdb.models['Model-1'].rootAssembly.sets['FULL-CRACK-FIELD-RIGHT']

mdb.models['Model-1'].FieldOutputRequest(name='FIELD-DISP-RIGHT',createStepName='Step-1',
    variables=('S', 'U', 'E','PEEQ','SDV'), frequency=1, region=regionDef )

'''
regionDef=mdb.models['Model-1'].rootAssembly.sets['LINE-RIGHT']
mdb.models['Model-1'].FieldOutputRequest(name='LINE-DISP-RIGHT',createStepName='Step-1',
    variables=('COORD', 'U',  'MISES', 'PE', 'PEEQ', 'S'), timeInterval=dimensions.time_inc, region=regionDef,
    sectionPoints=DEFAULT, rebar=EXCLUDE)

regionDef=mdb.models['Model-1'].rootAssembly.sets['FACES-RIGHT']
mdb.models['Model-1'].FieldOutputRequest(name='FACES-DISP-RIGHT',createStepName='Step-1',
    variables=( 'COORD', 'U', 'MISES', 'PE', 'PEEQ','S'), timeInterval=dimensions.time_inc, region=regionDef,
    sectionPoints=DEFAULT, rebar=EXCLUDE)

mdb.models['Model-1'].FieldOutputRequest(name='WHOLE_MODEL', region=MODEL ,
    createStepName='Step-1', frequency=1, variables=('S', 'U', 'E','PEEQ','SDV'))
'''

#####################################
#  History outputs
#####################################

mdb.models['Model-1'].historyOutputRequests['H-Output-1'].suppress()

mdb.models['Model-1'].HistoryOutputRequest(name='CRACK-RIGHT-SIF', 
    createStepName='Step-1', contourIntegral='Crack_RIGHT', 
    sectionPoints=DEFAULT, rebar=EXCLUDE, numberOfContours=23, 
    contourType=K_FACTORS)

mdb.models['Model-1'].historyOutputRequests['CRACK-RIGHT-SIF'].suppress()


regionDef=mdb.models['Model-1'].rootAssembly.sets['FACES-RIGHT']
mdb.models['Model-1'].HistoryOutputRequest(name='FACES-DISP-RIGHT', 
    createStepName='Step-1', variables=('COOR1', 'COOR2','COOR3' , 'U1', 'U2', 'U3' ), 
    timeInterval=1, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

regionDef=mdb.models['Model-1'].rootAssembly.sets['LINE-RIGHT']
mdb.models['Model-1'].HistoryOutputRequest(name='LINE-DISP-RIGHT', 
    createStepName='Step-1', variables=('COOR1', 'COOR2','COOR3', 'U1', 'U2', 'U3'), 
    timeInterval=1, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

regionDef=mdb.models['Model-1'].rootAssembly.sets['FIELD-RIGHT']
mdb.models['Model-1'].HistoryOutputRequest(name='FIELD-DISP-RIGHT', 
    createStepName='Step-1', variables=('COOR1', 'COOR2','COOR3', 'U1', 'U2', 'U3'), 
    timeInterval=1, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

regionDef=mdb.models['Model-1'].rootAssembly.sets['Rig_IL']
mdb.models['Model-1'].HistoryOutputRequest(name='RIGID-IL', 
    createStepName='Step-1', variables=('U1', 'U2', 'U3'), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

regionDef=mdb.models['Model-1'].rootAssembly.sets['Rig_IR']
mdb.models['Model-1'].HistoryOutputRequest(name='RIGID-IR', 
    createStepName='Step-1', variables=('U1', 'U2', 'U3'), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

regionDef=mdb.models['Model-1'].rootAssembly.sets['Rig_SR']
mdb.models['Model-1'].HistoryOutputRequest(name='RIGID-SR', 
    createStepName='Step-1', variables=('U1', 'U2', 'U3'), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)

regionDef=mdb.models['Model-1'].rootAssembly.sets['Rig_SL']
mdb.models['Model-1'].HistoryOutputRequest(name='RIGID-SL', 
    createStepName='Step-1', variables=('U1', 'U2', 'U3'), region=regionDef, 
    sectionPoints=DEFAULT, rebar=EXCLUDE)


####################################
#  Constrains
####################################


a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
'''
# MPC constrains ( TIE or BEAM )

refPoints1=(r1[4], )
region1=regionToolset.Region(referencePoints=refPoints1)
region2=a.sets['Model_SL']
mdb.models['Model-1'].MultipointConstraint(name='MPC_Tie_SL', controlPoint=region1, 
    surface=region2,mpcType=TIE_MPC, userMpde=DOF_MODE_MPC, userType=0, csys=None)

refPoints1=(r1[5], )
region1=regionToolset.Region(referencePoints=refPoints1)
region2=a.sets['Model_SR']
mdb.models['Model-1'].MultipointConstraint(name='MPC_Tie_SR', controlPoint=region1, 
    surface=region2,mpcType=TIE_MPC, userMpde=DOF_MODE_MPC, userType=0, csys=None)

refPoints1=(r1[6], )
region1=regionToolset.Region(referencePoints=refPoints1)
region2=a.sets['Model_IR']
mdb.models['Model-1'].MultipointConstraint(name='MPC_Tie_IR', controlPoint=region1, 
    surface=region2,mpcType=TIE_MPC, userMpde=DOF_MODE_MPC, userType=0, csys=None)

refPoints1=(r1[7], )
region1=regionToolset.Region(referencePoints=refPoints1)
region2=a.sets['Model_IL']
mdb.models['Model-1'].MultipointConstraint(name='MPC_Tie_IL', controlPoint=region1, 
    surface=region2,mpcType=TIE_MPC, userMpde=DOF_MODE_MPC, userType=0, csys=None)

'''
# Rigid bodies

f1 = a.instances['Arc_SUP_LEFT-1'].faces
faces1 = f1.findAt( ((-1000, 850, 0.05), ), ((-850, 1000, 0.05), ), ((-970.710678,970.710678,0.05), ), ((-1.029289322E+03,679.289322,0.05), ),((-679.289322,1.029289322E+03,0.05), ))
region2=regionToolset.Region(faces=faces1)
r1 = a.referencePoints
refPoints1=(r1[12], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Rigid_Body_SL', refPointRegion=region1, bodyRegion=region2)

f1 = a.instances['Arc_SUP_RIGHT-1'].faces
faces1 = f1.findAt( ((1000, 850, 0.05), ), ((850, 1000, 0.05), ), ((970.710678,970.710678,0.05), ), ((1.029289322E+03,679.289322,0.05), ),((679.289322,1.029289322E+03,0.05), ))
region2=regionToolset.Region(faces=faces1)
r1 = a.referencePoints
refPoints1=(r1[13], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Rigid_Body_SR', refPointRegion=region1, bodyRegion=region2)

f1 = a.instances['Arc_INF_RIGHT-1'].faces
faces1 = f1.findAt( ((1000, -850, 0.05), ), ((850, -1000, 0.05), ), ((970.710678,-970.710678,0.05), ), ((1.029289322E+03,-679.289322,0.05), ),((679.289322,-1.029289322E+03,0.05), ))
region2=regionToolset.Region(faces=faces1)
r1 = a.referencePoints
refPoints1=(r1[14], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Rigid_Body_IR', refPointRegion=region1, bodyRegion=region2)

f1 = a.instances['Arc_INF_LEFT-1'].faces
faces1 = f1.findAt( ((-1000, -850, 0.05), ), ((-850, -1000, 0.05), ), ((-970.710678,-970.710678,0.05), ),((-1.029289322E+03,-679.289322,0.05), ),((-679.289322,-1.029289322E+03,0.05), ) )
region2=regionToolset.Region(faces=faces1)
r1 = a.referencePoints
refPoints1=(r1[15], )
region1=regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].RigidBody(name='Rigid_Body_IL', refPointRegion=region1, bodyRegion=region2)



# Tie

region1=a.sets['Rig_SL']
region2=a.sets['Model_SL']
mdb.models['Model-1'].Tie(name='Tie_SL', master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

region1=a.sets['Rig_SR']
region2=a.sets['Model_SR']
mdb.models['Model-1'].Tie(name='Tie_SR', master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

region1=a.sets['Rig_IL']
region2=a.sets['Model_IL']
mdb.models['Model-1'].Tie(name='Tie_IL', master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)

region1=a.sets['Rig_IR']
region2=a.sets['Model_IR']
mdb.models['Model-1'].Tie(name='Tie_IR', master=region1, slave=region2, positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)


# Periodic boundary condition:

a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.findAt(((-10.003827, -0.019239, 0.1), ), ((-9.996173, 0.019239, 
    0.1), ), ((9.996173, -0.019239, 0.1), ), ((10.003827, 0.019239, 0.1), ), ((10.003827, 
    -0.019239, 0.1), ),  ((10.102572, -0.003827, 0.1), ), ((-10.003827, 0.019239, 0.1), ), ((10.493656, -0.03189, 0.1), ), ((57.30796, -0.127561, 0.1), ), ((10.102572, 0.003827, 0.1), ), ((9.996173, 
    0.019239, 0.1), ), ((57.30796, 0.127561, 0.1), ), ((10.493656, 0.03189, 
    0.1), ), ((-9.996173, -0.019239, 0.1), ), (( 433.529696, -433.529696, 0.1), ), (( 892.89624, -313.047597, 0.1), ), ((-806.343363, -968.109721, 0.1), ), ((-968.109721, 806.343363, 0.1), ), ((968.109721, -806.343363, 0.1), ),   ((806.343363, 968.109721, 0.1), ) )
region1=regionToolset.Region(side1Faces=side1Faces1)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.findAt(((-10.003827, -0.019239, 0.0), ), ((-9.996173, 0.019239, 
    0.0), ), ((9.996173, -0.019239, 0.0), ), ((10.003827, 0.019239, 0.0), ), ((10.003827, 
    -0.019239, 0.0), ),  ((10.102572, -0.003827, 0.0), ), ((-10.003827, 0.019239, 0.0), ), ((10.493656, -0.03189, 0.0), ), ((57.30796, -0.127561, 0.0), ), ((10.102572, 0.003827, 0.0), ), ((9.996173, 
    0.019239, 0.0), ), ((57.30796, 0.127561, 0.0), ), ((10.493656, 0.03189, 
    0.0), ), ((-9.996173, -0.019239, 0.0), ), (( 433.529696, -433.529696, 0.0), ), (( 892.89624, -313.047597, 0.0), ), ((-806.343363, -968.109721, 0.0), ), ((-968.109721, 806.343363, 0.0), ), ((968.109721, -806.343363, 0.0), ), ((806.343363, 968.109721, 0.0), ) )
region2=regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].Tie(name='Periodic-Tie', master=region1, slave=region2, 
    positionToleranceMethod=COMPUTED, adjust=OFF, tieRotations=ON, 
    thickness=ON)


# Mid-plane cut

a = mdb.models['Model-1'].rootAssembly
c1 = a.instances['Part-1-1'].cells
pickedCells = c1.findAt(((-10.003827, -0.019239, 0.05), ), ((-9.996173, 
    0.019239, 0.05), ), ((10.003827, 0.019239, 0.05), ), ((9.996173, -0.019239, 
    0.05), ), ((-10.003827, 0.019239, 0.05), ), ((10.493656, -0.03189, 0.05), ), (
    (57.30796, -0.127561, 0.05), ), ((10.003827, -0.019239, 0.05), ), ((
    10.102572, -0.003827, 0.05), ), ((10.102572, 0.003827, 0.05), ), ((9.996173, 
    0.019239, 0.05), ), ((57.30796, 0.127561, 0.05), ), ((10.493656, 0.03189, 
    0.05), ), ((-9.996173, -0.019239, 0.05), ), ((200, -0.1, 0.05), ),((900, 0.1, 0.05), ),
    ((900, -900, 0.05), ),((900, 900, 0.05), ), ((-900, -900, 0.05), ),((-900, 900, 0.05), ), )
e1 = a.instances['Part-1-1'].edges
a.PartitionCellByPlaneNormalToEdge(edge=e1.findAt(coordinates=(1000.0, 750.0, 
    0.025)), cells=pickedCells, 
    point=a.instances['Part-1-1'].InterestingPoint(edge=e1.findAt(
    coordinates=(1000.0, 750.0, 0.025)), rule=MIDDLE))

# Point and ligament sets: 

v1 = a.instances['Part-1-1'].vertices
verts1 = v1.findAt(((10.0, 0.0, 0.05), ))
a.Set(vertices=verts1, name='POINTE-RIGHT')
verts1 = v1.findAt(((-10.0, 0.0, 0.05), ))
a.Set(vertices=verts1, name='POINTE-LEFT')

e1 = a.instances['Part-1-1'].edges
edges1 = e1.findAt(((45.75, 0.0, 0.05), ), ((10.4375, 0.0, 0.05), ), ((10.0075, 0.0, 0.05), ), ((10.085, 0.0, 0.05), ))
a.Set(edges=edges1, name='LIGAMENT-RIGHT')

e1 = a.instances['Part-1-1'].edges
edges1 = e1.findAt(((9.9, 0.0, 0.05), ), ((9.99, 0.0, 0.05), ) )
a.Set(edges=edges1, name='LIPS-RIGHT')

f1 = a.instances['Part-1-1'].faces
faces1 = f1.findAt(((10.085, 0.01, 0.05), ), ((10.085, -0.01, 0.05), ) )
a.Set(faces=faces1, name='SECTION-RIGHT')


# Filed Output Request for the crack tip

regionDef=mdb.models['Model-1'].rootAssembly.sets['POINTE-RIGHT']
'''
mdb.models['Model-1'].FieldOutputRequest(name='POINTE-RIGHT',createStepName='Step-1',
    variables=('CDISP', 'CF', 'COORD', 'U', 'CSTRESS', 'LE', 'MISES', 'PE', 'PEEQ', 
    'PEMAG','RF', 'S'), timeInterval=dimensions.time_inc, region=regionDef,
    sectionPoints=DEFAULT, rebar=EXCLUDE)
'''

# History Output Request for the crack tip

mdb.models['Model-1'].HistoryOutputRequest(name='POINTE-DISP-RIGHT', 
    createStepName='Step-1', variables=('COOR1', 'COOR2','COOR3', 'U1', 'U2', 'U3'), 
    timeInterval=1, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

# History Output Request for the crack section
regionDef=mdb.models['Model-1'].rootAssembly.sets['SECTION-RIGHT']
mdb.models['Model-1'].HistoryOutputRequest(name='SECTION-DISP-RIGHT', 
    createStepName='Step-1', variables=('COOR1', 'COOR2','COOR3', 'U1', 'U2', 'U3'), 
    timeInterval=1, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

# History Output Request for the crack lips
regionDef=mdb.models['Model-1'].rootAssembly.sets['LIPS-RIGHT']
mdb.models['Model-1'].HistoryOutputRequest(name='LIPS-DISP-RIGHT', 
    createStepName='Step-1', variables=('COOR1', 'COOR2','COOR3', 'U1', 'U2', 'U3'), 
    timeInterval=1, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)

###################################
#  Loads
###################################

r1 = a.referencePoints
refPoints1=(r1[12], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='SUP_LEFT', 
    createStepName='Step-1', region=region, cf1= -1.0, cf2= 1.0, cf3 =1.0, 
    distributionType=UNIFORM, field='', localCsys=None)

r1 = a.referencePoints
refPoints1=(r1[13], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='SUP_RIGHT', 
    createStepName='Step-1', region=region, cf1= 1.0, cf2= 1.0, cf3 =1.0,
    distributionType=UNIFORM, field='', localCsys=None)

r1 = a.referencePoints
refPoints1=(r1[14], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='INF_RIGHT', 
    createStepName='Step-1', region=region, cf1= 1.0, cf2=-1.0, cf3 =-1.0,
    distributionType=UNIFORM, field='', localCsys=None)

r1 = a.referencePoints
refPoints1=(r1[15], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].ConcentratedForce(name='INF_LEFT', 
    createStepName='Step-1', region=region, cf1=-1.0, cf2=-1.0, cf3 =-1.0,
    distributionType=UNIFORM, field='', localCsys=None)


###################################
#  Boundary Conditions
###################################

region = a.sets['LIGAMENT-RIGHT']
mdb.models['Model-1'].DisplacementBC(name='Ligament-RIGHT', 
    createStepName='Step-1', region=region, u1=UNSET, u2=0.0, u3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['POINTE-RIGHT']
mdb.models['Model-1'].DisplacementBC(name='Pointe-RIGHT', 
    createStepName='Step-1', region=region, u1=0.0, u2=0.0, u3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['POINTE-LEFT']
mdb.models['Model-1'].DisplacementBC(name='Pointe-LEFT', 
    createStepName='Step-1', region=region, u1=UNSET, u2=0.0, u3=0.0, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['LINE-RIGHT']
mdb.models['Model-1'].DisplacementBC(name='Line-RIGHT', 
    createStepName='Step-1', region=region, u1=0.0, u2=0.0, u3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)

region = a.sets['LINE-LEFT']
mdb.models['Model-1'].DisplacementBC(name='Line-LEFT', 
    createStepName='Step-1', region=region, u1=UNSET, u2=0.0, u3=UNSET, 
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', 
    localCsys=None)


r1 = a.referencePoints
refPoints1=(r1[12], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='SUP_LEFT', createStepName='Step-1', 
    region=region, u1=-1.0, u2=1.0, u3=1.0, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

r1 = a.referencePoints
refPoints1=(r1[13], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='SUP_RIGHT', createStepName='Step-1', 
    region=region, u1=1.0, u2=1.0, u3=1.0, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

r1 = a.referencePoints
refPoints1=(r1[14], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='INF_RIGHT', createStepName='Step-1', 
    region=region, u1=1.0, u2=-1.0, u3=1.0, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)

r1 = a.referencePoints
refPoints1=(r1[15], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='INF_LEFT', createStepName='Step-1', 
    region=region, u1=-1.0, u2=-1.0, u3=1.0, amplitude=UNSET, fixed=OFF, 
    distributionType=UNIFORM, fieldName='', localCsys=None)





#################################
#   Mesh
#################################


a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Part-1-1'].edges

# Seed edges:

pickedEdges = e1.findAt(((10.027716, 0.011481, 0.), ), ((10.011481, -0.027716, 
    0.), ), ((9.972284, -0.011481, 0.), ), ((9.988519, 0.027716, 0.), ), ((10.027716, 0.011481, 0.05), ), ((10.011481, -0.027716, 0.05), ), ((9.972284, -0.011481, 0.05), ), ((9.988519, 0.027716, 0.05), ),((10.027716, 0.011481, 0.1), ), ((10.011481, -0.027716, 0.1), ), ((9.972284, -0.011481, 0.1), ), ((9.988519, 0.027716, 0.1), ))
a.seedEdgeByNumber(edges=pickedEdges, number=(dimensions.thet_len-1)/4, constraint=FIXED)

pickedEdges = e1.findAt( ((10.,250.E-03,0.), ), ((10.,-250.E-03,0.), ), ((10.,250.E-03,0.05), ), ((10.,-250.E-03,0.05), ), ((10.,250.E-03,0.1), ), ((10.,-250.E-03,0.1), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=(dimensions.thet_len-1)/2, constraint=FIXED)

pickedEdges = e1.findAt( ((10.,1.,0.), ),((10.,-1.,0.), ), ((10.,1.,0.05), ),((10.,-1.,0.05), ), ((10.,1.,0.1), ),((10.,-1.,0.1), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=(dimensions.thet_len-1)/2, constraint=FIXED)

pickedEdges = e1.findAt( ((10.,0.01,0), ), ((10.,-0.01,0), ), ((9.99,0.,0.), ),((10.01,0.,0.), ),((10.,0.01,0.05), ), ((10.,-0.01,0.05), ), ((9.99,0.,0.05), ),((10.01,0.,0.05), ),((10.,0.01,0.1), ), ((10.,-0.01,0.1), ), ((9.99,0.,0.1), ),((10.01,0.,0.1), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=15, constraint=FREE)

pickedEdges = e1.findAt( ((9.95,0.,0.), ), ((9.95,0.,0.05), ), ((10.05,0.,0.1), ))
a.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, ratio=10.0, number = dimensions.rad_len-1, constraint=FIXED)
pickedEdges = e1.findAt( ((9.95,0.,0.1), ), ((10.05,0.,0.), ), ((10.05,0.,0.05), ) )
a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, ratio=10.0, number = dimensions.rad_len-1, constraint=FIXED)


pickedEdges = e1.findAt( ((9.5,0.,0.), ), ((9.5,0.,0.05), ) ,  ((10.5,0.,0.1), ))
a.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, ratio=6.0, number=(dimensions.rad_len-1)/2, constraint=FIXED)
#a.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, minSize=0.015, maxSize=0.07, constraint=FIXED)

pickedEdges = e1.findAt( ((9.5,0.,0.1), ), ((10.5,0.,0.), ), ((10.5,0.,0.05), ) )
a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, ratio=6.0, number=(dimensions.rad_len-1)/2, constraint=FIXED)
#a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, minSize=0.015, maxSize=0.07, constraint=FIXED)


pickedEdges = e1.findAt( ((10.,0.,0.02), ), ((10.,0.,0.08), ),((10.03,0.,0.02), ), ((10.03,0.,0.08), ),((10.25,0.,0.02), ), ((10.25,0.,0.08), ),((150.,0.,0.08), ),((150.,0.,0.02), ) ,((1000.,900.,0.08), ),((1000.,900.,0.02), ),((1000.,-900.,0.08), ),((1000.,-900.,0.02), ),((-1000.,900.,0.08), ),((-1000.,900.,0.02), ),((-1000.,-900.,0.08), ),((-1000.,-900.,0.02), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=(dimensions.z_len-1)/2, constraint=FIXED)

pickedEdges = e1.findAt( ((100.,0.,0.), ), ((100.,0.,0.05), ) )
a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, minSize=0.07, maxSize=15.0, constraint=FIXED)
pickedEdges = e1.findAt( ((100.,0.,0.1), ) )
a.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, minSize=0.07, maxSize=15.0, constraint=FIXED)

pickedEdges = e1.findAt( ((-12.,0.,0.), ), ((-12.,0.,0.05), ) )
a.seedEdgeByBias(biasMethod=SINGLE, end2Edges=pickedEdges, minSize=0.07, maxSize=15.0, constraint=FIXED)
pickedEdges = e1.findAt( ((-12.,0.,0.1), ) )
a.seedEdgeByBias(biasMethod=SINGLE, end1Edges=pickedEdges, minSize=0.07, maxSize=15.0, constraint=FIXED)

pickedEdges = e1.findAt( ((8.,0.,0.), ), ((8.,0.,0.05), ), ((8.,0.,0.1), ) )
a.seedEdgeByBias(biasMethod=DOUBLE, endEdges=pickedEdges, minSize=0.07, maxSize=1.7, constraint=FIXED)

pickedEdges = e1.findAt( ((0.,150.0,0.), ), ((0.,-150.0,0.), ), ((0.,150.0,0.05), ), ((0.,-150.0,0.05), ), ((0.,150.0,0.1), ), ((0.,-150.0,0.1), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=30, constraint=FIXED)

pickedEdges = e1.findAt( ((850.,0.,0.), ),  ((850.,0.,0.1), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=60, constraint=FIXED)

pickedEdges = e1.findAt( ((1000.,1.,0.), ), ((-1000.,1.,0.), ), ((1.,1000.,0.), ),((1.,-1000.,0.), ), ((1000.,1.,0.1), ), ((-1000.,1.,0.1), ), ((1.,1000.,0.1), ),((1.,-1000.,0.1), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=16, constraint=FIXED)

pickedEdges = e1.findAt(((-1000, -850, 0.0), ), ((-850, -1000, 0.0), ), ((-970.710678,-970.710678,0.), ), ((1000, -850, 0.0), ), ((850, -1000, 0.0), ), ((970.710678,-970.710678,0.), ), ((1000, 850, 0.0), ), ((850, 1000, 0.0), ), ((970.710678,970.710678,0.), ), ((-1000, 850, 0.0), ), ((-850, 1000, 0.0), ), ((-970.710678,970.710678,0.), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FIXED)

pickedEdges = e1.findAt(((-823.223305,-823.223305,0.), ), ((823.223305,-823.223305,0.), ), ((823.223305,823.223305,0.), ), ((-823.223305,823.223305,0.), ) )
a.seedEdgeByNumber(edges=pickedEdges, number=5, constraint=FIXED)


e1 = a.instances['Arc_INF_LEFT-1'].edges
pickedEdges = e1.findAt(((-1000, -850, 0.0), ), ((-850, -1000, 0.0), ), ((-970.710678,-970.710678,0.), ), ((-679.289322,-1.029289322E+03,0),), (( -1.029289322E+03,-679.289322,0. ),)  )
a.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FIXED)

e1 = a.instances['Arc_INF_RIGHT-1'].edges
pickedEdges = e1.findAt(  ((1000, -850, 0.0), ), ((850, -1000, 0.0), ), ((970.710678,-970.710678,0.), ),  (( 679.289322,-1.029289322E+03,0),), (( 1.029289322E+03,-679.289322,0. ),)  )
a.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FIXED)

e1 = a.instances['Arc_SUP_LEFT-1'].edges
pickedEdges = e1.findAt(((-1000, 850, 0.0), ), ((-850, 1000, 0.0), ), ((-970.710678,970.710678,0.), ) ,  ((-679.289322,1.029289322E+03,0),), (( -1.029289322E+03,679.289322,0. ),) )
a.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FIXED)

e1 = a.instances['Arc_SUP_RIGHT-1'].edges
pickedEdges = e1.findAt( ((1000, 850, 0.0), ), ((850, 1000, 0.0), ), ((970.710678,970.710678,0.), ),  (( 679.289322, 1.029289322E+03,0),), (( 1.029289322E+03,679.289322,0. ),)  )
a.seedEdgeByNumber(edges=pickedEdges, number=3, constraint=FIXED)




# Elements control

#elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
#    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
#    hourglassControl=DEFAULT, distortionControl=DEFAULT)

elemType1 = mesh.ElemType(elemCode=C3D8, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)


a = mdb.models['Model-1'].rootAssembly
c1 = a.instances['Part-1-1'].cells
pickedRegions = c1.findAt(  ((9.99, 0.01, 0.0), ), ((9.99, -0.01, 0.0), ), ((10.01, 0.01, 0.0), ), ((10.01, -0.01, 0.0), ), ((9.99, 0.01, 0.1), ), ((9.99, -0.01, 0.1), ), ((10.01, 0.01, 0.1), ), ((10.01, -0.01, 0.1), ), ((-9.99, 0.01, 0.0), ), ((-9.99, -0.01, 0.0), ), ((-10.01, 0.01, 0.0), ), ((-10.01, -0.01, 0.0), ), ((-9.99, 0.01, 0.1), ), ((-9.99, -0.01, 0.1), ), ((-10.01, 0.01, 0.1), ), ((-10.01, -0.01, 0.1), ) )
pickedRegions_Type =(pickedRegions, )
a.setElementType(regions=pickedRegions_Type, elemTypes=(elemType1, elemType2, elemType3))
a.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=STRUCTURED)


a = mdb.models['Model-1'].rootAssembly
c1 = a.instances['Part-1-1'].cells
pickedRegions = c1.findAt( ((10.5, 0.1, 0.0), ),((10.5, -0.1, 0.0), ),  ((50.0, 0.1, 0.0), ),((50.0, -0.1, 0.0), ), ((400.0, 0.0, 0.0), ), ((900.0, 900.0, 0.0), ), ((-900.0, 900.0, 0.0), ), ((900.0, -900.0, 0.0), ), ((-900.0, -900.0, 0.0), ), ((900.0, 0.0, 0.0), ), ((10.5, 0.1, 0.1), ),((10.5, -0.1, 0.1), ),  ((50.0, 0.1, 0.1), ),((50.0, -0.1, 0.1), ) , ((400.0, 0.0, 0.1), ), ((900.0, 900.0, 0.1), ), ((-900.0, 900.0, 0.1), ), ((900.0, -900.0, 0.1), ), ((-900.0, -900.0, 0.1), ), ((900.0, 0.0, 0.1), ) )
pickedRegions_Type =(pickedRegions, )
a.setElementType(regions=pickedRegions_Type, elemTypes=(elemType1, elemType2, elemType3))
a.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)

a = mdb.models['Model-1'].rootAssembly
c1 = a.instances['Part-1-1'].cells
pickedRegions = c1.findAt(  ((9.96, 0.01, 0.0), ), ((9.96, -0.01, 0.0), ),  ((9.96, 0.01, 0.1), ), ((9.96, -0.01, 0.1), ) )
pickedRegions_Type =(pickedRegions, )
a.setElementType(regions=pickedRegions_Type, elemTypes=(elemType1, elemType2, elemType3))
a.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=STRUCTURED)


# Generate Mesh

partInstances =(a.instances['Part-1-1'], a.instances['Arc_SUP_RIGHT-1'], a.instances['Arc_SUP_LEFT-1'], a.instances['Arc_INF_RIGHT-1'], a.instances['Arc_INF_LEFT-1'], )

a.generateMesh(regions=partInstances)

##############################
# Save 
##############################

mdb.saveAs( pathName='3D_Model')
#: The model database has been saved to "Champ_3D_circular_partition.cae".
