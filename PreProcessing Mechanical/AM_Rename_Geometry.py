## Script contains multiple fucntions to rename the bodies 
## in the ANsys mechanical tree based on "\" as a seperator

import string
import re
import sys
import csv

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
			
###

def remove_last():
 	## Filter names to all charecters until the last "\"	
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename
				i=1
				new_name = rename[0]
				print new_name
				while i < len(rename)-1:				# Filter names to all charecters until the last "\"
					print i
					new_name = new_name + "\\" + rename[i]
					print new_name
					i = i+1
					
				child.Name = new_name					# Assign modified names to the Geometry List in mechanical
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###	
def first_section():
 	## Acvtivate to extract only a specific section  (eg: "1stSection\2nd Section\3rd Section\4th Section..." ) 	
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename
			
				child.Name = rename[0]					# Extract only the 1st Section
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###	
def second_section():
 	## Acvtivate to extract only a specific section  (eg: "1stSection\2nd Section\3rd Section\4th Section..." ) 	
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename
	
				child.Name = rename[1]				# Extract only the 2nd Section
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###	
def third_section():
 	## Acvtivate to extract only a specific section  (eg: "1stSection\2nd Section\3rd Section\4th Section..." )	
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename
	
	
				child.Name = rename[2]				# Extract only the 3rd Section
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###	
def fourth_section():
 	## Acvtivate to extract only a specific section  (eg: "1stSection\2nd Section\3rd Section\4th Section..." )
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename
	
				child.Name = rename[3]				# Extract only the 4th Section
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###
def odd_section():
	## Acvtivate to extract alternate odd section (eg: "1stSection\2nd Section\3rd Section\4th Section..." )
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename	
				i = 2
				new_name = rename[0]
				while i < len(rename):				
					print i
					new_name = new_name + "\\" + rename[i]
					print new_name
					i = i+2
					
				child.Name = new_name
	ExtAPI.DataModel.Tree.Refresh()
	return None
###			

###	
def even_section():
	## Acvtivate to extract alternate even section (eg: "1stSection\2nd Section\3rd Section\4th Section..." )
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename	
				i = 3
				new_name = rename[1]
				while i < len(rename):				
					print i
					new_name = new_name + "\\" + rename[i]
					print new_name
					i = i+2
					
				child.Name = new_name
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###
def first_last():
	## Activate to extract only the first and the last sections (eg: "1stSection\...\...\...\Last Section" )
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename	
				i = 1
				new_name = rename[0]
				while i < len(rename):				# Filter names to all charecters until the last "\"
					if (i ==len(rename)-1):
						new_name = new_name + "\\" + rename[i]
						print new_name
					i = i+1
					
				child.Name = new_name
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###
def keep_only_last():
	## Activate to extract only the the last section (eg: "1stSection\...\...\...\Last Section" )
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):				
				rename = re.split(r'\\', child.Name)		# Split names to rename	
				i = len(rename)-1
				
				child.Name = rename[i]
	ExtAPI.DataModel.Tree.Refresh()
	return None
###

###
def search_replace(var_1, var_2):
	## Activate to extract only the the last section (eg: "1stSection\...\...\...\Last Section" )
	new_list = flatten(ExtAPI.DataModel.Project.Model.Geometry)
	with Transaction():
		for child in new_list:
			if (child.Visible != False):
				print child.Name
				child.Name = re.sub(var_1, var_2, child.Name)		# Substitute the name 
				print child.Name
	ExtAPI.DataModel.Tree.Refresh()
	return None
###	

##Regular Expression##
# .* --> Matches evrything
# .*V --> Matches everything until a captial 'V' (eg: "PoB3500 M_M RM 180-V7\Actuator_M7" --> will match --> "PoB3500 M_M RM 180-V")
# \d --> will match all digits (eg: "PoB3500 M_M RM 180-V7\Actuator_M7" --> will match --> "3500" , "180", "7" and "7"
# .*V\d will match everything until captial 'V' followed by a number --> (eg: "PoB3500 M_M RM 180-V7\Actuator_M7" --> will match --> "PoB3500 M_M RM 180-V7")
# to add something at the end inp="$" (searches end of line) replace with out="xyz"
###########################

#################################################
##Activate to search and replace sepcific phrases
#################################################

inp = "$"			#Regular expression to catch the phrase you want to replace
out = "_SFr"					# Phrase to be insrted instead
search_replace(inp,out)		# Function for search and replace "inp" with "out"


#################################################
##Activate to reomove only last section
#################################################
#remove_last()     		# Activate(Remove Comment only this line) to reomove only last section


#################################################
# Acvtivate to extract only 1st section
#################################################
#first_section()		# Acvtivate(Remove Comment only this line) to extract only 1st section


#################################################
# Acvtivate to extract only 2nd section
#################################################
#second_section()	# Acvtivate(Remove Comment only this line) to extract only 2nd section


#################################################
# Acvtivate to extract only the 3rd section
#################################################
#	third_section()		# Acvtivate(Remove Comment only this line) to extract only the 3rd section


#################################################
# Acvtivate to extract only the 4th section
#################################################
#fourth_section()	# Acvtivate(Remove Comment only this line) to extract only the 4th section


#################################################
# Acvtivate to extract alternate odd section
#################################################
#odd_section()		# Acvtivate(Remove Comment only this line) to extract alternate odd section

#################################################
# Acvtivate to extract alternate even section
#################################################
#even_section()		# Acvtivate(Remove Comment only this line) to extract alternate even section


#################################################
# Activate to extract only the first and the last sections
#################################################
#first_last()		# Activate(Remove Comment only this line) to extract only the first and the last sections

#################################################
# Activate to extract only the first and the last sections
#################################################
keep_only_last()		# Activate(Remove Comment only this line) to extract only the first and the last sections

##else
#	print "Error!!! Please enter valid option number!!"