import sys
import os
import bpy
from math import radians
from math import degrees
from os.path import join


def export_anus_default(exportfolderpath, bodyNo):
	anus_default = [
	 0, 
	 0, 
	 0, 
	 90, 
	 0, 
	 0, 
	 1, 
	 1, 
	 1, 
	 0, 
	 0, 
	 0, 
	 0, 
	 0, 
	 0, 
	 1, 
	 1, 
	 1, 
	 0, 
	 0.867,
	 -0.038, 
	 5, 
	 0, 
	 0, 
	 1, 
	 1, 
	 1, 
	 bpy.data.objects['_anus_joint'].location.y,
	 bpy.data.objects['_anus_joint'].location.z,
	 bpy.data.objects['_anus_joint'].location.x, 
	 0, 
	 0, 
	 0, 
	 1, 
	 1, 
	 1
	]
	#
	anus_default_values_str = '\n:Person" + :person + "Anim:Model01:anus_poseBlend.PoseDefault ' + str(["{:.6f}f".format(float(i)) for i in anus_default])+';'  # + str([float("%.8f" % i) for i in anus_default])+';'
	anus_default_values_str = anus_default_values_str.replace("-0.000000f", "0f").replace("0.000000f", "0f").replace("-1.000000f", "-1f").replace("1.000000f", "1f").replace("'", "")
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(anus_default_values_str)
	f.flush()
	f.close()



