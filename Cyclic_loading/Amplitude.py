mdb.models['Model-1'].PeriodicAmplitude(name='Amp-1', timeSpan=STEP, 
    frequency=0.2, start=0.0, a_0=0.0, data=((3.0, 5.0), ))
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#8 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='Surf-1')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=5.0, 
    amplitude=UNSET)
mdb.models['Model-1'].loads['Load-1'].setValues(amplitude='Amp-1')
