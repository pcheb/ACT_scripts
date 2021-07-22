import csv
def writelog(data):
                cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
		with open(cdir + '\\'+ 'RP_Info.csv','wb') as csvfile:
			fieldnames = ['RP_Name','Coordinate_System','X_Coordinate','Y_Coordinate','Z_Coordinate'];
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
			writer.writeheader()
			for i in data:
				writer.writerow(i)


rp_list= ExtAPI.DataModel.Project.Model.RemotePoints
data=[]
with Transaction():
    for rp in rp_list.Children:
        data.append({'RP_Name':rp.Name,'Coordinate_System':rp.CoordinateSystem.Name,'X_Coordinate':rp.InternalObject.LocationX,'Y_Coordinate':rp.InternalObject.LocationY,'Z_Coordinate':rp.InternalObject.LocationZ});
ExtAPI.DataModel.Tree.Refresh()      
writelog(data)