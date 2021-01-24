import os
import bpy
import mathutils
from math import radians
from math import degrees
from .dictionaries import *

def remove_fake_bones():
	_fakes = bpy.data.objects.get("_fakes")
	if _fakes:
		print ("_fakes found in scene")
		objs = bpy.data.objects
		for child in _fakes.children:
			objs.remove(objs[child.name], do_unlink=True)
		objs.remove(objs[_fakes.name], do_unlink=True)
	#
	armature = bpy.context.scene.objects['Armature']
	if armature:
		for pose_bone in armature.pose.bones:
			pose_bone.custom_shape = None
			pose_bone.use_custom_shape_bone_size = False



	

def add_fake_bones():
	if bpy.data.objects.get("Armature") is None:
		ShowMessageBox("Can't find object: Armature", "Error", 'ERROR')
		return None
	#
	armature_object = bpy.data.objects.get("Armature")
	armature_object.select = True
	bpy.context.scene.objects.active = armature_object
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	armature_object.select = True
	bpy.context.scene.objects.active = armature_object
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	boneSizeDict = {}  
	boneFlippedDict = {} 
	#we need to save edit bone length in boneSizeDict
	for editBone in bpy.data.armatures['Armature'].edit_bones:
		boneName = editBone.name
		boneSizeDict[boneName] = editBone.length
		if editBone.get("isFlipped") is not None and editBone["isFlipped"] == True :
			boneFlippedDict[boneName] = True
		else:
			boneFlippedDict[boneName] = False
		print( boneName )
		#
	#
	#bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	#print(bpy.context.space_data.text.filepath)
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	script_file = os.path.realpath(__file__)
	directory = os.path.dirname(script_file)
	print(directory)
	path_to_file = os.path.join(directory, "rhomb_bone.obj")
	bpy.ops.import_scene.obj(filepath = path_to_file,split_mode='OFF')
	imported = bpy.context.selected_objects[0]
	print(imported.name)
	scn = bpy.context.scene
	parent = bpy.data.objects.new( "_fakes", None )
	scn.objects.link(parent)
	print("--------------------------")
	print("--------------------------")
	print("--------------------------")
	for key in sorted(boneSizeDict.keys()):
		print (key, boneSizeDict[key])
		src_obj = bpy.data.objects[imported.name]
		new_obj = src_obj.copy()
		new_obj.data = src_obj.data.copy()
		new_obj.name = "cone_"+key
		new_obj.data.name = "cone_"+key
		new_obj.scale = new_obj.scale * boneSizeDict[key]
		new_obj["scale"] = new_obj.scale
		new_obj["localTJoint"] = joint_to_local_dict[ctkToVillaDict[key]]
		new_obj.parent = parent
		scn.objects.link(new_obj)
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.scene.objects.active = new_obj
		new_obj.select = True	
		new_obj.rotation_euler.z= radians(90)
		bpy.ops.object.transform_apply(rotation = True)		
		if boneFlippedDict[key] == True :
			new_obj.rotation_euler.y= radians(180)
			bpy.ops.object.transform_apply(rotation = True)
			new_obj["isFlipped"] = True 
		bpy.ops.object.transform_apply(scale = True)
		#
	#
	# Deselect all
	bpy.ops.object.select_all(action='DESELECT')
	imported.select = True    # Blender 2.7x
	bpy.ops.object.delete() 
	#bpy.data.objects["Armature"].pose.bones["hip_joint.L"].custom_shape
	armature = bpy.context.scene.objects['Armature']
	for pose_bone in armature.pose.bones:
		pose_bone.custom_shape = bpy.data.objects["cone_"+pose_bone.name]
		pose_bone.use_custom_shape_bone_size = False
	









