import bpy, mathutils
from .tools_message_box import *

def duplicate_object_keep_only_VG():
	if (bpy.context.scene.objects.active is None) or (bpy.context.scene.objects.active.select == False) or (bpy.context.scene.objects.active.type != 'MESH'):
		ShowMessageBox("You need to select a mesh object before making a clone of it.", "Error", 'ERROR')
		return None

	active_object = bpy.context.scene.objects.active
	bpy.ops.object.duplicate(linked=False)
	cloned_object = bpy.context.scene.objects.active

	for i in reversed(range(len(cloned_object.material_slots))):
		print (i)
		cloned_object.active_material_index = i
		bpy.ops.object.material_slot_remove()

	for i in reversed(range(len(cloned_object.data.shape_keys.key_blocks.keys()))):
		print (i)
		cloned_object.active_shape_key_index = i
		bpy.ops.object.shape_key_remove()

	if cloned_object.name[-3:].isnumeric():
		if cloned_object.name[-4:-3] == '.':
			cloned_object.name = cloned_object.name[:-4]+"_weighted"

	cloned_object.modifiers.clear()

