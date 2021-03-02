import sys
import os
from math import radians
from math import degrees
from os.path import join

from .dictionaries import *

def export_joints_fix(exportfolderpath, bodyNo):
	adjusted_bones=""
	adjusted_bones =":Person\" + :person + \"Anim:Model01:root.SNode? . {\n"
	adjusted_bones = adjusted_bones +"\t.Translation (0f, 0.98419f, -0.031404294f);\n"
	adjusted_bones = adjusted_bones +"\t.Rotation (90f, -7.1250162f, 90f);\n};\n"
	#
	for joint in animSkeletonValues:
		if joint!="root":
			empty = bpy.data.objects["_"+joint]
			snippet = ":Person\" + :person + \"Anim:Model01:"
			snippet = snippet+joint
			snippet = snippet + ".SNode? . {\n";
			snippet = snippet+ "\t.JointOrientation ("   +" {:.6f}f,".format(degrees(empty.rotation_euler.y)+ 0)    +" {:.6f}f,".format(degrees(empty.rotation_euler.z)+ 0)    +" {:.6f}f".format(degrees(empty.rotation_euler.x)+ 0)   +" );\n"
			snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(empty.location.y+ 0)    +" {:.6f}f,".format(empty.location.z+ 0)    +" {:.6f}f".format(empty.location.x+ 0)   +" );\n"	
			snippet = snippet+ "\t.Rotation ( 0.0f, 0.0f, 0.0f );\n"
			snippet = snippet+ "};\n"
			snippet = snippet+""
			#print (snippet)
			adjusted_bones = adjusted_bones+snippet
		#
	#
	#
	#Smouth_L_fix_group
	#Smouth_R_fix_group
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	print("joints saved to: "+file_path)
	f = open(file_path, 'a')
	f.write(adjusted_bones)
	f.close()
	#
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)




