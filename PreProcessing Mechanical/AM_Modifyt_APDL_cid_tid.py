## Script searches and overwrites the APDL Commands with a Command Snippet name of "CiD_TiD_

import string,re

#Use the name of the system in case the snippet is 
#used on multiple independent systems in the project. 
 
	
contacts = ExtAPI.DataModel.Project.Model.Connections.GetChildren(DataModelObjectCategory.ContactRegion,True)	
contacts = filter(lambda x:not(x.InternalObject.Suppressed),contacts)
contacts = filter(lambda x:not(x.TargetLocation==None),contacts);
contacts = filter(lambda x:not(x.SourceLocation==None),contacts);


with Transaction():
	for i in contacts:
		name = "CiD_TiD_"+str(i.ObjectId)
		for j in i.Children:
			if j.Name==name:
				j.Input = "C"+str(i.ObjectId)+" = cid"
				j.AppendText ("\nT"+str(i.ObjectId)+" = tid")
#			if len(i.Children)>1:
#				i.Children[1].Delete()
ExtAPI.DataModel.Tree.Refresh()