import re
import sys



# C:\Users\xyakem\Desktop\LIT_ETMO_THERMAL_UTILITIES\Thermal Model Input + Info\b1007\Scripts ANSYS>"C:\Program Files\ANSYS Inc\v182\commonfiles\IronPython\ipy64.exe" SortFilterInputFilveFromCAD.py


#print "Hallo" + sys.argv[1] + "\n"
#print "Hallo" 
file_object  = open('filtered.txt', "r");


out_dict={};
for i in file_object.readlines():
	i=unicode(i,'utf8')
	m=re.match("^(.*)\t(.*)$",i)
	out_dict[m.group(1)]=m.group(2);


fo = open('sorted_filtered.txt',"w");
for j in sorted(out_dict.keys()):
	fo.write((j+"\t"+out_dict[j]+"\n").encode('utf8'));
fo.close();