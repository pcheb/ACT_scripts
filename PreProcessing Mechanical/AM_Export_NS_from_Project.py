##
import csv
import re

## Reads input file and processes it	
def readlog():
	import csv
	u=[]

	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\' + 'NS_Input.csv') as csvfile:
		fieldnames = ['NS'];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		for row in reader:
			u.append(row['NS'])

	return [u]
	
##

##
def writelog(data):
                cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
		with open(cdir + '\\'+ 'NS_FaceID.csv','wb') as csvfile:
			fieldnames = ['Named_Selection','Face_ID'];
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
			writer.writeheader()
			for i in data:
				writer.writerow(i)
##

##
def flatten(geom):
	#model = ExtAPI.DataModel.Project.Model 
	#geom = model.Geometry                 #Get the list of Geometries 
	

	flat_list = []
	filter_list = []
#	if geom:    #Do this to check if there are any Geometries
	for sublist in geom.Children:
		if sublist.GetType()==Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
			for item in sublist.Children:
				flat_list = flat_list + flatten(item);
		else:
			flat_list.append(sublist)					# Flatten List of geomerties
			
		print sublist.Name
	
#	for cell in flat_list:
#		if cell.GetType() != Ansys.ACT.Automation.Mechanical.TreeGroupingFolder:
#			filter_list.append(cell)
			
#	filter_list = filter(lambda x:not(x.Suppressed),filter_list)
	return flat_list
##


####################################################################

nsel=ExtAPI.DataModel.Project.Model.NamedSelections
ns_list=flatten(nsel)
#ns= "IC_TOP_PX_In_Power"  # Parameter to search for the NS Name

a=[]
faces=[]
data =[]
input_list=readlog();  # Function Call
alphalist = zip(input_list[0]);
nsel_filtered=[]


for ns in nsel.Children:
	for row in alphalist:
		if ns.Name ==row[0]:
			nsel_filtered.append(ns)
			a.append(ns.Ids)


for row in alphalist:
	for ns in nsel.Children:
		if ns.Name ==row[0]:
			#a=ns.Ids
			faces.append(ns.Ids)
		

#for r in ns_filtered:
#	faces=r.Ids
for c in range(0,len(nsel_filtered)):
	for d in range(0,len(faces[c])):
		data.append({'Named_Selection':nsel_filtered[c].Name,'Face_ID':str(faces[c][d])});

writelog(data)

