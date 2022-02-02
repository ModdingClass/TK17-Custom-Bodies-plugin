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
	
	vag_default = [
		0, 0, 0, 
		90, 0, 0, 
		1, 1, 1, 
		0, 0, 0, 
		0, 0, 0, 
		1, 1, 1, 
		1, 1, 1, 
		bpy.data.objects['_vagina_R_jointEnd'].location.y, bpy.data.objects['_vagina_R_jointEnd'].location.z, bpy.data.objects['_vagina_R_jointEnd'].location.x,  #Svagina_R_jointEnd
		0, 0, 0, 
		1, 1, 1, 
		bpy.data.objects['_vagina_R_joint01'].location.y, bpy.data.objects['_vagina_R_joint01'].location.z, bpy.data.objects['_vagina_R_joint01'].location.x, #Svagina_R_joint01
		0, 0, 0, 
		1, 1, 1, 
		bpy.data.objects['_vagina_L_jointEnd'].location.y, bpy.data.objects['_vagina_L_jointEnd'].location.z, bpy.data.objects['_vagina_L_jointEnd'].location.x, #Svagina_L_jointEnd
		0, 0, 0, 
		1, 1, 1, 
		bpy.data.objects['_vagina_L_joint01'].location.y, bpy.data.objects['_vagina_L_joint01'].location.z, bpy.data.objects['_vagina_L_joint01'].location.x, #Svagina_L_joint01
		0, 0, 0,
		1, 1, 1, 
		0
	]	
	
	vag_default_values_str = '\n:Person" + :person + "Anim:Model01:vagina_poseBlend.PoseDefault ' + str(["{:.6f}f".format(float(i)) for i in vag_default])+';'  
	vag_default_values_str = vag_default_values_str.replace("-0.000000f", "0f").replace("0.000000f", "0f").replace("-1.000000f", "-1f").replace("1.000000f", "1f").replace("'", "")
	#vag_default_values_str2 = '\n:Person" + :person + "AnimSingle:Model01:vagina_poseBlend.PoseDefault ' + str(["{:.6f}f".format(float(i)) for i in vag_default])+';'  
	#vag_default_values_str2 = vag_default_values_str2.replace("-0.000000f", "0f").replace("0.000000f", "0f").replace("-1.000000f", "-1f").replace("1.000000f", "1f").replace("'", "")
	
	
	
	
	
	
	
	
	
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(anus_default_values_str)
	f.write(vag_default_values_str)
	#f.write(vag_default_values_str2)
	f.flush()
	f.close()



