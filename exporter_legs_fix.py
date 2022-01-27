import sys
import os
from math import radians
from math import degrees
from os.path import join

from .ik_tools import *
from .dictionaries import *
import math
from mathutils import Vector
from mathutils import Matrix
from mathutils.geometry import intersect_point_line

#//	Object.Name "Model01:knee_LClips1__knee_L_initSource";
#//var :mySplineVector3f :Person" + :person + "Anim:Model01:leg_LClips1__leg_L_initSource.Curve[1] ?;
#//:mySplineVector3f.KeyValue [ (0.9113f, 0f, -0.095f), (0.9113f, 0f, -0.095f)];

#Model01:Sleg_L_ikEffector ->Sankle_L_joint



def export_legs_fix(exportfolderpath, bodyNo):
	#
	#
	legs_fix_string = "";
	#
	leg_init_L = Vector ((0.113, 0, -0.095))
	generic_x = 0.000168;
	knee_offset = 0.40407172;
	#tip_offset = 0.14387479;
	#
	toe_L_joint = bpy.data.objects[ "_toe_L_joint"]
	ball_L_joint = bpy.data.objects[ "_ball_L_joint"]
	knee_L_joint = bpy.data.objects[ "_knee_L_joint"]
	ankle_L_joint = bpy.data.objects[ "_ankle_L_joint"]
	#leg_target_L_joint = bpy.data.objects[ "_leg_target_L"]
	#
	#leg_LClips1__leg_L_initSource
	line_b = bpy.data.objects[ "_knee_L_joint"].matrix_world.to_translation()
	# we move it along local Y axis, get the moved vector then move it back to original location
	bpy.data.objects[ "_knee_L_joint"].matrix_basis *= Matrix.Translation((0.0, 10.0, 0.0))
	#for some reason we need to update the scene, otherwise the matrix wont work
	bpy.context.scene.update()
	line_a = bpy.data.objects[ "_knee_L_joint"].matrix_world.to_translation()
	bpy.data.objects[ "_knee_L_joint"].matrix_basis *= Matrix.Translation((0.0, -10.0, 0.0))
	bpy.context.scene.update()
	#
	plane_co = Vector ((0,0,0))# bpy.data.objects[ "_shoulder_L_joint"].matrix_world.to_translation()
	plane_no = Vector ((0,0,-1))
	calculated_intersection = mathutils.geometry.intersect_line_plane(line_b, line_a, plane_co, plane_no)
	leg_init_L = calculated_intersection
	#leg_init_L = Vector ( (calculated_intersection.x,calculated_intersection.z, -calculated_intersection.y) )
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:leg_LClips1__leg_L_initSource.Curve[1] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(leg_init_L.x + 0)    +" {:.6g}f,".format(leg_init_L.z  + 0)    +" {:.6g}f".format(-leg_init_L.y  + 0)   +" )" #x z -y
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#	
	#
	leg_L_ikEffector,leg_L_ikHandle = getIKValues("Armature","knee_joint.L","ankle_joint.L")
	ball_L_ikEffector,tiptoe_L_ikHandle = getIKValues("Armature","ankle_joint.L","ball_joint.L")
	toe_L_ikEffector,tiptoe_L_rotation_ikHandle = getIKValues("Armature","ball_joint.L","toe_joint.L")
	#
	#
	#
	#
	""" armature_object = bpy.context.scene.objects["Armature"]
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	ob = armature_object
	armature = ob.data    
	bone_ball_joint = ob.data.edit_bones["ball_joint.L"] # ball_joint.L   
	bone_ankle_joint= ob.data.edit_bones["ankle_joint.L"] # ankle_joint.L
	line_a = bone_ankle_joint.head
	line_b = bone_ankle_joint.tail
	plane_co = bone_ball_joint.head
	plane_no = bone_ball_joint.z_axis
	result = mathutils.geometry.intersect_line_plane(line_a, line_b, plane_co, plane_no, False)
	difference = result - bone_ankle_joint.head
	result_world = ob.matrix_world * result """

	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	legs_fix_string=legs_fix_string + "\n"
	#effector leg_L_ikEffector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"leg_L_ikEffector"
	snippet = snippet + ".SNode? . {\n";
	#------RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	#snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(ankle_L_joint.location.y+ 0)    +" {:.6g}f,".format(ankle_L_joint.location.z+ 0)    +" {:.6g}f".format(ankle_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(leg_L_ikEffector.x+ 0)    +" {:.6g}f,".format(leg_L_ikEffector.y+ 0)    +" {:.6g}f".format(leg_L_ikEffector.z+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string = legs_fix_string + "\n"
	#effector ball_L_ikEffector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ball_L_ikEffector"
	snippet = snippet + ".SNode? . {\n";
	#------RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	#snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(ball_L_joint.location.y+ 0)    +" {:.6g}f,".format(ball_L_joint.location.z+ 0)    +" {:.6g}f".format(ball_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(ball_L_ikEffector.x+ 0)    +" {:.6g}f,".format(ball_L_ikEffector.y+ 0)    +" {:.6g}f".format(ball_L_ikEffector.z+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string = legs_fix_string + "\n"	
	#effector toe_L_ikEffector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"toe_L_ikEffector"
	snippet = snippet + ".SNode? . {\n";
	#------RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	#snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(toe_L_joint.location.y+ 0)    +" {:.6g}f,".format(toe_L_joint.location.z+ 0)    +" {:.6g}f".format(toe_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(toe_L_ikEffector.x+ 0)    +" {:.6g}f,".format(toe_L_ikEffector.y+ 0)    +" {:.6g}f".format(toe_L_ikEffector.z+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string = legs_fix_string + "\n"	
	#knee_L_group
	knee_pole_L = bpy.data.objects[ "_knee_pole_L"]
	pivot_corrected = knee_pole_L.location - leg_init_L
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"knee_L_group"
	snippet = snippet + ".SNode? . {\n";
	#snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(knee_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" );\n"   #here we switch to xz -y	
	#snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(knee_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#
	#tiptoe_L_rotation_group OK
	#leg_init_L = Vector ((0.113, 0, -0.095))
	#pivot_local = Vector( (ball_L_joint.matrix_world.to_translation().x, ball_L_joint.matrix_world.to_translation().z, -ball_L_joint.matrix_world.to_translation().y) ) #here we switch to xz -y
	#pivot_local = Vector( (tiptoe_L_ikHandle.x, tiptoe_L_ikHandle.z, -tiptoe_L_ikHandle.y) ) #here we switch to xz -y	
	#pivot_corrected = pivot_local - leg_init_L
	pivot_corrected = tiptoe_L_ikHandle - leg_init_L
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_L_rotation_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#	
	#ball_L_group OK
	#same values as tiptoe_L_rotation_group ?!? 
	#pivot_local = Vector( (ball_L_joint.matrix_world.to_translation().x, ball_L_joint.matrix_world.to_translation().z, -ball_L_joint.matrix_world.to_translation().y) ) #here we switch to xz -y
	#pivot_local = Vector( (tiptoe_L_ikHandle.x, tiptoe_L_ikHandle.z, -tiptoe_L_ikHandle.y) ) #here we switch to xz -y	
	#pivot_corrected = pivot_local - leg_init_L
	pivot_corrected = tiptoe_L_ikHandle - leg_init_L
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ball_L_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#
	#tiptoe_L_rotation_ikHandle OK
	#pivot_local = Vector( (toe_L_joint.matrix_world.to_translation().x, toe_L_joint.matrix_world.to_translation().z, -toe_L_joint.matrix_world.to_translation().y) ) #here we switch to xz -y
	#pivot_local = Vector( (tiptoe_L_rotation_ikHandle.x, tiptoe_L_rotation_ikHandle.z, -tiptoe_L_rotation_ikHandle.y) ) #here we switch to xz -y	
	#pivot_corrected = pivot_local - leg_init_L	
	pivot_corrected = tiptoe_L_rotation_ikHandle - leg_init_L
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_L_rotation_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   
	ikEffector = bpy.data.objects[ "_toe_L_ikEffector"]
	move_down_transformation_local =    Vector([0,0,-0.2]) #+ikEffector.location 
	move_down_transformation_world = ikEffector.matrix_world.to_3x3() * move_down_transformation_local
	pole_world_location = ikEffector.matrix_world.translation + move_down_transformation_world
	#bpy.context.scene.cursor_location = ikEffector.matrix_world.translation
	#difference = pole_world_location  - ikEffector.matrix_world.translation
	#difference = move_down_transformation_world.x, 
	#pole will have values transformed from Blender coordinates to in game coordinates
	pole = Vector ( (move_down_transformation_world.x, move_down_transformation_world.z, - move_down_transformation_world.y))
	#pole = move_down_transformation_world_ingame ##move_down_transformation_world - ikEffector.matrix_world.translation #- leg_init_L #pole_world_location - leg_init_L
	snippet = snippet+ "\t.PoleVector ("		+" {:.6g}f,".format(pole.x + 0)    +" {:.6g}f,".format(pole.y + 0)    +" {:.6g}f".format(pole.z + 0)   +" );\n"   				
	#snippet = snippet+ "\t.PoleVector ("   ///////some values here     +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.y + 0)    +" {:.6g}f".format(pivot_corrected.z + 0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#
	#tip_toe_L_group
	#same pivot as tiptoe_L_rotation_ikHandle ?!?
	#pivot_local = Vector( (toe_L_joint.matrix_world.to_translation().x, toe_L_joint.matrix_world.to_translation().z, -toe_L_joint.matrix_world.to_translation().y) ) #here we switch to xz -y
	#pivot_local = Vector( (tiptoe_L_rotation_ikHandle.x, tiptoe_L_rotation_ikHandle.z, -tiptoe_L_rotation_ikHandle.y) ) #here we switch to xz -y	
	#pivot_corrected = pivot_local - leg_init_L		
	pivot_corrected = tiptoe_L_rotation_ikHandle - leg_init_L	
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tip_toe_L_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#
	#tiptoe_L_ikHandle
	#pivot matches ball_L_joint position in world space somewhere in front of the leg
	#pivot_local = Vector( (ball_L_joint.matrix_world.to_translation().x, ball_L_joint.matrix_world.to_translation().z, -ball_L_joint.matrix_world.to_translation().y) ) #here we switch to xz -y
	#pivot_local = Vector( (tiptoe_L_ikHandle.x, tiptoe_L_ikHandle.z, -tiptoe_L_ikHandle.y) ) #here we switch to xz -y	
	#pivot_corrected = pivot_local - leg_init_L	
	pivot_corrected = tiptoe_L_ikHandle - leg_init_L	
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_L_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   
	#snippet = snippet+ "\t.PoleVector ("   ///////some values here     +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.y + 0)    +" {:.6g}f".format(pivot_corrected.z + 0)   +" );\n"   	
	#pole_world_location = Vector ((0.043439, -0.897665, -0.317079))
	pole_world_location = Vector ((0.043439, 0.317079, -0.897665))
	#pole_corrected = pole_world_location - pivot_local
	pole_corrected = pole_world_location - tiptoe_L_ikHandle
	snippet = snippet+ "\t.PoleVector ("		+" {:.6g}f,".format(pole_corrected.x + 0)    +" {:.6g}f,".format(pole_corrected.z + 0)    +" {:.6g}f".format(-pole_corrected.y + 0)   +" );\n"   		
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#	
	#leg_L_ikHandle
	#pivot matches head ankle_L_joint position in world space
	#pivot_local = Vector( (ankle_L_joint.matrix_world.to_translation().x, ankle_L_joint.matrix_world.to_translation().z, -ankle_L_joint.matrix_world.to_translation().y) ) #here we switch to xz -y
	#pivot_local = Vector( (leg_L_ikHandle.x, leg_L_ikHandle.z, -leg_L_ikHandle.y) ) #here we switch to xz -y	
	#pivot_corrected = pivot_local - leg_init_L		
	pivot_corrected = leg_L_ikHandle - leg_init_L		
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"leg_L_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	#RK: SSimpleTransform. (SIKHandle) Your SIKHandle should use the same parameter (rotation, translation, pivot, etc.) as the one used by the transform node connected to the TNode.Parent (TIKHandle) node. If it do not contain any, it's mean that your SIKHandle only need a Object.Name parameter.
	#in this case Model01:Sball_L_group
	#but maybe RK was wrong, need to check again??!
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z + 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" );\n"   
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#
	#knee_LClips1__knee_L_initSource
	leg_pole_L = bpy.data.objects[ "_leg_pole_L"]
	leg_pole_L_location = leg_pole_L.matrix_world.to_translation()
	#pivot_local = Vector( (leg_pole_L_location.x, leg_pole_L_location.z, -leg_pole_L_location.y) ) #here we switch to xz -y	
	pivot_corrected = leg_pole_L_location - leg_init_L		
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:knee_LClips1__knee_L_initSource.Curve[0] ?;"
	#mySplineVectorString = "("+" {:.6g}f,".format(generic_x - generic_x+ 0)    +" {:.6g}f,".format(knee_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" )"
	mySplineVectorString = "("+" {:.6g}f,".format(pivot_corrected.x + 0)    +" {:.6g}f,".format(pivot_corrected.z+ 0)    +" {:.6g}f".format(-pivot_corrected.y + 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#
	#
	toe_R_joint = bpy.data.objects[ "_toe_R_joint"]
	ball_R_joint = bpy.data.objects[ "_ball_R_joint"]
	knee_R_joint = bpy.data.objects[ "_knee_R_joint"]
	ankle_R_joint = bpy.data.objects[ "_ankle_R_joint"]
	legs_fix_string=legs_fix_string + "\n"
	#effector leg_R_ikEffector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"leg_R_ikEffector"
	snippet = snippet + ".SNode? . {\n";
	#Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(ankle_R_joint.location.y+ 0)    +" {:.6g}f,".format(ankle_R_joint.location.z+ 0)    +" {:.6g}f".format(ankle_R_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"
	#effector ball_R_ikEffector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ball_R_ikEffector"
	snippet = snippet + ".SNode? . {\n";
	#RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(ball_R_joint.location.y+ 0)    +" {:.6g}f,".format(ball_R_joint.location.z+ 0)    +" {:.6g}f".format(ball_R_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string = legs_fix_string + "\n"	
	#effector toe_R_ikEffector
	#snippet = ":Person\" + :person + \"Anim:Model01:"
	#snippet = snippet+"toe_R_ikEffector"
	#snippet = snippet + ".SNode? . {\n";
	#RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	#snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(toe_R_joint.location.y+ 0)    +" {:.6g}f,".format(toe_R_joint.location.z+ 0)    +" {:.6g}f".format(toe_R_joint.location.x+ 0)   +" );\n"  #no switch
	#snippet = snippet+ "};\n"
	#snippet = snippet+""
	#legs_fix_string = legs_fix_string+snippet
	#legs_fix_string = legs_fix_string + "\n"		
	#knee_R_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"knee_R_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(knee_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(knee_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#
	#tiptoe_R_rotation_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_R_rotation_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ball_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ball_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#	
	#ball_R_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ball_R_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ball_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ball_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#	
	#tiptoe_R_rotation_ikHandle
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_R_rotation_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(toe_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(toe_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#	
	#tip_toe_R_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tip_toe_R_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(toe_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(toe_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_R_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#tiptoe_R_ikHandle
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_R_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ball_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ball_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#	
	#leg_R_ikHandle
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"leg_R_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ankle_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-(ball_R_joint.matrix_world.to_translation().y+knee_R_joint.matrix_world.to_translation().y)/2 + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(ankle_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-(ball_R_joint.matrix_world.to_translation().y+knee_R_joint.matrix_world.to_translation().y)/2 + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#	
	#knee_RClips1__knee_R_initSource
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:knee_RClips1__knee_R_initSource.Curve[0] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(generic_x+ 0)    +" {:.6g}f,".format(knee_R_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#	
	#leg_RClips1__leg_R_initSource
	line_b = bpy.data.objects[ "_knee_R_joint"].matrix_world.to_translation()
	# we move it along local Y axis, get the moved vector then move it back to original location
	bpy.data.objects[ "_knee_R_joint"].matrix_basis *= Matrix.Translation((0.0, 10.0, 0.0))
	#for some reason we need to update the scene, otherwise the matrix wont work
	bpy.context.scene.update()
	line_a = bpy.data.objects[ "_knee_R_joint"].matrix_world.to_translation()
	bpy.data.objects[ "_knee_R_joint"].matrix_basis *= Matrix.Translation((0.0, -10.0, 0.0))
	bpy.context.scene.update()
	#
	plane_co = Vector ((0,0,0))# bpy.data.objects[ "_shoulder_R_joint"].matrix_world.to_translation()
	plane_no = Vector ((0,0,-1))
	calculated_intersection = mathutils.geometry.intersect_line_plane(line_b, line_a, plane_co, plane_no)
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:leg_RClips1__leg_R_initSource.Curve[1] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(calculated_intersection.x+ 0)    +" {:.6g}f,".format(calculated_intersection.z+ 0)    +" {:.6g}f".format(-calculated_intersection.y+ 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#
	knee_translation_default = [knee_L_joint.location.y, knee_L_joint.location.z, knee_L_joint.location.x, knee_R_joint.location.y, knee_R_joint.location.z, knee_R_joint.location.x]
	snippet = '\n:Person" + :person + "Anim:Model01:knee_translation_poseBlend.PoseDefault ' + str(["{:.6f}f".format(float(i)) for i in knee_translation_default])+';'	
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"
	legs_fix_string = legs_fix_string.replace("-0.000000f", "0f").replace("0.000000f", "0f").replace("-1.000000f", "-1f").replace("1.000000f", "1f").replace("'", "")
	print (legs_fix_string)
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(legs_fix_string)
	f.flush()
	f.close()

#def export_arms_ikhandle_fix():
#	# we dont do much here...
#	#

#Sknee_L_group  knee_LClips1__knee_L_initSource           Sroot_knee_target  Sknee_L_parent
#Stip_toe_R_group
#STransform :local_57060 . {
#	STransform.ScalingPivot Vector3f( -0.000168, 0.520589, 0.40407172 );
#	STransform.RotationPivot Vector3f( -0.000168, 0.520589, 0.40407172 );
#	Object.Name "Model01:Sknee_L_group";
#};


