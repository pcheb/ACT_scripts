## Prerequisite: 
## --> .csv file with the name "htc_list_assignment.csv" containing following field:
##  contactname','body1','body2','contact_body_material','target_body_material','area_final','contact_body_area','target_body_area','contact_body_faces','target_body_faces','alpha_ref','htc' 
## Script reads the material assignment excel sheet and 
## assigns the respective materials to the list of bodies listed in Excel
import string,re

#Use the name of the system in case the snippet is 
#used on multiple independent systems in the project. 
 
	
contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.ContactRegion,True)	
contacts = filter(lambda x:not(x.InternalObject.Suppressed),contacts)
contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
contacts = filter(lambda x:not(x.SourceLocation==None),contacts);



##
import csv
def readlog():
	u=[]
	v=[]
	w=[]
	a=[]
	b=[]
	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\'+ 'htc_list_assignment.csv') as csvfile:
		fieldnames = ['contactname','body1','body2','contact_body_material','target_body_material','area_final','contact_body_area','target_body_area','contact_body_faces','target_body_faces','alpha_ref','htc'];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		for row in reader:
			u.append(row['contactname'])
			v.append(row['alpha_ref'])
			w.append(row['htc'])
			a.append(row['area_final'])
			#b.append(row['target_body_area'])
		
		unit =' [W m^-1 m^-1 C^-1]'
		w_new = [x + unit for x in w]
				
	return [u,v,w_new,a]
###
##def read_ref_log():
##	a=[]
##	b=[]
##	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
##	with open(cdir + '\\'+ 'Contact_names.csv') as csvfile:
##		fieldnames = ['contactname','body1','body2','contact_body_material','target_body_material','area_final','contact_body_area','target_body_area','contact_body_faces','target_body_faces','alpha_ref'];
##		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
##		#reader.readheader()
##		for row in reader:
##			a.append(row['contact_body_area'])
##			b.append(row['target_body_area'])
##
##				
##	return [a,b]
###
contact_info = readlog()
#
##ref_info = read_ref_log()
#
alphalist= zip(contact_info[0],contact_info[1],contact_info[2],contact_info[3]);


print alphalist

flag= 1
r=1
with Transaction():
	for i in contacts:
	
		for j in alphalist:
			if (i.Name == j[0] and contact_info[3][r] == j[3]):
	#			if (j[1] !=0):
				i.ThermalConductanceValue = Quantity(j[2])
				print i.Name
				#print i.ThermalConductanceValue
				print j[2]
				print "**"
	
				break
	#			else: 
	#				i.AutomaticThermalConductance = True
		r=r+1
ExtAPI.DataModel.Tree.Refresh()