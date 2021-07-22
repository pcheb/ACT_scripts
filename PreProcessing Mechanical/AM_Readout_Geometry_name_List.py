import string,re

def flatten(geom):
	#model = ExtAPI.DataModel.Project.Model 
	#geom = model.Geometry                 #Get the list of Geometries 
	

	flat_list = []
	filter_list = []
	if geom:    #Do this to check if there are any Geometries
		for sublist in geom.Children:
			for item in sublist.Children:
				if item.GetType()==Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
					flat_list = flat_list + flatten(item);
				else:
					flat_list.append(item)					# Flatten List of geomerties
				
				print item.Name
				
	for cell in flat_list:
		if cell.GetType()==flat_list[0].GetType():
			filter_list.append(cell)
			
	filter_list = filter(lambda x:not(x.Suppressed),filter_list)
	return filter_list
	
	
#The script writes out a list of all UNSUPPRESSED 
# bodies in the project to a .csv file 
 
flat_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)

cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
f=open(cdir + "\\"+ "Geometry_Readout.csv", "w")    # Location of a new file
##f=open("C:\\LIT_ETMO_THERMAL_UTILITIES\\Thermal Model Input + Info\\b1007\\Materials + documentation\\Geometry_Readout.csv", "w")    # Location of a new file

for i in flat_list:
	if (i.Suppressed == False):					# Filter out suppressed bodies
		print i.Name
		f.write('%s,%s\n'%(i.Name,i.InternalObject.MaterialName))					# Write body object to excel file
		
f.close()