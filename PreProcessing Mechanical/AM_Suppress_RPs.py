## Expected input:
##--> an input file - 'RP_Input.csv' in the solver directory
##    with 1st col: NS[header]                                  2nd col: CS[Header]          3rd Col(mandatory): RP
##					Namde Sel(already present in ANSYS Model)   Coordinate Syst (optional)   Name of the RP

## Script reads the given named selectiosn and respective CS (if given) and creates
## RemotePoints baseed on Named Selectiosn and CS. if no CS is given, 
## by default the Global CS is taken and a RP is created at the center of the selected NS

## Reads input file and processes it	

import re

## Reads input file and processes it	
def readlog():
	import csv
	u=[]
	v=[]
	w=[]

	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\' + 'RP_Suppress_List.csv') as csvfile:
		fieldnames = ['RP'];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		for row in reader:
			w.append(row['RP'])
	
	return [w]
	
input_list=readlog();  # Function Call
##
alphalist = zip(input_list[0]);

rp_list= ExtAPI.DataModel.Project.Model.RemotePoints
with Transaction():
	for row in alphalist:
		for r_point in rp_list.Children:
			if row[0] == r_point.Name:
				r_point.InternalObject.Suppressed = 1
ExtAPI.DataModel.Tree.Refresh()