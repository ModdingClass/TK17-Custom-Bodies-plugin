#very important, the armature 90 degrees must be applied before adjusting anything related to the bones

import bpy
import mathutils



def adjust_editbones_length():
	print("adjusting")
	#Make a coding shortcut
	armature_data = bpy.data.objects['Armature']
	#Must make armature active and in edit mode to create a bone
	bpy.context.scene.objects.active = armature_data
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	#
	parent_direct_child_dict = {
	"breast_scale_joint.R":"nipple_joint01.R",
	"breast_scale_joint.L":"nipple_joint01.L",
	"neck_joint01":"neck_jointEnd",
	"head_joint02":"head_jointEnd",
	"ball_joint.R":"toe_joint.R",
	"ball_joint.L":"toe_joint.L",
	"spine_joint02":"spine_joint03",
	"spine_joint03":"spine_joint04",
	"spine_joint04":"spine_jointEnd",
	"eye_socket_joint.L":"eye_joint.L",
	"eye_socket_joint.R":"eye_joint.R",
	"lower_jaw_joint01":"lower_jaw_jointEnd"
	}
	#
	#some bones should be left untouched
	ignore_list=["head_joint01"]
	#
	my_bones = [] 
	#	
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
	parentBone = bpy.data.armatures['Armature'].edit_bones["root"]
	print_heir(parentBone)
	#
	for bone in my_bones:
		#print ("bone: " + bone.name)
		if bone.name in ignore_list:
			#do nothing to bone size
			pass	
		else:
			if len(bone.children) == 1 :
				child = bone.children[0] # we select the single child
				bone.tail[0] = child.head[0]
				bone.tail[1] = child.head[1]
				bone.tail[2] = child.head[2]
				child.use_connect = True
			else :
				if bone.name in parent_direct_child_dict:
					childName =  parent_direct_child_dict[bone.name]
					child = bpy.data.armatures['Armature'].edit_bones[childName]
					print(bone.name+"->"+child.name)
					bone.tail[0] = child.head[0]
					bone.tail[1] = child.head[1]
					bone.tail[2] = child.head[2]
					child.use_connect = False
				#
			#
		#
	#
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

			
		
	


















