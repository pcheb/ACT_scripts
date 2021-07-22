nsFile = r'E:\akarabey\POB4000_v2\20 Lastenheft\ModelCompare_v3.csv'                      # Path to output file of 2nd step
import csv

def ImportNSelect():
    f = open(nsFile, 'rb')
    csvreader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    model = ExtAPI.DataModel.Project.Model
    
    NSlist = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.NamedSelection)
    Jointlist = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Joint)
    MClist = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.MeshControl)
    Bodylist = ExtAPI.DataModel.GetObjectsByType(DataModelObjectCategory.Body)
    MatDict = {}
    
    
    with Transaction():
        for row in csvreader:
            
            if row[0] == "NamedSelection":
                NSname = row[1]
                NSentities = row[2:]
                    
                for iNS in NSlist:
                    if iNS.Name == NSname:
                        Sel = AddSelection(NSentities)
                        try:
                            iNS.Location = Sel
                        except:
                            print(iNS.Name, NSentities)
                        break
                    
            elif row[0] == "Material":
                for i in row[2:]:
                    MatDict[i] = row[1]
                    
            elif row[0] == "Joint":
                Jointname = row[1]
                component = row[2]
                NSentities = row[3:]
                for iNS in Jointlist:
                    if iNS.Name == Jointname:
                        Sel = AddSelection(NSentities)
                        try:
                            if component == "Origin":
                                iNS.ReferenceCoordinateSystem.OriginLocation = Sel
                            elif component == "PrimaryAxis":
                                iNS.ReferenceCoordinateSystem.PrimaryAxisLocation = Sel
                            else:
                                iNS.ReferenceCoordinateSystem.SecondaryAxisLocation = Sel
                        except:
                            print(iNS.Name, NSentities)
                        break
                        
            elif row[0] == "MeshControl":
                MCname = row[1]
                MCentities = row[2:]
                for iNS in MClist:
                    if iNS.Name == MCname:
                        Sel = AddSelection(MCentities)
                        try:
                            iNS.Location = Sel
                        except:
                            print(iNS.Name, MCentities)
                        break

        for ibody in Bodylist:
            try:
                ibody.Material = MatDict[ibody.GetGeoBody().Id]
            except:
                pass
                #rint(ibody.Name + " not found")


def AddSelection(plist):
    SlMn = ExtAPI.SelectionManager
    SlMn.ClearSelection()
    Sel = SlMn.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    Sel.Ids = plist
    return Sel

ImportNSelect()