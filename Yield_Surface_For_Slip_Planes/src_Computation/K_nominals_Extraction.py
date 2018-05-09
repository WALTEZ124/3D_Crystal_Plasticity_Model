def K_nominals_Extraction(odbSrc, jobName):
    jobPath = os.path.join( odbSrc,jobName +'.odb')
    odb=openOdb(path= jobPath)
    KI   = xyPlot.XYDataFromHistory(odb=odb, outputVariableName='Stress intensity factor K1: K1 at CRACK-RIGHT-SIF_CRACK_RIGHT__PICKEDSET30-5__Contour_22', steps=('Step-1', ), ).data[-1][1]    
    KII  = xyPlot.XYDataFromHistory(odb=odb, outputVariableName='Stress intensity factor K2: K2 at CRACK-RIGHT-SIF_CRACK_RIGHT__PICKEDSET30-5__Contour_22', steps=('Step-1', ), ).data[-1][1]
    KIII = xyPlot.XYDataFromHistory(odb=odb, outputVariableName='Stress intensity factor K3: K3 at CRACK-RIGHT-SIF_CRACK_RIGHT__PICKEDSET30-5__Contour_22', steps=('Step-1', ), ).data[-1][1]
    odb.close()
    Keq = sqrt(pow(KI,2)+pow(KII,2)+pow(KIII,2))
    print 'KI   = ', KI/sqrt(1000) ,'MPa m 0.5'
    print 'KII  = ', KII/sqrt(1000) ,'MPa m 0.5'
    print 'KIII = ', KIII/sqrt(1000) ,'MPa m 0.5'
    print 'Keq = ', Keq/sqrt(1000) ,'MPa m 0.5'
    return  KI , KII, KIII, Keq
