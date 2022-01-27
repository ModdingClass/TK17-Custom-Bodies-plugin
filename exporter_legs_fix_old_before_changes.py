import sys
import os
from math import radians
from math import degrees
from os.path import join

from .dictionaries import *
import math
from mathutils import Vector
from mathutils import Matrix

#//	Object.Name "Model01:knee_LClips1__knee_L_initSource";
#//var :mySplineVector3f :Person" + :person + "Anim:Model01:leg_LClips1__leg_L_initSource.Curve[1] ?;
#//:mySplineVector3f.KeyValue [ (0.9113f, 0f, -0.095f), (0.9113f, 0f, -0.095f)];

#Model01:Sleg_L_ikEffector ->Sankle_L_joint

def export_legs_fix(exportfolderpath, bodyNo):
	#
	#
	legs_fix_string = "";
	#
	generic_x = 0.000168;
	knee_offset = 0.40407172;
	tip_offset = 0.14387479;
	#
	toe_L_joint = bpy.data.objects[ "_toe_L_joint"]
	ball_L_joint = bpy.data.objects[ "_ball_L_joint"]
	knee_L_joint = bpy.data.objects[ "_knee_L_joint"]
	ankle_L_joint = bpy.data.objects[ "_ankle_L_joint"]
	leg_target_L_joint = bpy.data.objects[ "_leg_target_L"]
	legs_fix_string=legs_fix_string + "\n"
	#effector leg_L_ikEffector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"leg_L_ikEffector"
	snippet = snippet + ".SNode? . {\n";
	#RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(ankle_L_joint.location.y+ 0)    +" {:.6g}f,".format(ankle_L_joint.location.z+ 0)    +" {:.6g}f".format(ankle_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string = legs_fix_string + "\n"
	if True == True:
		#effector leg_L_ikEffector
		snippet = ":Person\" + :person + \"Anim:Model01:"
		snippet = snippet+"leg_L_ikEffector"
		snippet = snippet + ".SNode? . {\n";
		#RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
		snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(leg_target_L_joint.location.y+ 0)    +" {:.6g}f,".format(leg_target_L_joint.location.z+ 0)    +" {:.6g}f".format(leg_target_L_joint.location.x+ 0)   +" );\n"  #no switch
		snippet = snippet+ "};\n"
		snippet = snippet+""
		legs_fix_string = legs_fix_string+snippet
		legs_fix_string = legs_fix_string + "\n"
	#effector ball_L_ikEffector
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ball_L_ikEffector"
	snippet = snippet + ".SNode? . {\n";
	#RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(ball_L_joint.location.y+ 0)    +" {:.6g}f,".format(ball_L_joint.location.z+ 0)    +" {:.6g}f".format(ball_L_joint.location.x+ 0)   +" );\n"  #no switch
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string = legs_fix_string + "\n"	
	#effector toe_L_ikEffector
	#snippet = ":Person\" + :person + \"Anim:Model01:"
	#snippet = snippet+"toe_L_ikEffector"
	#snippet = snippet + ".SNode? . {\n";
	#RK: Must use the same value than the one used by the joint linked to the TIKEffector.TranslationLink parameter. (check the sjoint of it) If the sjoint do not contain any... this mean that the translation = (0, 0, 0) and that your didn't follow the rule!
	#snippet = snippet+ "\t.Translation ("        +" {:.6g}f,".format(toe_L_joint.location.y+ 0)    +" {:.6g}f,".format(toe_L_joint.location.z+ 0)    +" {:.6g}f".format(toe_L_joint.location.x+ 0)   +" );\n"  #no switch
	#snippet = snippet+ "};\n"
	#snippet = snippet+""
	#legs_fix_string = legs_fix_string+snippet
	#legs_fix_string = legs_fix_string + "\n"	
	#knee_L_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"knee_L_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(knee_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(knee_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#
	#tiptoe_L_rotation_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_L_rotation_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ball_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ball_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#	
	#ball_L_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"ball_L_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ball_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ball_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#
	#tiptoe_L_rotation_ikHandle
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_L_rotation_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(toe_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(toe_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"	
	#
	#tip_toe_L_group
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tip_toe_L_group"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(toe_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(toe_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(0.1-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#
	#tiptoe_L_ikHandle
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"tiptoe_L_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ball_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ball_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-toe_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#	
	#leg_L_ikHandle
	snippet = ":Person\" + :person + \"Anim:Model01:"
	snippet = snippet+"leg_L_ikHandle"
	snippet = snippet + ".SNode? . {\n";
	#RK: SSimpleTransform. (SIKHandle) Your SIKHandle should use the same parameter (rotation, translation, pivot, etc.) as the one used by the transform node connected to the TNode.Parent (TIKHandle) node. If it do not contain any, it's mean that your SIKHandle only need a Object.Name parameter.
	#in this case Model01:Sball_L_group
	#but maybe RK was wrong, need to check again??!
	snippet = snippet+ "\t.ScalingPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ankle_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-ball_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "\t.RotationPivot ("        +" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(ankle_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(-ball_L_joint.matrix_world.to_translation().y + 0)   +" );\n"   #here we switch to xz -y	
	snippet = snippet+ "};\n"
	snippet = snippet+""
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
	#
	#knee_LClips1__knee_L_initSource
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:knee_LClips1__knee_L_initSource.Curve[0] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(-generic_x+ 0)    +" {:.6g}f,".format(knee_L_joint.matrix_world.to_translation().z+ 0)    +" {:.6g}f".format(knee_offset + 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	legs_fix_string = legs_fix_string+snippet
	legs_fix_string=legs_fix_string + "\n"		
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
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:leg_LClips1__leg_L_initSource.Curve[1] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(calculated_intersection.x+ 0)    +" {:.6g}f,".format(calculated_intersection.z+ 0)    +" {:.6g}f".format(-calculated_intersection.y+ 0)   +" )"
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