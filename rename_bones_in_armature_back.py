import bpy
import mathutils
from .dictionaries import *

def rename_bones_back():
	#Make a coding shortcut
	armature_data = bpy.data.objects['Armature']
	#Must make armature active and in edit mode to create a bone
	bpy.context.scene.objects.active = armature_data
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	#
	armature_matrix_world = armature_data.matrix_world
	#
	my_bones = [] 
	def print_heir(ob, levels=50):
		def recurse(ob, parent, depth):
			if depth > levels: 
				return
			#print("  " * depth, ob.name)
			my_bones.append(ob)
			for child in ob.children:
				recurse(child, ob,  depth + 1)
		recurse(ob, ob.parent, 0)
	#
	#
	#
	#
	parentBone = bpy.data.armatures['Armature'].edit_bones["root"]
	print_heir(parentBone)
	#
	for bone in my_bones:
		if ctkToVillaDict.get(bone.name) != None:
			bone.name = ctkToVillaDict[bone.name]
		
	
#
#
#
		










