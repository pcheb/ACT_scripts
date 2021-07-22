import re
import sys

#C:\Users\xyakem\Desktop\LIT_ETMO_THERMAL_UTILITIES\Thermal Model Input + Info\b1007\Scripts ANSYS>"C:\Program Files\ANSYS Inc\v182\commonfiles\IronPython\ipy64.exe" FilterInputFilveFromCAD.py C:\Users\xyakem\Downloads\Names_Geom_POB3500-u.txt

#print "Hallo" + sys.argv[1] + "\n"
#print "Hallo" 
file_object  = open(sys.argv[1], "r");
fo = open('filtered.txt',"w");

def l(x):
	return (re.match(".*[.](PRT|ASM).*",x)!=None);

count = 0 ;
for i in file_object.readlines():
	if l(i):
		i=unicode(i,'utf8')
		m=re.match("^.*?[(]?([^ ]*)[.](PRT|ASM)[)]?.*",i)
		if m==None:
			print i
		else:
			m2 = re.match("^.{82}(.{40})",i);
			s=m2.group(1);
			s=re.sub("[ ]*$","",s);
			s1 = m.group(1);
			s1=re.sub('[<].*[>]$','',s1);
			fo.write((s1+"\t"+s+"\n").encode('utf8'))

fo.close();