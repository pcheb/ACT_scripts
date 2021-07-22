ExportFile = r'E:\akarabey\POB4000\20 Lastenheft\MechModelExport_4000_D005_M5_v2.csv'                      # Path to exported file

import csv
import logging
import os.path
import time

def ExportGeo():

    f = open(ExportFile, 'wb')
    csvwriter = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    
    flag = False
    scalef = 1
    materials = {}
    
    with Transaction():
        for itm in ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Body):
            logger.info("Body name: " + itm.Name)
            ibody=itm.GetGeoBody()

            #Calculate factor for unit conversion)
            if not flag:
                if ibody.Volume > 0:
                    scalef = (itm.Volume.GetConvertedValue('mm mm mm') / ibody.Volume)**(1.0/3.0)
                    flag = True
            isize = getSize(ibody,scalef)
            sCentroid = getCentroid(ibody,scalef)
            csvwriter.writerow(["Body",ibody.Id,ibody.Name,isize,ibody.Suppressed] + sCentroid)
            
            for iface in ibody.Faces:
                try:
                    temp = list(iface.Centroid)
                    sCentroid = [temp[0] * scalef, temp[1] * scalef, temp[2] * scalef]
                    csvwriter.writerow(["Face",iface.Id,ibody.Id,iface.Area * (scalef ** 2)] + sCentroid)
                except:
                    logger.info("Failed face in:" + itm.Name)
            for iedge in ibody.Edges:
                try:
                    temp = list(iedge.Centroid)
                    sCentroid = [temp[0] * scalef, temp[1] * scalef, temp[2] * scalef]
                    csvwriter.writerow(["Edge",iedge.Id,ibody.Id,iedge.Length * scalef] + sCentroid)
                except:
                    logger.info("Failed edge in:" + itm.Name)
            for ivert in ibody.Vertices:
                try:
                    csvwriter.writerow(["Vertex",ivert.Id,ibody.Id,0] + [ivert.X * scalef , ivert.Y * scalef, ivert.Z * scalef])
                except:
                    logger.info("Failed vertex in:" + itm.Name)

            try:
                materials[itm.Material].append(ibody.Id)
            except:
                materials[itm.Material] = [ibody.Id]

        print("Exporting Named Selections")

        names={}
        for itm in ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.NamedSelection):
            try:
                if not itm.Suppressed:
                    if itm.Name in names.keys():
                        names[itm.Name]=names[itm.Name]+1
                        itm.Name=itm.Name +"_"+ str(names[itm.Name])
                    else: 
                        names[itm.Name]=1
                        
                    if itm.InternalObject.ScopeBasedType == 0: #and itm.InternalObject.ScopedType in [1,2,5,4]:
                        NSlist = []
                        for i in itm.Location:
                            NSlist.append(i)
                        csvwriter.writerow(["NamedSelection",int(itm.ObjectId),itm.Name] + NSlist)
            except:
                logger.info("Failed Named Selection:" + itm.Name)
        print("Exporting Materials")
        
        for itm in ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Material):
            try:
                if itm.Name in materials:
                    csvwriter.writerow(["Material",int(itm.ObjectId),itm.Name] + materials[itm.Name])
            except:
                logger.info("Failed Material:" + itm.Name)        
        print("Exporting Joints")

        names={}
        for itm in ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Joint):
            try:
                if itm.Name in names.keys():
                    names[itm.Name]=names[itm.Name]+1
                    itm.Name=itm.Name +"_"+ str(names[itm.Name])
                else: 
                    names[itm.Name]=1
                    
                origin = itm.ReferenceCoordinateSystem.OriginLocation
                axis = itm.ReferenceCoordinateSystem.PrimaryAxisLocation
                axis2 = itm.ReferenceCoordinateSystem.SecondaryAxisLocation
                
                iorigin = []
                iaxis = []
                jaxis = []
                try:
                    for i in origin:
                        iorigin.append(i)
                except:
                    pass
                try:
                    for i in axis:
                        iaxis.append(i)
                except:
                    pass
                try:
                    for i in axis2:
                        jaxis.append(i)
                except:
                    pass
                csvwriter.writerow(["Joint",int(itm.ObjectId),itm.Name,"Origin"] + iorigin)
                csvwriter.writerow(["Joint",int(itm.ObjectId),itm.Name,"PrimaryAxis"] + iaxis)
                csvwriter.writerow(["Joint",int(itm.ObjectId),itm.Name,"SecondaryAxis"] + jaxis)
            except:
                logger.info("Failed Joint:" + itm.Name)
        print("Exporting Contact Regions")

        names={}
        for itm in ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.ContactRegion):
            try:
                if itm.Name in names.keys():
                    names[itm.Name]=names[itm.Name]+1
                    itm.Name=itm.Name +"_"+ str(names[itm.Name])
                else: 
                    names[itm.Name]=1

                if itm.InternalObject.GeometryDefineBy == 0: #Geometry selection
                    source = itm.SourceLocation
                    target = itm.TargetLocation
                else: #Named selection
                    source = itm.SourceLocation.Location
                    target = itm.TargetLocation.Location

                
                isource = []
                itarget = []
                try:
                    for i in source:
                        isource.append(i)
                except:
                    pass
                try:
                    for i in target:
                        itarget.append(i)
                except:
                    pass

                csvwriter.writerow(["ContactRegion",int(itm.ObjectId),itm.Name,itm.Suppressed,itm.InternalObject.ThermalConductance,"Source"] + isource)
                csvwriter.writerow(["ContactRegion",int(itm.ObjectId),itm.Name,itm.Suppressed,itm.InternalObject.ThermalConductance,"Target"] + itarget)
            except:
                logger.info("Failed Contact Region:" + itm.Name)

        print("Exporting Mesh Control")

        for itm in ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.MeshControl):
            try:
                if itm.InternalObject.GeometryDefineBy == 0:
                    NSlist = []
                    for i in itm.Location:
                        NSlist.append(i)
                    csvwriter.writerow(["MeshControl",int(itm.ObjectId),itm.Name] + NSlist)
            except:
                logger.info("Failed Mesh Control:" + itm.Name)
        
    f.close()

