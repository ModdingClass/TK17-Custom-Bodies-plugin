import bpy
import mathutils
from math import radians
from math import degrees
from .dictionaries import *
from .tools_message_box import *

def fix_rolls(armature_object):
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	if (armature_object.rotation_euler.x!=0 or armature_object.rotation_euler.y!=0 or armature_object.rotation_euler.z!=0):
		print("Armature has a rotation applied, fix that first")
		ShowMessageBox("Armature has a rotation applied, fix that first", "Error", 'ERROR')
		return None
	armature_object.rotation_euler.z= radians(-270)
	armature_object.select = True
	bpy.context.scene.objects.active = armature_object
	bpy.ops.object.transform_apply(rotation = True)
	armature_object.rotation_euler.z= radians(-90)
	armature_object.select = True
	#NEGATIVE_X
	#POSITIVE_X
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	ebones = bpy.data.armatures[armature_object.data.name].edit_bones
	#
	bpy.ops.armature.select_all(action="DESELECT")
	legSymmetryList={
	'hip_L_joint' : 	'hip_R_joint', 
	'knee_L_joint' : 	'knee_R_joint', 
	'ankle_L_joint' : 	'ankle_R_joint', 
	'ball_L_joint' : 	'ball_R_joint', 
	'toe_deform01_L_joint01' : 	'toe_deform01_R_joint01', 
	'toe_deform01_L_jointEnd' : 	'toe_deform01_R_jointEnd', 
	'toe_deform02_L_joint01' : 	'toe_deform02_R_joint01', 
	'toe_deform02_L_jointEnd' : 	'toe_deform02_R_jointEnd', 
	'toe_L_joint' : 	'toe_R_joint'
	}
	for key in legSymmetryList:
		print(key, '->', legSymmetryList[key])
		print(villaToCtkDict[key], '->', villaToCtkDict[legSymmetryList[key]])
		ebones[villaToCtkDict[legSymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#	
	bpy.ops.armature.select_all(action="DESELECT")
	armSymmetryList={
	'clavicle_R_joint' : 	'clavicle_L_joint', 
	'elbow_R_joint' : 	'elbow_L_joint', 
	'finger01_R_joint01' : 	'finger01_L_joint01', 
	'finger01_R_joint02' : 	'finger01_L_joint02', 
	'finger01_R_joint03' : 	'finger01_L_joint03', 
	'finger01_R_jointEnd' : 	'finger01_L_jointEnd', 
	'finger02_R_joint01' : 	'finger02_L_joint01', 
	'finger02_R_joint02' : 	'finger02_L_joint02', 
	'finger02_R_joint03' : 	'finger02_L_joint03', 
	'finger02_R_joint04' : 	'finger02_L_joint04', 
	'finger02_R_jointEnd' : 	'finger02_L_jointEnd', 
	'finger03_R_joint01' : 	'finger03_L_joint01', 
	'finger03_R_joint02' : 	'finger03_L_joint02', 
	'finger03_R_joint03' : 	'finger03_L_joint03', 
	'finger03_R_joint04' : 	'finger03_L_joint04', 
	'finger03_R_jointEnd' : 	'finger03_L_jointEnd', 
	'finger04_R_joint01' : 	'finger04_L_joint01', 
	'finger04_R_joint02' : 	'finger04_L_joint02', 
	'finger04_R_joint03' : 	'finger04_L_joint03', 
	'finger04_R_joint04' : 	'finger04_L_joint04', 
	'finger04_R_jointEnd' : 	'finger04_L_jointEnd', 
	'finger05_R_joint01' : 	'finger05_L_joint01', 
	'finger05_R_joint02' : 	'finger05_L_joint02', 
	'finger05_R_joint03' : 	'finger05_L_joint03', 
	'finger05_R_joint04' : 	'finger05_L_joint04', 
	'finger05_R_jointEnd' : 	'finger05_L_jointEnd', 
	'forearm_R_joint' : 	'forearm_L_joint', 
	'shoulder_R_joint' : 	'shoulder_L_joint', 
	'wrist_R_joint' : 	'wrist_L_joint', 
	}
	for key in armSymmetryList:
		print(key, '->', armSymmetryList[key])
		ebones[villaToCtkDict[armSymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#
	bpy.ops.armature.select_all(action="DESELECT")
	breast_L_SymmetryList={
	'breast_deform01_L_joint01' : 	'breast_deform01_R_joint01', 		
	'breast_deform01_L_jointEnd' : 	'breast_deform01_R_jointEnd', 		
	'breast_deform02_L_joint01' : 	'breast_deform02_R_joint01', 		
	'breast_deform02_L_jointEnd' : 	'breast_deform02_R_jointEnd', 		
	'breast_deform03_L_joint01' : 	'breast_deform03_R_joint01', 		
	'breast_deform03_L_jointEnd' : 	'breast_deform03_R_jointEnd'
	}
	for key in breast_L_SymmetryList:
		print(key, '->', breast_L_SymmetryList[key])
		ebones[villaToCtkDict[breast_L_SymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#
	bpy.ops.armature.select_all(action="DESELECT")
	breast_R_SymmetryList={
	'breast_R_joint' : 	'breast_L_joint', 		
	'breast_scale_R_joint' : 	'breast_scale_L_joint', 		
	'nipple_R_joint01' : 	'nipple_L_joint01', 		
	'nipple_R_jointEnd' : 	'nipple_L_jointEnd', 		
	}
	for key in breast_R_SymmetryList:
		print(key, '->', breast_R_SymmetryList[key])
		ebones[villaToCtkDict[breast_R_SymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#
	bpy.ops.armature.select_all(action="DESELECT")
	face_SymmetryList={
	'cheek_L_joint01' : 	'cheek_R_joint01', 
	'cheek_L_jointEnd' : 	'cheek_R_jointEnd', 
	'ear_L_joint01' : 	'ear_R_joint01', 
	'ear_L_jointEnd' : 	'ear_R_jointEnd', 
	'eye_brow_L_joint01' : 	'eye_brow_R_joint01', 
	'eye_brow_L_joint02' : 	'eye_brow_R_joint02', 
	'eye_brow_L_jointEnd' : 	'eye_brow_R_jointEnd', 
	'eye_L_joint' : 	'eye_R_joint', 
	'eye_socket_L_joint' : 	'eye_socket_R_joint', 
	'lower_lip_L_joint01' : 	'lower_lip_R_joint01', 
	'lower_lip_L_joint02' : 	'lower_lip_R_joint02', 
	'lower_lip_L_joint03' : 	'lower_lip_R_joint03', 
	'lower_lip_L_jointEnd' : 	'lower_lip_R_jointEnd', 
	'upper_lip_L_joint01' : 	'upper_lip_R_joint01', 
	'upper_lip_L_joint02' : 	'upper_lip_R_joint02', 
	'upper_lip_L_joint03' : 	'upper_lip_R_joint03', 
	'upper_lip_L_jointEnd' : 	'upper_lip_R_jointEnd'
	}
	for key in face_SymmetryList:
		print(key, '->', face_SymmetryList[key])
		ebones[villaToCtkDict[face_SymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#
	bpy.ops.armature.select_all(action="DESELECT")
	vagina_SymmetryList={
	'vagina_R_joint01': 	'vagina_L_joint01', 
	'vagina_R_jointEnd':	'vagina_L_jointEnd'
	}
	for key in vagina_SymmetryList:
		print(key, '->', vagina_SymmetryList[key])
		ebones[villaToCtkDict[vagina_SymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#
	bpy.ops.armature.select_all(action="DESELECT")
	extra_L_SymmetryList={
	'butt_L_joint01': 	'butt_R_joint01',
	'butt_L_jointEnd': 	'butt_R_jointEnd', 
	#'rib_L_joint01': 	"????",
	'rib_L_jointEnd': 	'rib_R_jointEnd'
	}
	for key in extra_L_SymmetryList:
		print(key, '->', extra_L_SymmetryList[key])
		ebones[villaToCtkDict[extra_L_SymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#
	bpy.ops.armature.select_all(action="DESELECT")
	extra_R_SymmetryList={
	#'butt_R_joint01': 	"????",
	#'rib_R_joint01': 	"????",
	}
	for key in extra_R_SymmetryList:
		print(key, '->', extra_R_SymmetryList[key])
		ebones[villaToCtkDict[extra_R_SymmetryList[key]]].roll = radians(180 + degrees(ebones[villaToCtkDict[key]].roll))
	#
	#hardcode fix for butt_R_joint01
	ebones[villaToCtkDict['butt_R_joint01']].roll = ebones[villaToCtkDict['butt_L_joint01']].roll
	#centered_bones_list = ['root', 'anus_joint', 'penis_joint01', 'penis_joint02', 'penis_joint03', 'penis_jointEnd', 'spine_joint01', 'spine_joint02', 'spine_joint03', 'spine_joint04', 'spine_jointEnd', 'neck_joint01', 'neck_jointEnd', 'head_joint01', 'head_joint02', 'forehead_joint01', 'forehead_jointEnd', 'head_jointEnd', 'lower_jaw_joint01', 'lower_jaw_jointEnd', 'chin_joint01', 'chin_jointEnd', 'nose_joint01', 'nose_joint02', 'nose_jointEnd', 'stomach_joint01', 'stomach_jointEnd', 'testicles_joint01', 'testicles_joint02', 'testicles_jointEnd']
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	#final cleanup
	bpy.ops.object.select_all(action='DESELECT')
	armature_object.select = True    # Blender 2.7x
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	#bpy.ops.object.delete() 
	#bpy.ops.object.select_all(action='DESELECT')
	#armature_object = bpy.data.objects["Armature"]
	#armature_object = bpy.context.active_object
	#armature_object.select = True



