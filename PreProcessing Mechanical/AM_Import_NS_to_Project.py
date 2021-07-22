##
import csv
import re

## Reads input file and processes it	
def readlog():
	import csv
	u=[]
	v=[]
	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\' + 'NS_FaceID.csv') as csvfile:
		fieldnames = ['NS','Face_ID'];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		for row in reader:
			u.append(row['NS'])
			v.append(row['Face_ID'])
	return [u,v]
##


my_sel=ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
my_sel.Ids=[565048]


input_list = readlog()
a=[input_list[1][1]]

with Transaction():
	for j in range(1,(len(input_list[0]))-1):
		if input_list[0][j]==input_list[0][j+1]:
			a.append(input_list[1][j+1])
			if j==(len(input_list[0]))-2:
				print "YES"
				a=[int(i) for i in a];
				my_sel.Ids=a
				ExtAPI.SelectionManager.NewSelection(my_sel)
				new_ns=ExtAPI.DataModel.Project.Model.AddNamedSelection()
				new_ns.Name=input_list[0][j]
				a=[input_list[1][j+1]]
		else:
			a=[int(i) for i in a];
			my_sel.Ids=a
			ExtAPI.SelectionManager.NewSelection(my_sel)
			new_ns=ExtAPI.DataModel.Project.Model.AddNamedSelection()
			new_ns.Name=input_list[0][j]
			a=[input_list[1][j+1]]
			
			if j==len(input_list[0])-2:
				a=[int(i) for i in a];
				my_sel.Ids=a
				ExtAPI.SelectionManager.NewSelection(my_sel)
				new_ns=ExtAPI.DataModel.Project.Model.AddNamedSelection()
				new_ns.Name=input_list[0][j+1]
ExtAPI.DataModel.Tree.Refresh()