def getSize(ibody,scalef):
    if str(ibody.BodyType) == "GeoBodySolid":
        isize = ibody.Volume * scalef**3
    elif str(ibody.BodyType) == "GeoBodySheet":
        isize = ibody.Area * scalef**2
    elif str(ibody.BodyType) == "GeoBodyWire":
        isize = ibody.Length * scalef
    else:
        isize = 0
        print ibody.BodyType
    return isize
    
def getCentroid(ibody,scalef):
    
    if str(ibody.BodyType) == "GeoBodyWire":
        icent = [0, 0, 0]
        tlen = 0
        for iedge in ibody.Edges:
            temp = list(iedge.Centroid)
            ilen = iedge.Length
            tlen += ilen
            icent = [icent[0]+temp[0]*ilen, icent[1]+temp[1]*ilen, icent[2]+temp[2]*ilen]
            
        icent = [icent[0]*scalef/tlen, icent[1]*scalef/tlen, icent[2]*scalef/tlen]
    else:
        temp = list(ibody.Centroid)
        icent = [temp[0] * scalef, temp[1] * scalef, temp[2] * scalef]
    return icent
    
def init_log(logger):
    if logger.handlers:
        logger.handlers[0].close()
        logger.handlers = []
    
    #logHandler = logging.FileHandler("status.log", mode='w')
    logHandler = logging.FileHandler(logFile, mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler) 
    logger.setLevel(logging.INFO)

def close_log(logger):
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)

logFile = os.path.join(os.path.dirname(ExportFile),'status.log')
logger = logging.getLogger('StatusLog')
init_log(logger)

logger.info("Process Started!")

ExportGeo()

logger.info("Process Finished!")
close_log(logger)
