## The script reads out the unsuppressed contacts along with target and source body names, 
## their respective contact and target face IDs and writes them out into a .csv file in the wrking directory

def contact_info_func(contacts):
## Extracts the contact and target face IDs along with Contact names as Arrays a
## Input required: contacts from ANSYS

	cont_name=[]
	cont_id=[]
	targ_id=[]
#	i=0				# Loop counter for debugging
	ns_c = ExtAPI.DataModel.Project.Model.AddNamedSelection()
	ns_t = ExtAPI.DataModel.Project.Model.AddNamedSelection()
	with Transaction():
		for ii in contacts:
			
			print ii.Name
#			ns_c.Location = ii.SourceLocation
#			ns_t.Location = ii.TargetLocation
			
			cont_id.append(ii.SourceLocation.Ids)
			targ_id.append(ii.TargetLocation.Ids)
			cont_name.append(ii.Name)
			
			#print area[i]  ## For debugging
#			i = i+1			# Loop condition for testing and debugging
#			if i >5:
#				break

#			new_ns_1.Delete()														# Delete the created named selections --> Takes additional time
#			new_ns_2.Delete()
	ExtAPI.DataModel.Tree.Refresh()
	return [cont_name, cont_id, targ_id]

import csv
def writelog(data):						## Function to write out data into a csv file
        cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
		with open(cdir +'\\'+ 'Contact_names.csv','wb') as csvfile:
			fieldnames = ['contactname','body1','body2','contact_body_IDs','target_body_IDs'];
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
			writer.writeheader()
			for i in data:
				writer.writerow(i)



##def writeb2b(data):
##                cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
##		with open(cdir + '\\'+ 'b2b.csv','wb') as csvfile:
##			fieldnames = ['b1','b1a','b2','b2a'];
##			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect = csv.excel)
##			writer.writeheader()
##			for i in data:
##				writer.writerow({'b1':i[0],'b1a':i[1],'b2':i[2],'b2a':i[3]})
##


def flatten(geom):					## Function to flatten a geometry strcuture with multiple levels of folders within the geometry tree strcuture
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

#########################################################################################################
#
# Write out The contact list along with bodie names and contact area
#
import re
var_model = ExtAPI.DataModel.Project.Model;
contacts = var_model.Connections.GetChildren(DataModelObjectCategory.ContactRegion,True)
contacts = filter(lambda x:not(x.InternalObject.Suppressed),contacts);
contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
contacts = filter(lambda x:not(x.SourceLocation==None),contacts);
contact_info = contact_info_func(contacts)
flat_list=flatten(ExtAPI.DataModel.Project.Model.Geometry)


## Loop to make sure that the assigned contact area column is complete
if (len(contact_info)!=len(contacts)):
	c=len(contact_info)
	while (c<len(contacts)):
		contact_info.append(None)
		c=c+1
## Used to reoragnise data for file data manipulation
alphalist =[
[".*",".*",None,contact_info[0],contact_info[1],contact_info[2]],
]

#alphalist = zip(contact_info);

#alphalist=[contact_info[0],contact_info[1],contact_info[2]]


###########################################################################################################

#r=0 				## Counter for testing and debuggign
data = [];
for i in contacts:
           
	contactbody = i.ContactBodies
	targetbody = i.TargetBodies
	print contactbody+"-"+targetbody
			
	if re.match('^H2G',i.Name)==None:
			for j in alphalist:
						if ((re.match(j[0],contactbody)!=None) & (re.match(j[1],targetbody) != None)) | ((re.match(j[1],contactbody)!=None) & (re.match(j[0],targetbody) != None)):
							for l in range(0,len(j[4])):
								for m in range(0,len(j[4][l])):
									data.append({'contactname':i.Name,'body1':contactbody,'body2':targetbody,'contact_body_IDs':j[4][l][m],'target_body_IDs':"--"});
								for n in range(0,len(j[5][l])):
									data.append({'contactname':i.Name,'body1':contactbody,'body2':targetbody,'contact_body_IDs':"--",'target_body_IDs':j[5][l][n]});
							#ids= contacts[0].TargetLocation
							#ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
							# g=ExtAPI.DataModel.GeoData.GeoEntityById(ids.Ids[0])
							# g.Area
#	r=r+1						
writelog(data)   	## Function call to write out data into csv file




