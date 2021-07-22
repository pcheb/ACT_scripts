#Prereq: Group all the CS for Tsensors in a folder called "Tsensor_CS" in the tree

cs = ExtAPI.DataModel.Project.Model.CoordinateSystems.GetChildren(DataModelObjectCategory.TreeGroupingFolder,True)
with Transaction():
	for c in cs:
		if c.Name == 'Tsensor_CS' :
			for child in c.Children:
				cs_id = child.ObjectId
				named_sel=ExtAPI.DataModel.Project.Model.AddNamedSelection()
				named_sel.SendToSolver=0
				named_sel.Location=ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.WorksheetSpecific)
				named_sel_WS=named_sel.Location
				named_sel.Name=child.Name[6:]
				named_sel_WS.AddRow()
				named_sel_WS.SetAction(0,NamedSelectionWorksheetAction.Add)
				named_sel_WS.SetEntityType(0,NamedSelectionWorksheetEntityType.MeshNode)
				named_sel_WS.SetCriterion(0,NamedSelectionWorksheetCriterion.Distance) #NamedSelection Distance
				named_sel_WS.SetOperator(0,NamedSelectionWorksheetOperator.Smallest) #Smallest Distance from CS
				named_sel_WS.SetCoordinateSystemSelection(0,cs_id)   
				named_sel_WS.Generate()
ExtAPI.DataModel.Tree.Refresh()	
