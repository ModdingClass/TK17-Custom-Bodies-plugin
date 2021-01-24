import bpy
import mathutils

def apply_armature_rotation():
	#
	mirror_x_flag = bpy.data.armatures["Armature"].use_mirror_x
	bpy.data.armatures["Armature"].use_mirror_x = False
	#
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	armature_object = bpy.data.objects["Armature"]
	armature_object.select = True
	bpy.context.scene.objects.active = armature_object
	bpy.ops.object.transform_apply(rotation = True)
	#
	bpy.data.armatures["Armature"].use_mirror_x = mirror_x_flag





