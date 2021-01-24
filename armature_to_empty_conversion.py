#logic behind is:
#right hand is good, left leg is good, etc... (everything which is not flipped)
#but we can't symmetrize the armature because it has a -90 z rotation
#so first apply rotation, then symmetrize in groups (because we want to set right hand values to left hand and left leg to right leg : not flipped to flipped) then only then!!! check x-axis mirror 
#adjust armature to body
#remove check x-axis mirror option
#select all edit bones and rotate 90
#in object mode set rotation back to 90
#corect rolls for flipped bones (180 + value of non flipped
#now can finally export

import bpy
import mathutils
import math

from mathutils import Vector
from mathutils import Matrix
from math import radians

from .dictionaries import *
from .correct_final_rolls import *


def regenerate_empties(armature_object):
	center_list = ["spine_joint01","spine_joint02","spine_joint03","spine_joint04","spine_jointEnd","neck_joint01","neck_jointEnd","head_joint01","head_joint02","head_jointEnd"]
	#
	#
	bpy.context.scene.objects.active = armature_object
	bpy.ops.object.duplicate(linked=False)
	clone = bpy.context.scene.objects.active
	fix_rolls(clone)
	#
	#
	#Must make armature active and in edit mode to create a bone
	#bpy.context.scene.objects.active = armature_object
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	#
	armature_matrix_world = clone.matrix_world
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
	parentBone = clone.data.edit_bones["root"]
	print_heir(parentBone)
	#
	for bone in my_bones:
		#print ("bone: " + bone.name)
		ob = bpy.data.objects.new( "_"+ctkToVillaDict[bone.name], None )
		ob.rotation_mode = 'YZX'
		if bone.name != "root":
			ob.parent = bpy.data.objects[ "_"+ctkToVillaDict[bone.parent.name]]	
			print (ob.name+ " "+ob.parent.name)
		#if "wrist_joint.L" in bone.name :
		#	bone.length *= -1	
		if bone.get("isFlipped") is not None and bone["isFlipped"] == True :
			bone.length *= -1	
		ob.matrix_world = armature_matrix_world * bone.matrix		
		if bone.get("isFlipped") is not None and bone["isFlipped"] == True :
			bone.length *= -1	
		#if "wrist_joint.L" in bone.name :
		#	bone.length *= -1			
		ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
		ob.matrix_parent_inverse.identity()
		if ctkToVillaDict[bone.name] in center_list:
			ob.location.x	= 0
		#ob.show_axis = True		
		bpy.context.scene.objects.link( ob )
	#
	ob = bpy.data.objects.new( "_mouth_L_fix_group", None )
	ob.rotation_mode = 'YZX'
	ob.parent = bpy.data.objects[ "_head_joint02"]	
	ob.matrix_world =  bpy.data.objects[ "_upper_lip_L_joint02"].matrix_world
	ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
	ob.matrix_parent_inverse.identity()
	bpy.context.scene.objects.link( ob )
	#
	ob = bpy.data.objects.new( "_mouth_R_fix_group", None )
	ob.rotation_mode = 'YZX'
	ob.parent = bpy.data.objects[ "_head_joint02"]	
	ob.matrix_world =  bpy.data.objects[ "_upper_lip_R_joint02"].matrix_world
	ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
	ob.matrix_parent_inverse.identity()
	bpy.context.scene.objects.link( ob )
	#
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	#
	bpy.ops.object.delete() 
	bpy.ops.object.select_all(action='DESELECT')
	armature_object.select = True
	bpy.context.scene.objects.active = armature_object
	armature_object.select = True








