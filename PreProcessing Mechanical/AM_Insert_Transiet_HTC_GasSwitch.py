import string,re

#Use the name of the system in case the snippet is 
#used on multiple independent systems in the project. 

###
def writelog(data,name):
	import csv
	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + name,'wb') as csvfile:
		fieldnames = ['contactname'];
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

contacts_group = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.ConnectionGroup,True)	
contacts_group = filter(lambda x:not(x.InternalObject.Suppressed),contacts_group)
H2_cont = filter(lambda x:(x.GetType()==Ansys.ACT.Automation.Mechanical.Connections.ContactRegion),contacts_group[17].Children)
H2_cont = filter(lambda x:not(x.InternalObject.Suppressed),H2_cont)

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
no_TS = 5
with Transaction():
    for i in H2_cont:
        contactbody = i.ContactBodies
        targetbody = i.TargetBodies
        ## Extrcting contact and target material for HTC assignment
        for child in flat_list:
            if ((contactbody)==(child.Name)):
                contact_mat=child.InternalObject.MaterialName
			
            elif ((targetbody)==(child.Name)):
                targ_mat=child.InternalObject.MaterialName
   ## Adding a APDL command to assign respective  Time varying htc table       
        with Transaction():
            tab_name = "htctab_" + str(i.ObjectId)
            i.Children[2].Delete()
            i.Children[1].Delete()
          
   ## 3rd Command for inserting and controlling HTC values for each contact transiently
            cs_1=i.AddCommandSnippet()
            cs_1.Name = "HTC_table_new"
            cs_1.Input = "*DIM," + tab_name + ",TABLE," + str(no_TS) + ",1,1,TIME,"
            cs_1.AppendText("\n!Time Values")
            cs_1.AppendText("\n" + tab_name + "(1,0,1) = 0")
            cs_1.AppendText("\n" + tab_name + "(2,0,1) = 1e-2")
            cs_1.AppendText("\n" + tab_name + "(3,0,1) = 600")
            cs_1.AppendText("\n" + tab_name + "(4,0,1) = 1500")
            cs_1.AppendText("\n" + tab_name + "(5,0,1) = 2700")
   ## Assignment of HTC values for tables based on Contact and Target material     
            if contact_mat=="Aluminium 5083" or targ_mat =="Aluminium 5083" or contact_mat=="Aluminium 2014" or targ_mat =="Aluminium 2014" or contact_mat=="Aluminium 6061" or targ_mat =="Aluminium 6061" :
                cs_1.AppendText("\n!HTC Values")
                cs_1.AppendText("\n" + tab_name + "(1,1,1) = 5.368")
                cs_1.AppendText("\n" + tab_name + "(2,1,1) = 5.368")
                cs_1.AppendText("\n" + tab_name + "(3,1,1) = 3.87")
                cs_1.AppendText("\n" + tab_name + "(4,1,1) = 1.25")
                cs_1.AppendText("\n" + tab_name + "(5,1,1) = 1.5")
                
            elif contact_mat=="SiSiC" or targ_mat =="SiSiC" :
                cs_1.AppendText("\n!HTC Values")
                cs_1.AppendText("\n" + tab_name + "(1,1,1) = 4.673")
                cs_1.AppendText("\n" + tab_name + "(2,1,1) = 4.673")
                cs_1.AppendText("\n" + tab_name + "(3,1,1) = 3.936")
                cs_1.AppendText("\n" + tab_name + "(4,1,1) = 1.25")
                cs_1.AppendText("\n" + tab_name + "(5,1,1) = 1.5")
                
            elif contact_mat=="X5 (1.4301)" or targ_mat =="X5 (1.4301)" or contact_mat=="Steel 316" or targ_mat =="Steel 316" or contact_mat=="X6 (1.4980)" or targ_mat =="X6 (1.4980)":
                cs_1.AppendText("\n!HTC Values")
                cs_1.AppendText("\n" + tab_name + "(1,1,1) = 3.533")
                cs_1.AppendText("\n" + tab_name + "(2,1,1) = 3.533")
                cs_1.AppendText("\n" + tab_name + "(3,1,1) = 3.38")
                cs_1.AppendText("\n" + tab_name + "(4,1,1) = 1.25")
                cs_1.AppendText("\n" + tab_name + "(5,1,1) = 1.5")
                
            elif contact_mat=="ULE" or targ_mat =="ULE" or contact_mat=="Zerodur" or targ_mat =="Zerodur":
                cs_1.AppendText("\n!HTC Values")
                cs_1.AppendText("\n" + tab_name + "(1,1,1) = 6.86335")
                cs_1.AppendText("\n" + tab_name + "(2,1,1) = 6.86335")
                cs_1.AppendText("\n" + tab_name + "(3,1,1) = 4.045")
                cs_1.AppendText("\n" + tab_name + "(4,1,1) = 1.25")
                cs_1.AppendText("\n" + tab_name + "(5,1,1) = 1.5")
        
            elif contact_mat=="Acidur 1.4404" or targ_mat =="Acidur 1.4404" :
                cs_1.AppendText("\n!HTC Values")
                cs_1.AppendText("\n" + tab_name + "(1,1,1) = 3.915570423")
                cs_1.AppendText("\n" + tab_name + "(2,1,1) = 3.915570423")
                cs_1.AppendText("\n" + tab_name + "(3,1,1) = 3.727")
                cs_1.AppendText("\n" + tab_name + "(4,1,1) = 1.25")
                cs_1.AppendText("\n" + tab_name + "(5,1,1) = 1.5")
                
            else:
                cs_1.AppendText("\n!HTC Values")
                cs_1.AppendText("\n" + tab_name + "(1,1,1) = 4.81267")
                cs_1.AppendText("\n" + tab_name + "(2,1,1) = 4.81267")
                cs_1.AppendText("\n" + tab_name + "(3,1,1) = 3.76846")
                cs_1.AppendText("\n" + tab_name + "(4,1,1) = 1.25")
                cs_1.AppendText("\n" + tab_name + "(5,1,1) = 1.5")
                print i.Name
                print contact_mat + "--" + targ_mat
                print "****"
        ExtAPI.DataModel.Tree.Refresh()
        
        with Transaction():
            cs=i.AddCommandSnippet()
#	        cs.Name="CiD_TiD_"+str(i.ObjectId)
            cs.Input = "rmod,tid,14,%" + tab_name + "%"
            cs.AppendText ("\nrmod,cid,14,%" + tab_name + "%")
        ExtAPI.DataModel.Tree.Refresh()
ExtAPI.DataModel.Tree.Refresh()
