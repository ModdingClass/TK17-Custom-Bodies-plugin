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

from .ik_tools import *
from .dictionaries import *
from mathutils.geometry import intersect_point_line

#//	Object.Name "Model01:knee_LClips1__knee_L_initSource";
#//var :mySplineVector3f :Person" + :person + "Anim:Model01:leg_LClips1__leg_L_initSource.Curve[1] ?;
#//:mySplineVector3f.KeyValue [ (0.9113f, 0f, -0.095f), (0.9113f, 0f, -0.095f)];

#Model01:arm_L_effector ->Swrist_L_joint

def export_arms_fix(exportfolderpath, bodyNo):
	#
	# first we need to start with arm_LClips1__arm_L_initSource
	# but this is not done yet, how could I miss this initialization?
	# on a second thought, to match the body, maybe this should be actually 0 ? game default has a rotation on Y axis of -18/18 degrees
	#
	neck_joint01 = bpy.data.objects[ "_neck_joint01"]
	wrist_L_joint = bpy.data.objects[ "_wrist_L_joint"]
	forearm_L_joint = bpy.data.objects[ "_forearm_L_joint"]
	forearm_L_joint = bpy.data.objects[ "_forearm_L_joint"]
	#arm_R_ikEffector,arm_R_ikHandle = getIKValues("Armature","elbow_joint.R","wrist_joint.R")
	arm_R_ikEffector,arm_R_ikHandle, distance, translation = getClosestPointFromBoneProjection("Armature","elbow_joint.R","wrist_joint.R")
	arm_L_ikEffector,arm_L_ikHandle, distance,translation = getClosestPointFromBoneProjection("Armature","elbow_joint.L","wrist_joint.L")
	arms_fix_string="\n"
	#
	#arm_LClips1__arm_L_initSource
	#those are actually rotations that are applied to the hands, in this case we want to keep the rest pose at 0
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:arm_LClips1__arm_L_initSource.Curve[0] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(0)    +" {:.6g}f,".format(0)    +" {:.6g}f".format(0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#
	#arm_RClips1__arm_R_initSource1   (there must be a 1 at the end, is not like arm_RClips1__arm_R_initSource and that is it)
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:arm_RClips1__arm_R_initSource1.Curve[0] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(0)    +" {:.6g}f,".format(0)    +" {:.6g}f".format(0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#	
	#
	ob = bpy.data.objects.new( "_neck_joint01_translated", None )
	ob.rotation_mode = 'YZX'
	ob.parent = neck_joint01
	ob.matrix_world =  neck_joint01.matrix_world
	ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
	ob.matrix_parent_inverse.identity()       
	# Define the translation we want to perform in local space (after rotation) # we actually move down the local Y axis of the ankle joint
	trans_local = neck_joint01.matrix_world.inverted() * Vector((0,0,0))
	# Convert the local translation to global with the 3x3 rotation matrix of our object
	trans_world = ob.matrix_world.to_3x3() * trans_local
	# Apply the translation
	ob.matrix_world.translation += trans_world
	bpy.context.scene.objects.link( ob )
	neck_joint01_translated = ob
	#
	#elbow_LClips1__elbow_L_initSource + elbow_RClips1__elbow_R_initSource
	elbow_initSource = neck_joint01.matrix_world.inverted() * Vector((0,0,0))
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:elbow_LClips1__elbow_L_initSource.Curve[0] ?;"
	mySplineVectorString = "("+" {:.6f}f,".format(elbow_initSource.y+ 0)    +" {:.6f}f,".format(-elbow_initSource.z+0)    +" {:.6f}f".format(elbow_initSource.x+0)   +" )" #??? y,-z,x
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:elbow_RClips1__elbow_R_initSource.Curve[0] ?;"
	mySplineVectorString = "("+" {:.6f}f,".format(elbow_initSource.y+ 0)    +" {:.6f}f,".format(-elbow_initSource.z+0)    +" {:.6f}f".format(elbow_initSource.x+0)   +" )" # y,-z,x
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#	
	arms_fix_string=arms_fix_string + "\n"	
	#
	snippet = ":Person\" + :person + \"Pick:body_hand_L_pick.SNode?.Translation ( -0.096892565f, 0.0010810591f, -0.0056944136f );\n"
	arms_fix_string = arms_fix_string+snippet
	snippet = ":Person\" + :person + \"Anim:Model01:wrist_L_joint.SNode?.RotationAxis (0f, 0f, 0f);\n";
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	#
	#
	wrist_R_joint = bpy.data.objects[ "_wrist_R_joint"]
	forearm_R_joint = bpy.data.objects[ "_forearm_R_joint"]
	elbow_R_joint = bpy.data.objects[ "_elbow_R_joint"]
	arm_R_ikEffector,arm_R_ikHandle = getIKValues("Armature","elbow_joint.R","wrist_joint.R")
	arm_R_ikEffector,arm_R_ikHandle, distance,translationAlongY = getClosestPointFromBoneProjection("Armature","elbow_joint.R","wrist_joint.R")
	localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection("Armature","forearm_joint.R","wrist_joint.R")
	wrist_R_joint_world_coordinates = wrist_R_joint.matrix_world.to_translation()
	arm_effector = elbow_R_joint.matrix_world.inverted() * wrist_R_joint_world_coordinates
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_R_effector"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(translationAlongY.x+ 0)    +" {:.6g}f,".format(translationAlongY.y+ 0)    +" {:.6g}f".format(translationAlongY.z + 0)   +" );\n"  #no switch	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(translationAlongY.x+ 0)    +" {:.6g}f,".format(translationAlongY.y+ 0)    +" {:.6g}f".format(translationAlongY.z + 0)   +" );\n"  #no switch	
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(forearm_R_joint.location.y+ 0)    +" {:.6f}f,".format(forearm_R_joint.location.z+ 0)    +" {:.6g}f".format(forearm_R_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string = arms_fix_string+"\n"
	#arm_R_group depends on hand_R_target01_locator_parent because it has a constraint reparent on it
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_R_target01_locator_parent"
	snippet = snippet + ".SNode? . {\n";
	#snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_R_joint.matrix_world.to_translation().y+ 0)   +" );\n"  #here we switch to xz -y	(daz to villa)
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(arm_R_ikHandle.x+ 0)    +" {:.6f}f,".format(arm_R_ikHandle.z+ 0)    +" {:.6f}f".format(-arm_R_ikHandle.y+ 0)   +" );\n"  #no switch	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_R_target01"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(arm_R_ikHandle.x+ 0)    +" {:.6f}f,".format(arm_R_ikHandle.z+ 0)    +" {:.6g}f".format(-arm_R_ikHandle.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(arm_R_ikHandle.x+ 0)    +" {:.6f}f,".format(arm_R_ikHandle.z+ 0)    +" {:.6g}f".format(-arm_R_ikHandle.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	#arm_R_locator	
	#
	fingers_average_location = Vector((0,0,0))
	fingers_names = ["_finger01_R_joint01","_finger02_R_joint01","_finger03_R_joint01","_finger04_R_joint01", "_finger05_R_joint01", "_finger01_R_joint02", "_finger02_R_joint02","_finger03_R_joint02","_finger04_R_joint02","_finger05_R_joint02"]
	for finger in fingers_names:
		fingers_average_location += bpy.data.objects[finger].matrix_world.translation

	fingers_average_location = fingers_average_location / len(fingers_names)
	difference = fingers_average_location - wrist_R_joint.matrix_world.to_translation() 
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_R_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(difference.x+ 0)    +" {:.6f}f,".format(difference.z+ 0)    +" {:.6g}f".format(-difference.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	# arm_R_base_locator
	# I think arm_R_offset_locator moves in the center of palm, then it rotates then returns back to wrist loc
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_R_base_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(-difference.x+ 0)    +" {:.6f}f,".format(-difference.z+ 0)    +" {:.6g}f".format(difference.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.Rotation ( 0f, 0f, 180f );\n"
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	#wrist_R_joint_orientConstraint1.OrientOffset
	wrist_fake_joint_R = bpy.data.objects[ "_wrist_fake_joint_R"]
	snippet = ":Person\" + :person + \"Anim:Model01:wrist_R_joint_orientConstraint1.OrientOffset ("         +" {:.6f}f,".format(degrees(wrist_fake_joint_R.rotation_euler.y)+ 0)    +" {:.6f}f,".format(degrees(wrist_fake_joint_R.rotation_euler.z)+ 0)    +" {:.6g}f".format(degrees(wrist_fake_joint_R.rotation_euler.x)+ 0)   +" );\n"   #here we switch to y z x	
	snippet = snippet+ "\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#arm_R_ikHandle
	# this should be maybe all zero ?!??
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_R_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(0)    +" {:.6f}f,".format(0)    +" {:.6g}f".format(0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#	
	#
	#Selbow_R_group
	##=new code, now we calculate elbow manipulator based on empty _arm_pole_R
	calculated_elbow_R_group_world_coordinates = bpy.data.objects["_arm_pole_R"].matrix_world.to_translation()
	calculated_elbow_R_group_local_coord = neck_joint01_translated.matrix_world.inverted() * calculated_elbow_R_group_world_coordinates
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"elbow_R_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(calculated_elbow_R_group_local_coord.y+ 0)    +" {:.6f}f,".format(calculated_elbow_R_group_local_coord.z+ 0)    +" {:.6f}f".format(calculated_elbow_R_group_local_coord.x+ 0)   +" );\n"   #here we switch to xz -y	
	#we also need to do RotationPivotTranslation ... 
	#but if we calculated above correctly, then there should be no requirements for RotationPivotTranslation
	snippet = snippet+ "\t.RotationPivotTranslation ("        +" {:.6f}f,".format(0)    +" {:.6f}f,".format(0)    +" {:.6f}f".format(0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	#ellbow_R_locator
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ellbow_R_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(calculated_elbow_R_group_local_coord.y+ 0)    +" {:.6f}f,".format(calculated_elbow_R_group_local_coord.z+ 0)    +" {:.6f}f".format(calculated_elbow_R_group_local_coord.x+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#
	#
	#
	#
	#
	#
	#
	wrist_L_joint = bpy.data.objects[ "_wrist_L_joint"]
	forearm_L_joint = bpy.data.objects[ "_forearm_L_joint"]
	elbow_L_joint = bpy.data.objects[ "_elbow_L_joint"]
	arm_L_ikEffector,arm_L_ikHandle = getIKValues("Armature","elbow_joint.L","wrist_joint.L")
	arm_L_ikEffector,arm_L_ikHandle, distance,translationAlongY = getClosestPointFromBoneProjection("Armature","elbow_joint.L","wrist_joint.L")
	localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection("Armature","forearm_joint.L","wrist_joint.L")
	wrist_L_joint_world_coordinates = wrist_L_joint.matrix_world.to_translation()
	arm_effector = elbow_L_joint.matrix_world.inverted() * wrist_L_joint_world_coordinates
	#
	#arm_L_effector
	#the value should be negative, first number should be negative it seems
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_L_effector"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-translationAlongY.x+ 0)    +" {:.6g}f,".format(translationAlongY.y+ 0)    +" {:.6g}f".format(translationAlongY.z + 0)   +" );\n"  #no switch	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-translationAlongY.x+ 0)    +" {:.6g}f,".format(translationAlongY.y+ 0)    +" {:.6g}f".format(translationAlongY.z + 0)   +" );\n"  #no switch	
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(forearm_L_joint.location.y+ 0)    +" {:.6f}f,".format(forearm_L_joint.location.z+ 0)    +" {:.6g}f".format(forearm_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string = arms_fix_string+"\n"
	#arm_L_group depends on hand_L_target01_locator_parent because it has a constraint reparent on it
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_L_target01_locator_parent"
	snippet = snippet + ".SNode? . {\n";
	#snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().x+ 0)    +" {:.6f}f,".format(wrist_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-wrist_L_joint.matrix_world.to_translation().y+ 0)   +" );\n"  #here we switch to xz -y	(daz to villa)
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(arm_L_ikHandle.x+ 0)    +" {:.6f}f,".format(arm_L_ikHandle.z+ 0)    +" {:.6f}f".format(-arm_L_ikHandle.y+ 0)   +" );\n"  #no switch	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"hand_L_target01"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(arm_L_ikHandle.x+ 0)    +" {:.6f}f,".format(arm_L_ikHandle.z+ 0)    +" {:.6g}f".format(-arm_L_ikHandle.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(arm_L_ikHandle.x+ 0)    +" {:.6f}f,".format(arm_L_ikHandle.z+ 0)    +" {:.6g}f".format(-arm_L_ikHandle.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#
	#arm_L_locator	
	#
	fingers_average_location = Vector((0,0,0))
	fingers_names = ["_finger01_L_joint01","_finger02_L_joint01","_finger03_L_joint01","_finger04_L_joint01", "_finger05_L_joint01", "_finger01_L_joint02", "_finger02_L_joint02","_finger03_L_joint02","_finger04_L_joint02","_finger05_L_joint02"]
	for finger in fingers_names:
		fingers_average_location += bpy.data.objects[finger].matrix_world.translation

	fingers_average_location = fingers_average_location / len(fingers_names)
	difference = fingers_average_location - wrist_L_joint.matrix_world.to_translation() 
	bpy.context.scene.cursor_location = fingers_average_location
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_L_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(difference.x+ 0)    +" {:.6f}f,".format(difference.z+ 0)    +" {:.6g}f".format(difference.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.Rotation ( 0f, 180f, 0f );\n"
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	# arm_L_base_locator
	# I think arm_L_offset_locator moves in the center of palm, then it rotates then returns back to wrist loc
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_L_base_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(difference.x+ 0)    +" {:.6f}f,".format(-difference.z+ 0)    +" {:.6g}f".format(difference.y+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	#wrist_L_joint_orientConstraint1.OrientOffset
	wrist_fake_joint_L = bpy.data.objects[ "_wrist_fake_joint_L"]
	snippet = ":Person\" + :person + \"Anim:Model01:wrist_L_joint_orientConstraint1.OrientOffset ("         +" {:.6f}f,".format(-degrees(wrist_fake_joint_L.rotation_euler.y)+ 0)    +" {:.6f}f,".format(-degrees(wrist_fake_joint_L.rotation_euler.z)+ 0)    +" {:.6g}f".format(degrees(wrist_fake_joint_L.rotation_euler.x)+ 0)   +" );\n"   #here we switch to y z x	
	snippet = snippet+ "\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#arm_L_ikHandle
	# this should be maybe all zero ?!??
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"arm_L_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(0)    +" {:.6f}f,".format(0)    +" {:.6g}f".format(0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#	
	#
	#Selbow_L_group
	##=new code, now we calculate elbow manipulator based on empty _arm_pole_L
	calculated_elbow_L_group_world_coordinates = bpy.data.objects["_arm_pole_L"].matrix_world.to_translation()
	calculated_elbow_L_group_local_coord = neck_joint01_translated.matrix_world.inverted() * calculated_elbow_L_group_world_coordinates
	#
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"elbow_L_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(calculated_elbow_L_group_local_coord.y+ 0)    +" {:.6f}f,".format(calculated_elbow_L_group_local_coord.z+ 0)    +" {:.6f}f".format(calculated_elbow_L_group_local_coord.x+ 0)   +" );\n"   #here we switch to xz -y	
	#we also need to do RotationPivotTranslation ... 
	#but if we calculated above correctly, then there should be no requirements for RotationPivotTranslation
	snippet = snippet+ "\t.RotationPivotTranslation ("        +" {:.6f}f,".format(0)    +" {:.6f}f,".format(0)    +" {:.6f}f".format(0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"	
	#	
	#ellbow_L_locator
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ellbow_L_locator"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(calculated_elbow_L_group_local_coord.y+ 0)    +" {:.6f}f,".format(calculated_elbow_L_group_local_coord.z+ 0)    +" {:.6f}f".format(calculated_elbow_L_group_local_coord.x+ 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	arms_fix_string = arms_fix_string+snippet
	arms_fix_string=arms_fix_string + "\n"		
	#
	print (arms_fix_string)
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(arms_fix_string)
	f.flush()
	f.close()

#def export_arms_ikhandle_fix():
#	# we dont do much here...
#	#


