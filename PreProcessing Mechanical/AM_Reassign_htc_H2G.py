## Prerequisite: 
## --> Excel Sheet with name of body and material name(matches charecters to ANSYS Material DB)

## Script reads the material assignment excel sheet and 
## assigns the respective materials to the list of bodies listed in Excel
import string,re

#Use the name of the system in case the snippet is 
#used on multiple independent systems in the project. 
import csv
def readlog():
	u=[]
	v=[]
	w=[]
	a=[]
	b=[]
	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\'+ 'H2G_htc_list_assignment.csv') as csvfile:
		fieldnames = ['contactname','body1','body2','contact_body_material','target_body_material','alpha_ref','htc'];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		for row in reader:
			u.append(row['contactname'])
			v.append(row['alpha_ref'])
			w.append(row['htc'])
			#a.append(row['area_final'])
			#b.append(row['target_body_area'])
		
		unit =' [W m^-1 m^-1 C^-1]'
		w_new = [x + unit for x in w]
				
	return [u,v,w_new]
	
contacts_folder = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.TreeGroupingFolder,True)	
contacts_folder = filter(lambda x:not(x.InternalObject.Suppressed),contacts_folder)
#contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
#contacts = filter(lambda x:not(x.SourceLocation==None),contacts);

contact_info = readlog()
#
##ref_info = read_ref_log()
#
alphalist= zip(contact_info[0],contact_info[1],contact_info[2]);


with Transaction():
	for i in contacts_folder:
		if i.Name =='H2G':
			for k in i.Children:
				print k.Name
				for j in alphalist:
					if (k.Name == j[0]):
	#			if (j[1] !=0):
						k.ThermalConductanceValue = Quantity(j[2])
						print k.Name
				#print i.ThermalConductanceValue
						print j[2]
						print "**"
	
						break
	#			else: 
	#				i.AutomaticThermalConductance = True
	#			r=r+1
ExtAPI.DataModel.Tree.Refresh()
