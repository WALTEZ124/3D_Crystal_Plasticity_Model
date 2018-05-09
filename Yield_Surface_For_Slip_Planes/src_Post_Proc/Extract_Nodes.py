# -*- coding: utf-8 -*-
def Extract_Nodes_Field_Output(odb):  
    # It's better to use pure elastic equibiaxial test for node extraction, hence, the displacement Uy of crack lips can be  used to separate nodes of upper and lower lips.
    step=odb.steps['Step-1']
    # Extract crack Tip coordinates and diplacement
    setname = 'POINTE-RIGHT'
    print '      #: Node Set Name=', setname
    POINTE_RIGHT = odb.rootAssembly.nodeSets[setname]
    ToAnalyseU = POINTE_RIGHT.nodes[0]
    listN_TIP_RIGHT=[]
    for v in ToAnalyseU:
        listN_TIP_RIGHT += [(v.label)] 
    CoordSubField = step.frames[-1].fieldOutputs['COORD'].getSubset(region=POINTE_RIGHT)
    xpointe = CoordSubField.values[0].data[0] 
    ypointe = CoordSubField.values[0].data[1] 
    zpointe = CoordSubField.values[0].data[2] 
    USubField = step.frames[-1].fieldOutputs['U'].getSubset(region=POINTE_RIGHT)
    Uxpointe = USubField.values[0].data[0] 
    Uypointe = USubField.values[0].data[1] 
    Uzpointe = USubField.values[0].data[2] 
    setname = 'FIELD-DISP-RIGHT'
    print '      #: Node Set Name=', setname
    FIELD_RIGHT = odb.rootAssembly.nodeSets[setname]
    CoordSubField = step.frames[-1].fieldOutputs['COORD'].getSubset(region=FIELD_RIGHT)
    USubField = step.frames[-1].fieldOutputs['U'].getSubset(region=FIELD_RIGHT)
    listN_F_RIGHT =[]
    Coorx=[]
    Coory=[]
    Coorz=[]
    Rad=[]
    Theta=[]
    listN_F_z_rad_ang=[]
    listN_F_z_x_y = []
    epsilon = 1.e-6
    for index, v in enumerate(FIELD_RIGHT.nodes[0]):
        listN_F_RIGHT += [(v.label)]  
        px = CoordSubField.values[index].data[0] - xpointe
        py = CoordSubField.values[index].data[1] - ypointe
        pz = CoordSubField.values[index].data[2] - zpointe       
        ray=sqrt((px*px)+(py*py))
        if py > epsilon :
            ang=acos(px/ray)
        elif py < -1*epsilon :
            ang=-acos(px/ray)
        elif (px > 0) :
            ang = 0
        else :
            Uy = USubField.values[index].data[1] - Uypointe    
            if Uy < 0 : 
                ang =  -acos(px/ray)
            else :
                ang = acos(px/ray)
        px_approx=round(px, 4) 
        py_approx=round(py, 4)
        pz_approx=round(pz, 4)        
        listN_F_z_x_y.append([pz_approx, px_approx, py_approx])
        ray_approx=round(ray, 4) 
        ang_approx=round(ang, 4)
        for r in listN_F_z_rad_ang:
            if abs(ray_approx - r[0]) <= 1.e-4:              # This value depends on the mesh refinement 
                ray_approx = r[0]
                break
        listN_F_z_rad_ang.append([pz_approx, ray_approx,ang_approx])
    
    listN_F_z_rad_ang_sort = sorted(listN_F_z_rad_ang)           # Sort the list [rayon,angle]
    listN_F_sorted=[]
    listN_F_z_x_y_sort=[]
    ind=0
    for triple  in listN_F_z_rad_ang_sort:
        ind = listN_F_z_rad_ang.index(triple)                  # Obtain the index of the sorted couple in the original list 
        listN_F_sorted.append(listN_F_RIGHT[ind])            # Sort the list N based on the obtained index  
        listN_F_z_x_y_sort.append(listN_F_z_x_y[ind])
    return listN_TIP_RIGHT, listN_F_RIGHT, listN_F_sorted, listN_F_z_x_y_sort, listN_F_z_rad_ang_sort


