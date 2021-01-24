import sys
import os
from math import radians
from math import degrees
from os.path import join

from .dictionaries import *

def export_mouth_fix(exportfolderpath, bodyNo):
	#
	mouth_fix_string="\n"
	#
	for joint in ["mouth_L_fix_group","mouth_R_fix_group"]:
		empty = bpy.data.objects["_"+joint]
		snippet = ":Person\" + :person + \"Anim:Model01:"
		snippet = snippet+joint
		snippet = snippet + ".SNode? . {\n";
		snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(empty.location.y+ 0)    +" {:.6g}f,".format(empty.location.z+ 0)    +" {:.6g}f".format(empty.location.x+ 0)   +" );\n"	
		snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(empty.location.y+ 0)    +" {:.6g}f,".format(empty.location.z+ 0)    +" {:.6g}f".format(empty.location.x+ 0)   +" );\n"	
		snippet = snippet+ "};\n"
		snippet = snippet+""
		print (snippet)
		mouth_fix_string = mouth_fix_string+snippet
		#
	#
	mouth_fix_string = mouth_fix_string+"\n"
	print (mouth_fix_string)
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(mouth_fix_string)
	f.flush()
	f.close()





