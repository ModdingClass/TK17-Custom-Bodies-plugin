import bpy


def merge_vgroups_into_third(object_name, vgroup_A_name, vgroup_B_name, vgroup_C_name):
	#
	ob = bpy.data.objects[object_name]
	# EDIT THIS
	#vgroup_A_name = groupA
	#vgroup_B_name = groupB
	#vgroup_C_name = groupC
	# Get both groups and add them into third
	if (vgroup_A_name in ob.vertex_groups and vgroup_B_name in ob.vertex_groups):
		vgroup = ob.vertex_groups.new(name=vgroup_C_name)
		for id, vert in enumerate(ob.data.vertices):
			available_groups = [v_group_elem.group for v_group_elem in vert.groups]
			A = B = 0
			if ob.vertex_groups[vgroup_A_name].index in available_groups:
				A = ob.vertex_groups[vgroup_A_name].weight(id)
			if ob.vertex_groups[vgroup_B_name].index in available_groups:
				B = ob.vertex_groups[vgroup_B_name].weight(id)
			# only add to vertex group is weight is > 0
			sum = A + B
			if sum > 0:
				vgroup.add([id], sum ,'REPLACE')



