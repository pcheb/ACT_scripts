##
def writelog(data):
		import csv
                cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
		with open(cdir + '\\'+ 'NS_Input.csv','wb') as csvfile:
			fieldnames = ['NS',];
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
			writer.writeheader()
			for i in data:
				writer.writerow(i)
##



var_model = ExtAPI.DataModel.Project.Model;
ns = ExtAPI.DataModel.Project.Model.NamedSelections.GetChildren(DataModelObjectCategory.TreeGroupingFolder,True)
row=[]
with Transaction():	
	for n in ns:
		if n.Name =='Postprocessing':
			for j in n.Children:
				if str(j.GetType())=='Ansys.ACT.Automation.Mechanical.TreeGroupingFolder' and j.Name == 'SFr sensitivity areas':
					for k in j.Children:
						row.append(k.Name)

ExtAPI.DataModel.Tree.Refresh()

for i in range(0,len(row)):
	data.append({'NS':row[i]});

		
writelog(data)