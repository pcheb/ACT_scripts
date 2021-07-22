## Prerequisite: 
## --> Excel Sheet with name of body and material name(matches charecters to ANSYS Material DB)

## Script reads the material assignment excel sheet and 
## assigns the respective materials to the list of bodies listed in Excel
import string,re

#Use the name of the system in case the snippet is 
#used on multiple independent systems in the project. 
 

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
			if cell.GetType() == flat_list[0].GetType():
				filter_list.append(cell)
				
	filter_list = filter(lambda x:not(x.Suppressed),filter_list)
	return filter_list
	
flat_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
			
# Regexps for Body1 and Body2 (Body1-Body2 and Body2-Body1 are matched ) and associated thermal resistance
alphalist =[
[".*",".*","Aluminum 5083"],
]

##
import csv
def readlog():
	u=[]
	v=[]
	
	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\'+ 'material_list_assignment.csv') as csvfile:
		fieldnames = ['name','material'];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		c=0
		for row in reader:
			c = c+1
			u.append(row['name'])
			v.append(row['material'])
			
				
	return [u,v]
##

mat_list = readlog()

# chaneg names
alphalist = zip(mat_list[0],mat_list[1]);
#
print alphalist
#c=0
#flag=1
for i in flat_list:
    for j in alphalist:
                if (i.Name == j[0]):
                        if j[1]!=None:
							i.InternalObject.MaterialName = j[1]
							print i.InternalObject.MaterialName
							#c=c+1
							#if c>20:
							#	flag =0
							#	break
	#if flag ==0:
	#	break