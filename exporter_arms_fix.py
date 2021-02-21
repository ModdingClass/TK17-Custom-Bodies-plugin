import bpy
import sys
import os
from math import radians
from math import degrees
from os.path import join
import mathutils
import math
from mathutils import Vector
from mathutils import Matrix

from .dictionaries import *


#//	Object.Name "Model01:knee_LClips1__knee_L_initSource";
#//var :mySplineVector3f :Person" + :person + "Anim:Model01:leg_LClips1__leg_L_initSource.Curve[1] ?;
#//:mySplineVector3f.KeyValue [ (0.9113f, 0f, -0.095f), (0.9113f, 0f, -0.095f)];

#Model01:arm_L_effector ->Swrist_L_joint

def export_arms_fix(exportfolderpath, bodyNo):
	#
	#
	wrist_L_joint = bpy.data.objects[ "_wrist_L_joint"]
	forearm_L_joint = bpy.data.objects[ "_forearm_L_joint"]
	arms_fix_string="\n"
	#effector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_L_effector"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(wrist_L_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_L_joint.location.x+ 0)    +" {:.6g}f".format(wrist_L_joint.location.z+ 0)   +" );\n"   #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(wrist_L_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_L_joint.location.x+ 0)    +" {:.6g}f".format(wrist_L_joint.location.z+ 0)   +" );\n"  #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(forearm_L_joint.location.y+ 0)    +" {:.6f}f,".format(forearm_L_joint.location.z+ 0)    +" {:.6g}f".format(forearm_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"
	#arm_L_group depends on hand_L_target01_locator_parent because it has a constraint reparent on it
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_L_target01_locator_parent"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_L_joint.matrix_world.to_translation().y+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"
	#hand_L_target01
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_L_target01"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_L_joint.matrix_world.to_translation().y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_L_joint.matrix_world.to_translation().y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	snippet = ":Person\" + :person + \"Pick:body_hand_L_pick.SNode?.Translation ( -0.096892565f, 0.0010810591f, -0.0056944136f );\n"
	#:Person" + :person + "Pick:body_hand_L_pick.SNode?.Translation ( -0.096892565f, 0.0010810591f, -0.0056944136f );
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	#Selbow_L_group
	line_b = bpy.data.objects[ "_elbow_L_joint"].matrix_world.to_translation()
	# we move it along local Y axis, get the moved vector then move it back to original location
	bpy.data.objects[ "_elbow_L_joint"].matrix_basis *= Matrix.Translation((0.0, -1.0, 0.0))
	#for some reason we need to update the scene, otherwise the matrix wont work
	bpy.data.scenes[0].update()
	line_a = bpy.data.objects[ "_elbow_L_joint"].matrix_world.to_translation()
	bpy.data.objects[ "_elbow_L_joint"].matrix_basis *= Matrix.Translation((0.0, 1.0, 0.0))
	bpy.data.scenes[0].update()
	#
	plane_co =  bpy.data.objects[ "_shoulder_L_joint"].matrix_world.to_translation()
	plane_no = Vector ((-1,0,0))
	calculated_elbow_L_group = mathutils.geometry.intersect_line_plane(line_b, line_a, plane_co, plane_no)
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"elbow_L_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(calculated_elbow_L_group.x+ 0)    +" {:.6f}f,".format(calculated_elbow_L_group.z+ 0)    +" {:.6g}f".format(-calculated_elbow_L_group.y+ 0)   +" );\n"   #here we switch to xz -y	
	#we also need to do RotationPivotTranslation ... 
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	#ellbow_L_locator
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ellbow_L_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(calculated_elbow_L_group.x+ 0)    +" {:.6f}f,".format(calculated_elbow_L_group.z+ 0)    +" {:.6g}f".format(-calculated_elbow_L_group.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	#
	#
	wrist_R_joint = bpy.data.objects[ "_wrist_R_joint"]
	forearm_R_joint = bpy.data.objects[ "_forearm_R_joint"]
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_R_effector"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(wrist_R_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_R_joint.location.x+ 0)    +" {:.6g}f".format(wrist_R_joint.location.z+ 0)   +" );\n"   #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(wrist_R_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_R_joint.location.x+ 0)    +" {:.6g}f".format(wrist_R_joint.location.z+ 0)   +" );\n"  #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(forearm_R_joint.location.y+ 0)    +" {:.6f}f,".format(forearm_R_joint.location.z+ 0)    +" {:.6g}f".format(forearm_R_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string = arms_fix_string+"\n"
	#arm_R_group depends on hand_R_target01_locator_parent because it has a constraint reparent on it
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_R_target01_locator_parent"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_R_joint.matrix_world.to_translation().y+ 0)   +" );\n"  #here we switch to xz -y	(daz to villa)
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_R_target01"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_R_joint.matrix_world.to_translation().y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_R_joint.matrix_world.to_translation().y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	#Selbow_R_group
	line_b = bpy.data.objects[ "_elbow_R_joint"].matrix_world.to_translation()
	# we move it along local Y axis, get the moved vector then move it back to original location
	bpy.data.objects[ "_elbow_R_joint"].matrix_basis *= Matrix.Translation((0.0, 1.0, 0.0))
	#for some reason we need to update the scene, otherwise the matrix wont work
	bpy.data.scenes[0].update()
	line_a = bpy.data.objects[ "_elbow_R_joint"].matrix_world.to_translation()
	bpy.data.objects[ "_elbow_R_joint"].matrix_basis *= Matrix.Translation((0.0, -1.0, 0.0))
	bpy.data.scenes[0].update()
	#
	plane_co =  bpy.data.objects[ "_shoulder_R_joint"].matrix_world.to_translation()
	plane_no = Vector ((-1,0,0))
	calculated_elbow_R_group = mathutils.geometry.intersect_line_plane(line_a, line_b, plane_co, plane_no)
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"elbow_R_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(calculated_elbow_R_group.x+ 0)    +" {:.6f}f,".format(calculated_elbow_R_group.z+ 0)    +" {:.6g}f".format(-calculated_elbow_R_group.y+ 0)   +" );\n"   #here we switch to xz -y	
	#we also need to do RotationPivotTranslation ... 
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	#ellbow_R_locator
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ellbow_R_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(calculated_elbow_R_group.x+ 0)    +" {:.6f}f,".format(calculated_elbow_R_group.z+ 0)    +" {:.6g}f".format(-calculated_elbow_R_group.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#
	arms_fix_string += ":Person\" + :person + \"Anim:Model01:wrist_L_joint.SNode?.RotationAxis (0f, 0f, 0f);\n";
	print (arms_fix_string)
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(arms_fix_string)
	f.flush()
	f.close()

#def export_arms_ikhandle_fix():
#	# we dont do much here...
#	#

def export_elbows_grup_fix(exportfolderpath, bodyNo):
	#Sellbow_R_locator location has same value as Selbow_R_group RotationPivot
	#    -0.15868729, 1.4871917, -0.19562815 
	_shoulder_R_joint = bpy.data.objects[ "_shoulder_R_joint"]
	forearm_L_joint = bpy.data.objects[ "_forearm_L_joint"]
	arms_fix_string="\n"
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_L_effector"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(wrist_L_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_L_joint.location.x+ 0)    +" {:.6g}f".format(wrist_L_joint.location.z+ 0)   +" );\n"   #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(wrist_L_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_L_joint.location.x+ 0)    +" {:.6g}f".format(wrist_L_joint.location.z+ 0)   +" );\n"  #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(forearm_L_joint.location.y+ 0)    +" {:.6f}f,".format(forearm_L_joint.location.z+ 0)    +" {:.6g}f".format(forearm_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"
	#
	wrist_R_joint = bpy.data.objects[ "_wrist_R_joint"]
	forearm_R_joint = bpy.data.objects[ "_forearm_R_joint"]
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_R_effector"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(wrist_R_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_R_joint.location.x+ 0)    +" {:.6g}f".format(wrist_R_joint.location.z+ 0)   +" );\n"   #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(wrist_R_joint.location.y+ 0)    +" {:.6f}f,".format(wrist_R_joint.location.x+ 0)    +" {:.6g}f".format(wrist_R_joint.location.z+ 0)   +" );\n"  #here we switch  from yzx to yxz	
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(forearm_R_joint.location.y+ 0)    +" {:.6f}f,".format(forearm_R_joint.location.z+ 0)    +" {:.6g}f".format(forearm_R_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string = arms_fix_string+"\n"
	arms_fix_string = arms_fix_string.replace("-0.000000f", "0f").replace("0.000000f", "0f").replace("-1.000000f", "-1f").replace("1.000000f", "1f")
	#
	print (arms_fix_string)
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(arms_fix_string)
	f.close()