def Extract_Nodes_History_Output(odb):  
    # It's better to use pure elastic equibiaxial test for node extraction, hence, the displacement Uy of crack lips can be  used to separate nodes of upper and lower lips.
    step=odb.steps['Step-1']
    #: Extract labels of node sets
    print '   #: Extracting labels of nodes where displacement is mesured' 
    instname=(odb.rootAssembly.instances.keys())[0]
    print '      #: Instance Name=', instname
    setname=(odb.rootAssembly.nodeSets.keys())
    print '      #: Node Set Name=', setname
    setname = 'SECTION-RIGHT'
    print '      #: Node Set Name=', setname
    ToAnalyseU = odb.rootAssembly.nodeSets[setname].nodes[0]
    listN_F_RIGHT =[]
    for v in ToAnalyseU:
       listN_F_RIGHT += [(v.label)]  
    setname = 'POINTE-RIGHT'
    print '      #: Node Set Name=', setname
    ToAnalyseU = odb.rootAssembly.nodeSets[setname].nodes[0]
    listN_TIP_RIGHT=[]
    for v in ToAnalyseU:
       listN_TIP_RIGHT += [(v.label)] 
    word='Node PART-1-1.%d' % listN_TIP_RIGHT[0]
    region=step.historyRegions[word]
    dep=region.historyOutputs['COOR1'].data
    xpointe=dep[-1][1]
    dep=region.historyOutputs['COOR2'].data
    ypointe=dep[-1][1]
    dep=region.historyOutputs['COOR3'].data
    zpointe=dep[-1][1]
    dep=region.historyOutputs['U2'].data  
    Uypointe=dep[-1][1]
    Coorx=[]
    Coory=[]
    Coorz=[]
    Rad=[]
    Theta=[]
    listN_F_z_rad_ang=[]
    listN_F_z_x_y = []
    epsilon = 1.e-6
    for index in listN_F_RIGHT:
        word='Node PART-1-1.%d' % index
        region=step.historyRegions[word]
        dep=region.historyOutputs['COOR1'].data
        px=(dep[-1][1]-xpointe)
        dep=region.historyOutputs['COOR2'].data        
        py=(dep[-1][1]-ypointe)
        dep=region.historyOutputs['COOR3'].data        
        pz=(dep[-1][1]-zpointe)
        ray=sqrt((px*px)+(py*py))    
        if py > epsilon :
            ang=acos(px/ray)
        elif py < -1*epsilon :
            ang=-acos(px/ray)
        elif (px > 0) :
            ang = 0
        else :
            dep=region.historyOutputs['U2'].data
            Uy=(dep[-1][1]-Uypointe)   
            if Uy < 0 : 
                ang =  -acos(px/ray)
            else :
                ang = acos(px/ray)
        px_approx=round(px, 4) 
        py_approx=round(py, 4)
        pz_approx=round(pz, 4)        
        listN_F_z_x_y.append([pz_approx, px_approx, py_approx])
        ray_approx=round(ray, 4) 
        ang_approx=round(ang, 4)
        for r in listN_F_z_rad_ang:
            if abs(ray_approx - r[0]) <= 1.e-4:              # This value depends on the mesh refinement 
                ray_approx = r[0]
                break
        listN_F_z_rad_ang.append([pz_approx, ray_approx,ang_approx])
    listN_F_z_rad_ang_sort = sorted(listN_F_z_rad_ang)           # Sort the list [rayon,angle]
    listN_F_sorted=[]
    listN_F_z_x_y_sort=[]
    ind=0
    for triple  in listN_F_z_rad_ang_sort:
        ind = listN_F_z_rad_ang.index(triple)                  # Obtain the index of the sorted couple in the original list 
        listN_F_sorted.append(listN_F_RIGHT[ind])            # Sort the list N based on the obtained index  
        listN_F_z_x_y_sort.append(listN_F_z_x_y[ind])
    return listN_TIP_RIGHT, listN_F_RIGHT, listN_F_sorted, listN_F_z_x_y_sort, listN_F_z_rad_ang_sort

