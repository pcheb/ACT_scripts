import string,re

#Use the name of the system in case the snippet is 
#used on multiple independent systems in the project. 

###
def writelog(data,name):
	import csv
	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + name,'wb') as csvfile:
		fieldnames = ['contactname','body1','body2','contact_body_material','target_body_material','alpha_ref'];
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		writer.writeheader()
		for i in data:
			writer.writerow(i)
###

##
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
					flat_list.append(item)					# Flatten List of geomerties
				
				print item.Name
				
	flat_list = filter(lambda x:not(x.Suppressed),flat_list)
	return flat_list
##
	
contacts_folder = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.TreeGroupingFolder,True)	
contacts_folder = filter(lambda x:not(x.InternalObject.Suppressed),contacts_folder)
#contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
#contacts = filter(lambda x:not(x.SourceLocation==None),contacts);

flat_list=flatten(ExtAPI.DataModel.Project.Model.Geometry);

#
# Write out The contact list along with bodie names and contact area
#
var_model = ExtAPI.DataModel.Project.Model;
contacts = var_model.Connections.GetChildren(DataModelObjectCategory.ContactRegion,True)
contacts = filter(lambda x:not(x.InternalObject.Suppressed),contacts);
contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
contacts = filter(lambda x:not(x.SourceLocation==None),contacts);


r=0
data = [];
for i in contacts_folder:
	if i.Name =='H2G':
		for k in i.Children:
			contactbody = k.ContactBodies
			targetbody = k.TargetBodies
			print contactbody+"-"+targetbody
			#A loop to extract contact and target body material
			for child in flat_list:
				if ((contactbody)==(child.Name)):
					contact_mat=child.InternalObject.MaterialName
			
				elif ((targetbody)==(child.Name)):
					targ_mat=child.InternalObject.MaterialName	
			data.append({'contactname':k.Name,'body1':contactbody,'body2':targetbody,'contact_body_material':contact_mat,'target_body_material':targ_mat,'alpha_ref':k.InternalObject.ThermalConductance});
                               #ids= contacts[0].TargetLocation
                               #ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
                               # g=ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
                               # g.Area
	r=r+1						
writelog(data,'Contact_names_H2G.csv')





alphalist =[
[".*",".*",None],
]

r=0
data = [];
for i in contacts:
           
	contactbody = i.ContactBodies
	targetbody = i.TargetBodies
	print contactbody+"-"+targetbody
	#A loop to extract contact and target body material
	for child in flat_list:
		if ((contactbody)==(child.Name)):
			contact_mat=child.InternalObject.MaterialName
			
		elif ((targetbody)==(child.Name)):
			targ_mat=child.InternalObject.MaterialName
			
	if re.match('^H2G',i.Name)==None:
		for j in alphalist:
			if ((re.match(j[0],contactbody)!=None) & (re.match(j[1],targetbody) != None)) | ((re.match(j[1],contactbody)!=None) & (re.match(j[0],targetbody) != None)):
				data.append({'contactname':i.Name,'body1':contactbody,'body2':targetbody,'contact_body_material':contact_mat,'target_body_material':targ_mat,'alpha_ref':i.InternalObject.ThermalConductance});
                               #ids= contacts[0].TargetLocation
                               #ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
                               # g=ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
                               # g.Area
	r=r+1						
writelog(data,'Contact_names.csv')
