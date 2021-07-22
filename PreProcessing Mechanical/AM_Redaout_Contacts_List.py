## The script readsout the unsuppressed contacts along with target and source body names, 
## their respective material assignment and the minimum suface area of contact.
#def reportoncontact(contact):
#		sourcearea  = [ExtAPI.DataModel.GeoData.GeoEntityById(k).Area for k in contact.SourceLocation.Ids];
#		targetarea  = [ExtAPI.DataModel.GeoData.GeoEntityById(k).Area for k in contact.TargetLocation.Ids];
#		print contact.SourceLocation.Ids,contact.TargetLocation.Ids;
#		print sourcearea,targetarea;
#		print sum(sourcearea),sum(targetarea);
#   return {'source':{'area':sourcearea,'ids':contact.SourceLocation.Ids},'target':{'area':targetarea,'ids':contact.TargetLocation.Ids}}

def contact_area(contacts):
## Extracts the minimum area of contact from Source and Target Bodies 
## by creating and comparing the area of the named selections at the target 
## and contact faces. Returns the area for each contact as a list
	area=[]
	cont_area=[]
	targ_area=[]
	cont_faces=[]
	targ_faces=[]
	i=0
	with Transaction():
		for ii in contacts:
			
			print ii.Name
			
			#ExtAPI.SelectionManager.NewSelection(ii.TargetLocation)					# Select target faces 
			#new_ns_1 = ExtAPI.DataModel.Project.Model.AddNamedSelection()
			#print new_ns_1.Name
			#target_area = new_ns_1.InternalObject.AreaOfScopedFaces
			#target_face = new_ns_1.InternalObject.NumInSelection
            
			t_face  = [ExtAPI.DataModel.GeoData.GeoEntityById(k).Area for k in ii.TargetLocation.Ids]; ## More effiecent for area and no. of faces
			target_area = str(sum(t_face))
			target_face = len(t_face)
			print target_area														# Area of target faces
			print target_face
			
			#ExtAPI.SelectionManager.NewSelection(ii.SourceLocation)					# Select contact faces 
			#new_ns_2 = ExtAPI.DataModel.Project.Model.AddNamedSelection()
			#print new_ns_2.Name  
            #contact_area = new_ns_2.InternalObject.AreaOfScopedFaces
			#contact_face = new_ns_2.InternalObject.NumInSelection
            
			s_face  = [ExtAPI.DataModel.GeoData.GeoEntityById(k).Area for k in ii.SourceLocation.Ids]; # More effiecent for area and no. of faces
			contact_area = str(sum(s_face))
			contact_face = len(s_face)
		
			print contact_area                                     					# Area of contact faces
			print contact_face
			
			cont_area.append(contact_area)
			targ_area.append(target_area)
			area.append((min(target_area,contact_area)))
			cont_faces.append(contact_face)
			targ_faces.append(target_face)
			
			print area[i]
			i = i+1
	
#			new_ns_1.Delete()														# Delete the created named selections
#			new_ns_2.Delete()
	ExtAPI.DataModel.Tree.Refresh()
	return [area, cont_area, targ_area, cont_faces, targ_faces]

import csv

def writelog(data):
		cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
		with open(cdir + '\\'+ 'Contact_names.csv','wb') as csvfile:
			fieldnames = ['contactname','body1','body2','contact_body_material','target_body_material','area_final','contact_body_area','target_body_area','contact_body_faces','target_body_faces','alpha_ref'];
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
			writer.writeheader()
			for i in data:
				writer.writerow(i)



##def writeb2b(data):
##		cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
##		with open(cdir + '\\'+ 'b2b.csv','wb') as csvfile:
##			fieldnames = ['b1','b1a','b2','b2a'];
##			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
##			writer.writeheader()
##			for i in data:
##				writer.writerow({'b1':i[0],'b1a':i[1],'b2':i[2],'b2a':i[3]})
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


#
# Write out The contact list along with bodie names and contact area
#
import re
var_model = ExtAPI.DataModel.Project.Model;
contacts = var_model.Connections.GetChildren(DataModelObjectCategory.ContactRegion,True)
contacts = filter(lambda x:not(x.InternalObject.Suppressed),contacts);
contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
contacts = filter(lambda x:not(x.SourceLocation==None),contacts);
contact_info = contact_area(contacts)
flat_list=flatten(ExtAPI.DataModel.Project.Model.Geometry)
## Loop to make sure that the assigned contact area column is complete
if (len(contact_info)!=len(contacts)):
	c=len(contact_info)
	while (c<len(contacts)):
		contact_info.append(None)
		c=c+1

alphalist =[
[".*",".*",None,contact_info[0],contact_info[1],contact_info[2],contact_info[3],contact_info[4]],
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
							data.append({'contactname':i.Name,'body1':contactbody,'body2':targetbody,'contact_body_material':contact_mat,'target_body_material':targ_mat,'area_final':j[3][r],'contact_body_area':j[4][r],'target_body_area':j[5][r],'contact_body_faces':j[6][r],'target_body_faces':j[7][r],'alpha_ref':i.InternalObject.ThermalConductance});
                               #ids= contacts[0].TargetLocation
                               #ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
                               # g=ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
                               # g.Area
	r=r+1						
writelog(data)




