# Python Script, API Version = V15
import re

#Definition function rename
def rename_partb(currentPart,in_dict):
    for subpart in currentPart.Components:
            my_template = subpart.Template
            Part_Name = my_template.Name
            print Part_Name
			Body_Name = subpart.GetBodies()[0].Name
            print Body_Name
            for n in in_dict.keys():
                if Body_Name.startswith(n):
                    my_template.Name = in_dict[n]
            rename_partb(my_template,in_dict)
			
		

# Get list of all components
part = GetRootPart()

# Read list with part numbers and partnames 
file_object  =open(r'c:\Users\xyasa\Documents\work\3400\Actuator\20 Lastenheft\Materials\3400AktuatorStueckliste_Skript_utf8.txt', 'r');

# Create array from input file
out_dict={};
for i in file_object.readlines():
    i=unicode(i,'utf8')
    m=re.match("^(.*)\t(.*)$",i) 
    out_dict[m.group(1)]=m.group(2);
 
# Call rename function 
rename_partb(part,out_dict)
