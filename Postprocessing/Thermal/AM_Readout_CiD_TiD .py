## This script reads out CID and TID of contacts for specific Named Selectiosn (have to be surface Named Selections)
## Based on Contact IDs for C007 (tested based on T001_v94 version ANSYS) for specific Named Slections 
## Input Prerequisite: .csv File named "NS_Input" in the solver directory, with a list of named seletion names  !(surface Named Selctiosn ONLY)! matching the ANSYS Project.
## Example of Input fiel:

## NS
## <Name of NS_1>
## <Name of NS_2>
## eof

## Output Generated: CSV file ("NS_CiD_TiD.csv") with NS, CID, TID

####

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
		with open(cdir + '\\'+ 'NS_CiD_TiD.csv','wb') as csvfile:
			fieldnames = ['Named_Selection','CID','TID'];
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
			writer.writeheader()
			for i in data:
				writer.writerow(i)
##

#####

####################################################################

var_model = ExtAPI.DataModel.Project.Model;
contacts = var_model.Connections.GetChildren(DataModelObjectCategory.ContactRegion,True)
contacts = filter(lambda x:not(x.InternalObject.Suppressed),contacts);
contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
contacts = filter(lambda x:not(x.SourceLocation==None),contacts);

ns = ExtAPI.DataModel.Project.Model.NamedSelections
	
input_list=readlog();  # Function Call
alphalist = zip(input_list[0]);

ns_filtered=[]
for nsel in ns.Children:
	for row in alphalist:
		if nsel.Name ==row[0]:
			ns_filtered.append(nsel)
			
row=[]
register=[]
data = [];
c=0

for r in ns_filtered:
	faces=r.Ids
	row =[]
	for id in faces:
		for i in contacts:
			flag = 1
			if i.Children[0].Name in row:
				continue
				
			for j in i.TargetLocation.Ids:
				if id == j : 
					print c
					c=c+1
					print r.Name
					print i.Name
					print i.Children[0].Name
					row.append(i.Children[0].Name)	
					flag=0
					break
					
			if flag == 0:
#				register.append(row)
				continue
		
			for j in i.SourceLocation.Ids:
				if id ==j :	
					print c
					c=c+1
					print r.Name
					print i.Name
					print i.Children[0].Name
					row.append(i.Children[0].Name)
					flag=0
					break
	register.append(row)
	
	
for a in range(0,len(register)):
	for b in range(0,len(register[a])):
		data.append({'Named_Selection':ns_filtered[a].Name,'CID':'C'+register[a][b][-6:],'TID':'T'+register[a][b][-6:]});

writelog(data)		

####################################################################		