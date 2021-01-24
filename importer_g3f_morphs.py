import bpy
from .dictionary_g3f_vertices import *
from .tools_message_box import *

def import_g3f_morph(base_body_mesh, morph_object) :
	
	scene = bpy.context.scene
	#for obj in scene.objects:
	#	if obj.type == 'MESH':
	#		scene.objects.active = obj
	#	
	bpy.context.scene.objects.active = morph_object
	
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.transform_apply( rotation = True )	
	
	
	bpy.ops.object.editmode_toggle()
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')
	

	#time to remove vertex we dont want from the scene
	for i in g3f_unwanted_vertices:
		bpy.context.active_object.data.vertices[i].select=True	
	bpy.ops.object.editmode_toggle()
	# materials_list = bpy.context.object.material_slots.keys()
	# for mat in materials_list:
		# if ("Irises" in mat) or ("Cornea" in mat) or ("EyeMoisture" in mat) or ("Pupils" in mat) or ("Sclera" in mat):
			# mat_index = bpy.context.object.material_slots.find(mat)
			# bpy.context.object.active_material_index = mat_index
			# bpy.ops.object.material_slot_select()
	bpy.ops.mesh.delete(type='VERT')

	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.editmode_toggle()

	bpy.ops.object.mode_set(mode='OBJECT')
	
	if (base_body_mesh != None):
		base_body_mesh.select = True
		bpy.context.scene.objects.active = base_body_mesh
		if base_body_mesh.data.shape_keys != None:
			if morph_object.name in base_body_mesh.data.shape_keys.key_blocks.keys():
				shapekey_index = base_body_mesh.data.shape_keys.key_blocks.keys().index(morph_object.name)
				#base_body_mesh = bpy.context.scene.objects.active
				base_body_mesh.active_shape_key_index = shapekey_index
				bpy.ops.object.shape_key_remove()
		#
		bpy.ops.object.join_shapes()
	else:
		ShowMessageBox("Morph imported but an Active base mesh is missing!", "Success", 'INFO')
		return {'FINISHED'}


