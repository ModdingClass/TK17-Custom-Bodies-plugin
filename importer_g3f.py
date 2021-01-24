import bpy
from .dictionary_g3f_vertices import *

def import_g3f() :
	
	scene = bpy.context.scene
	#for obj in scene.objects:
	#	if obj.type == 'MESH':
	#		scene.objects.active = obj
	#	
	
	bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.transform_apply( rotation = True )

	bpy.ops.object.editmode_toggle()
	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')
	
	for i in g3f_unwanted_vertices:
		bpy.context.active_object.data.vertices[i].select=True	
	bpy.ops.object.editmode_toggle()
	# materials_list = bpy.context.object.material_slots.keys()
	# for mat in materials_list:
		# if ("Irises" in mat) or ("Cornea" in mat) or ("EyeMoisture" in mat) or ("Pupils" in mat) or ("Sclera" in mat):
			# mat_index = bpy.context.object.material_slots.find(mat)
			# bpy.context.object.active_material_index = mat_index
			# bpy.ops.object.material_slot_select()
			
			
			
			
	#mat_index = bpy.context.object.material_slots.find("Irises")
	#bpy.context.object.active_material_index = mat_index
	#bpy.ops.object.material_slot_select()
	#mat_index = bpy.context.object.material_slots.find("Cornea")
	#bpy.context.object.active_material_index = mat_index
	#bpy.ops.object.material_slot_select()
	#mat_index = bpy.context.object.material_slots.find("EyeMoisture")
	#bpy.context.object.active_material_index = mat_index
	#bpy.ops.object.material_slot_select()
	#mat_index = bpy.context.object.material_slots.find("Pupils")
	#bpy.context.object.active_material_index = mat_index
	#bpy.ops.object.material_slot_select()
	#mat_index = bpy.context.object.material_slots.find("Sclera")
	#bpy.context.object.active_material_index = mat_index
	#bpy.ops.object.material_slot_select()


	bpy.ops.mesh.delete(type='VERT')

	bpy.ops.mesh.select_all(action='DESELECT')
	bpy.ops.object.editmode_toggle()



	#delete unused materials
	ob = bpy.context.active_object
	mat_slots = {}
	for p in ob.data.polygons:
		mat_slots[p.material_index] = 1

	mat_slots = mat_slots.keys()
	 
	for i in reversed(range(len(ob.material_slots))):
		if i not in mat_slots:
			bpy.context.scene.objects.active = ob
			ob.active_material_index = i
			bpy.ops.object.material_slot_remove()
		

	bpy.ops.object.editmode_toggle()
	bpy.ops.mesh.select_mode(type="FACE")


	materials_list = bpy.context.object.material_slots.keys()
	for mat in materials_list:
		if ("EyeSocket" in mat) or ("Ears" in mat) or ("Lips" in mat) or ("Face" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()
	#
	#assign all faces to the Face material
	bpy.ops.object.material_slot_assign()
	bpy.context.object.active_material.name = "body_head01"
	bpy.ops.mesh.select_all(action='DESELECT')


	materials_list = bpy.context.object.material_slots.keys()
	for mat in materials_list:
		if ("Mouth" in mat) or ("Teeth" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()
	#
	#assign all faces to the Face material
	bpy.ops.object.material_slot_assign()
	bpy.context.object.active_material.name = "body_teeth01"
	bpy.ops.mesh.select_all(action='DESELECT')

	materials_list = bpy.context.object.material_slots.keys()
	for mat in materials_list:
		if ("Arms" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()		
	#
	bpy.context.object.active_material.name = "body_hand01_L"
	bpy.ops.mesh.select_all(action='DESELECT')


	materials_list = bpy.context.object.material_slots.keys()
	for mat in materials_list:
		if ("Torso" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()	
	#			
	bpy.context.object.active_material.name = "body_main_upper"
	bpy.ops.mesh.select_all(action='DESELECT')

	materials_list = bpy.context.object.material_slots.keys()
	for mat in materials_list:
		if ("Toenails" in mat) or ("Legs" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()	
	#
	bpy.context.object.active_material.name = "body_foot_L"
	bpy.ops.object.material_slot_assign()
	bpy.ops.mesh.select_all(action='DESELECT')

	materials_list = bpy.context.object.material_slots.keys()
	for mat in materials_list:
		if ("Genitalia" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()	
	#
	bpy.context.object.active_material.name = "body_genital01"
	bpy.ops.mesh.select_all(action='DESELECT')

	for mat in materials_list:
		if ("Eyelashes" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()	
	#
	bpy.context.object.active_material.name = "body_eyelash01"
	bpy.ops.mesh.select_all(action='DESELECT')

	for mat in materials_list:
		if ("Fingernails" in mat):
			mat_index = bpy.context.object.material_slots.find(mat)
			bpy.context.object.active_material_index = mat_index
			bpy.ops.object.material_slot_select()	
	#
	#assign all faces to the Fingernails material
	bpy.ops.object.material_slot_assign()
	bpy.context.object.active_material.name = "body_fingernails_L"
	bpy.ops.mesh.select_all(action='DESELECT')


	bpy.ops.object.mode_set(mode='OBJECT')

	#delete unused materials
	ob = bpy.context.active_object
	mat_slots = {}
	for p in ob.data.polygons:
		mat_slots[p.material_index] = 1

	mat_slots = mat_slots.keys()
	 
	for i in reversed(range(len(ob.material_slots))):
		if i not in mat_slots:
			bpy.context.scene.objects.active = ob
			ob.active_material_index = i
			bpy.ops.object.material_slot_remove()
		



	material_names = [
	'body_teeth01',
	'body_leg_lower_R',
	'body_leg_lower_L',
	'body_main_lower',
	'body_arm_lower_R',
	'body_arm_lower_L',
	'body_fingernails_R',
	'body_arm_upper_R',
	'body_arm_upper_L',
	'body_leg_upper_R',
	'body_leg_upper_L',
	'body_foot_L',
	'body_hand01_L',
	'body_genital01',
	'body_head01',
	'body_main_upper',
	'body_hand01_R',
	'body_foot_R',
	'body_fingernails_L',
	'body_eyelash01']




	for target_mat_name in material_names: 
		# Get material
		mat = bpy.data.materials.get(target_mat_name)
		#if it doesnt exist, create it.
		if mat is None:
			# create material
			mat = bpy.data.materials.new(name=target_mat_name)
			#assign material
			ob.data.materials.append(mat)	
		#otherwise
		else:
			#get material
			mat = bpy.data.materials.get(target_mat_name)
			found = False
			for idx, m in enumerate(ob.material_slots):
				if (m.name == target_mat_name):
					bpy.context.object.active_material_index = idx
					bpy.ops.object.material_slot_select()
					found = True
					break
			if (found == False):
				ob.data.materials.append(mat)










	ob = bpy.context.active_object
	for j in range (len(ob.material_slots)):
		for i in range (len(ob.material_slots)-1):
			ob.active_material_index = i
			tempStr = ob.active_material.name
			ob.active_material_index = i+1
			if ob.active_material.name.split("_")[-1] < tempStr.split("_")[-1]:
				bpy.ops.object.material_slot_move(direction='UP')




	ob.active_material_index = 0
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')
	bpy.ops.object.material_slot_move(direction='DOWN')


	#add fake shapekeys

	verts = ob.data.vertices

	sk_basis = ob.shape_key_add('Basis')
	ob.data.shape_keys.use_relative = True

	shape_keys = [
	'bbb_asian02_morph',
	'bbb_vaginafix_morph',
	'bbb_eye_L_morph',
	'bbb_asian01_morph',
	'bbb_atomic01',
	'bbb_hentai01_morph',
	'bbb_eye_R_morph',
	'bbb_african01_morph',
	'bbb_vagina_morph',
	'bbb_jenna01_morph',
	'bbb_capelli01_morph',
	'bbb_ear01',
	'bbb_pregnant',
	'bbb_ear02'
	]

	# Create 10 sequential deformations
	for shape_key in shape_keys: 
		# Create new shape key
		sk = ob.shape_key_add(shape_key)
		sk.slider_min = -1





	ob.name= "body_subdiv_cage"
	ob.data.name = "M_body_subdiv_cage"


	ob.data.uv_layers[0].name = "UVMap"


