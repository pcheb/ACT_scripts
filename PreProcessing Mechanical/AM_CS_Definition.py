# (C) 2016 by Carl Zeiss GmbH
# 
import xml.etree.ElementTree as ET
import math
#import Ansys.Core.Units

def evtoTrafo(M):
	beta=math.acos(M[2][2]);
	if beta!=0:
		alpha = -math.atan2(-M[2][0],-M[2][1])
		gamma = math.atan2(M[0][2],M[1][2])
	else:
		alpha = 0
		gamma = -math.atan2(-M[0][1],M[1][1])
	return (alpha/math.pi*180.0,beta/math.pi*180.0,gamma/math.pi*180.0)


def selectfn():
		import clr
		# from http://www.ironpython.info/index.php?title=SaveFileDialog
		clr.AddReference('System.Windows.Forms')
		clr.AddReference('System.Drawing')			
		from System.Drawing import Bitmap
		from System.Drawing.Imaging import ImageFormat
		from System.Windows.Forms import DialogResult, OpenFileDialog
		# Not a very interesting image
		image = Bitmap(1, 1)
		dialog = OpenFileDialog()
		dialog.Title = 'Read XML'
		dialog.Filter = 'XML Files(*.xml)|*.xml'
		
		if dialog.ShowDialog() == DialogResult.OK:
			# Should really check what format they *really* want!
			try:
				return(dialog.FileName)
			except IOError, e:
				print 'An error occurred:', e

def readcsxml(model,newcs,ExtAPI):
	x=ET.parse(selectfn())
	z=x.getroot().findall('definitions')[0]
	ExtAPI.Log.WriteMessage("Loading CS XML"  + z.tag)
	#z=x.findall('Carl_Zeiss_SMT_Container')[0].findall('definitions')[0]
	
	ExtAPI.Log.WriteMessage("Loading CS XML"  + [i.tag for i in z][0])
	csnew=[];
	for i in z.findall('coordinate_system'):
		origin = i.findall('origin');
		name= "IMP" + i.get("name")
		x=float(origin[0].findall('x')[0].text)/1000
		y=float(origin[0].findall('y')[0].text)/1000
		z=float(origin[0].findall('z')[0].text)/1000
		M = [[float(i.findall(k)[0].findall(j)[0].text) for j in ["ex","ey","ez"]] for k in ["x_axis","y_axis","z_axis"]] ;
		rot =  evtoTrafo(M);
		cs=newcs(name,x,y,z,rot[0],rot[1],rot[2],model)
		x=cs
		csnew.append({'name':x.Name,'origin':[x.InternalObject.OriginXLocation,x.InternalObject.OriginYLocation,x.InternalObject.OriginZLocation],'evx':x.XAxis,'evy':x.YAxis,'evz':x.ZAxis})
	return csnew

	
def newcs(name,x,y,z,rx,ry,rz,model):
	import Ansys.ACT
	cs=model.CoordinateSystems.AddCoordinateSystem()
	cs.Name = name
	cs.InternalObject.OriginAlignment=0
	cs.InternalObject.OriginXLocation = x
	cs.InternalObject.OriginYLocation = y
	cs.InternalObject.OriginZLocation = z
	cs.AddTransformation(TransformationType.Rotation,CoordinateSystemAxisType.PositiveZAxis)
	cs.AddTransformation(TransformationType.Rotation,CoordinateSystemAxisType.PositiveXAxis)
	cs.AddTransformation(TransformationType.Rotation,CoordinateSystemAxisType.PositiveZAxis)
	cs.SetTransformationValue(1,rx)
	cs.SetTransformationValue(2,ry)
	cs.SetTransformationValue(3,rz)
	return cs


ExtAPI.Log.WriteMessage("Loading CS XML")
#reload(csparser)
model=ExtAPI.DataModel.Project.Model
readcsxml(model,newcs,ExtAPI);