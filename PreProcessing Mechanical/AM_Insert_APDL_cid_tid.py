## Prerequisite: 
## --> Excel Sheet with name of body and material name(matches charecters to ANSYS Material DB)

## Script reads the material assignment excel sheet and 
## assigns the respective materials to the list of bodies listed in Excel
import string,re

#Use the name of the system in case the snippet is 
#used on multiple independent systems in the project. 
 
	
contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.ContactRegion,True)	
contacts = filter(lambda x:not(x.InternalObject.Suppressed),contacts)
contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
contacts = filter(lambda x:not(x.SourceLocation==None),contacts);

r=1
with Transaction():
	for i in contacts:
		cs=i.AddCommandSnippet()
		cs.Name="CiD_TiD_"+str(i.ObjectId)
		cs.Input = "C"+ str(i.ObjectId)+" = cid"
		cs.AppendText ("\nT"+str(i.ObjectId)+" = tid")
ExtAPI.DataModel.Tree.Refresh()

##To Delete all existing APDL Commands and create a new APDL snippet
#with Transaction():
#	for i in contacts:
#		if len(i.Children)>0:
#			for j in range(0,len(i.Children)):
#				i.Children[j].Delete()
#		cs=i.AddCommandSnippet()
#		cs.Name="CiD_TiD_"+str(i.ObjectId)
#		cs.Input = "CONT_"+ str(i.ObjectId)+" = cid"
#		cs.AppendText ("\nTARG_"+str(i.ObjectId)+" = tid")
#ExtAPI.DataModel.Tree.Refresh()
