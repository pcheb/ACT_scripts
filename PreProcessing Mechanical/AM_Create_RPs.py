## Expected input:
##--> an input file - 'RP_Input.csv' in the solver directory
##    with 1st col: NS[header]                                  2nd col: CS[Header]          3rd Col(mandatory): RP
##					Namde Sel(already present in ANSYS Model)   Coordinate Syst (optional)   Name of the RP

## Script reads the given named selectiosn and respective CS (if given) and creates
## RemotePoints baseed on Named Selectiosn and CS. if no CS is given, 
## by default the Global CS is taken and a RP is created at the center of the selected NS

## Reads input file and processes it	
def readlog():
	import csv
	u=[]
	v=[]
	w=[]

	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\' + 'RP_Input.csv') as csvfile:
		fieldnames = ['NS','CS','RP'];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		for row in reader:
			u.append(row['NS'])
			v.append(row['CS'])
			w.append(row['RP'])

				
	return [u,v,w]
	
##
def flatten(geom):
	#model = ExtAPI.DataModel.Project.Model 
	#geom = model.Geometry                 #Get the list of Geometries 
	

	flat_list = []
	filter_list = []
#	if geom:    #Do this to check if there are any Geometries
	for sublist in geom.Children:
		for item in sublist.Children:
			if item.GetType()==Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
				flat_list = flat_list + flatten(item);
			else:
				flat_list.append(item)					# Flatten List of geomerties
			
			print item.Name
	
	for cell in flat_list:
		if cell.GetType() != Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
			filter_list.append(cell)
			
	filter_list = filter(lambda x:not(x.Suppressed),filter_list)
	return filter_list
######
	
ns_flat_list = flatten(ExtAPI.DataModel.Project.Model.NamedSelections)
##
cs_flat_list = flatten(ExtAPI.DataModel.Project.Model.CoordinateSystems)
##
rp_list= ExtAPI.DataModel.Project.Model.RemotePoints
##
input_list=readlog();  # Function Call
##
alphalist = zip(input_list[0],input_list[1],input_list[2]);

with Transaction():
    for row in alphalist:
        for nsel in ns_flat_list:                                     ## Loop to select surfaces from NS for RP
            flag = 1
            if (row[0] == nsel.Name):
                for r_point in rp_list.Children:
                    if r_point.Name ==row[2]:
                        flag=0
                        break
                if flag ==0:
                    continue
                rp = ExtAPI.DataModel.Project.Model.AddRemotePoint()
                rp.Name = row[2]                    ## When name the same as NS:-->  nsel.Name
                rp.PilotNodeAPDLName= row[2]
                rp.InternalObject.GeometryDefineBy = 1
                rp.InternalObject.ComponentSelection = nsel.ObjectId
                for csys in cs_flat_list: 	                           ## Loop defines correct CS for RP
                    if (row[1] == csys.Name):
                        rp.InternalObject.CoordinateSystemSelection=csys.ObjectId
                        rp.InternalObject.LocationX=0
                        rp.InternalObject.LocationY=0
                        rp.InternalObject.LocationZ=0
ExtAPI.DataModel.Tree.Refresh()