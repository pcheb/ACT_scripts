#Inserting a NS with all the node IDs listed in an input file

##
def insert_NS_Node_IDs(node_info,NS_name):
# Takes an input file with a list of node numbers and creates a named selection in ANSYS by inserting the Node IDs in a worksheet
# node_info (list with an array of node ids Type: str) ; NS_name (str type)

	new_list=[]
	for i in node_list[0]:		# Convert node IDs from str to float 
		i=float(i)
		new_list.append(i)
		
	with Transaction():
		named_sel=ExtAPI.DataModel.Project.Model.AddNamedSelection()
		named_sel.SendToSolver=0
		named_sel.Location=ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.WorksheetSpecific)
		named_sel_WS=named_sel.Location
		named_sel.Name=NS_name
		count =0
		for n in new_list:
			named_sel_WS.AddRow()
			named_sel_WS.SetEntityType(count,NamedSelectionWorksheetEntityType.MeshNode)
			named_sel_WS.SetCriterion(count,NamedSelectionWorksheetCriterion.NodeId) #NamedSelection Creiteria --> NodeID
			named_sel_WS.SetOperator(count,NamedSelectionWorksheetOperator.Equal) #Smallest Distance from CS
			named_sel_WS.SetValue(count,n)  
			count = count+1
		named_sel_WS.Generate()
	ExtAPI.DataModel.Tree.Refresh()	
##

##
import csv
def readlog(input_file,header_1):
	u=[]
	
	cdir = ExtAPI.DataModel.AnalysisList[0].WorkingDir
	with open(cdir + '\\'+ input_file) as csvfile:
		fieldnames = [header_1];
		reader = csv.DictReader(csvfile, fieldnames=fieldnames, dialect = csv.excel)
		#reader.readheader()
		c=0
		for row in reader:
			if c>0:
				u.append(row[header_1])
			c = c+1	
	return [u]
##

node_list = readlog('T_Sensor_200_Node_Number.csv', 'Node_ID')
insert_NS_Node_IDs(node_list,'200_TSensor')