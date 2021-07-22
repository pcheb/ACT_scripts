##Pre-requisit: --> Run the flatten function before in ANSYS
##				-->	Set the 1st Line Body to the correct Model Type


def flatten(geom):
	#model = ExtAPI.DataModel.Project.Model 
	#geom = model.Geometry                 #Get the list of Geometries 
	

	flat_list = []
	
	if geom:    #Do this to check if there are any Geometries
		for sublist in geom.Children:
			for item in sublist.Children:
				if item.GetType()==Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
					flat_list = flat_list + flatten(item);
				else:
					if (item.GetType()==Ansys.ACT.Automation.Mechanical.Body):
						flat_list.append(item)					# Flatten List of geomerties
				
				#print item.Name

	flat_list = filter(lambda x:not(x.Suppressed),flat_list)
	return flat_list

	
flat_list=flatten(ExtAPI.DataModel.Project.Model.Geometry)
new_list=[]
b = flat_list[0].CrossSectionArea

with Transaction():
	for i in flat_list:
		if (i.GetType() == Ansys.ACT.Automation.Mechanical.Body):
			if (i.CrossSectionArea != b ):
				i.InternalObject.MaterialName = "Water Liquid"
				print i.Name
				new_list.append(i)
	
	a = new_list[0].ModelType
	
	for i in new_list:
		i.ModelType = a
		print i.Name

ExtAPI.DataModel.Tree.Refresh()