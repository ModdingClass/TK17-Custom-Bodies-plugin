import bpy, mathutils
from collections import OrderedDict
from .dictionary_materials import *



stock_materials = [
	['body_leg_lower_R','822',0],
	['body_leg_lower_L','823',1],
	['body_main_lower','824',2],
	['body_arm_lower_R','825',3],
	['body_arm_lower_L','826',4],
	['body_fingernails_R','827',5],
	['body_arm_upper_R','828',6],
	['body_arm_upper_L','829',7],
	['body_leg_upper_R','830',8],
	['body_leg_upper_L','831',9],
	['body_foot_L','832',10],
	['body_hand01_L','833',11],
	['body_genital01','834',12],
	['body_head01','835',13],
	['body_main_upper','242',14],
	['body_hand01_R','836',15],
	['body_foot_R','837',16],
	['body_fingernails_L','838',17],
	['body_eyelash01','839',18]
	#['body_teeth01','461',19],
]	


def build_materials_list_lookup():
	#
	ob = bpy.data.objects["body_subdiv_cage"]
	me = ob.data
	
	output_materials = OrderedDict()
	indexed_output_materials = OrderedDict()
	lookup_materials=[]
	
	#output_materials = { mat.name : [i, False]        for i, mat in enumerate(ob.data.materials)}
	# first we create the list of all materials with their blender material index, and set for all the processed flag as false
	for index, stock_mat in enumerate(stock_materials):
		stock_mat_name = stock_mat[0] # stock_mat[0] is the name
		output_materials[stock_mat_name]={} 
		output_materials[stock_mat_name]["key"]=stock_mat_name 
		output_materials[stock_mat_name]["index"]=index
		output_materials[stock_mat_name]["localname"]="local_"+stock_mat[1]
		output_materials[stock_mat_name]["objectname"]=stock_mat_name + "_SG"
		output_materials[stock_mat_name]["stock"]= True
	print (index)
	#
	for mat in ob.data.materials:
		if mat is not None:
			if mat.name in output_materials:
				print(mat.name +" was already added at index: "+str(output_materials[mat.name]["index"]))
			else:
				index = index + 1
				print(mat.name +" will be added at index: "+str(index))
				if mat.get("localname") is not None:
					localname = mat["localname"]
				else: 
					localname = "custom_"+mat.name
				if mat.get("objectname") is not None:
					objectname = mat["objectname"]
				else: 
					objectname = "custom_" + mat.name + "_SG"
				#	
				output_materials[mat.name]={} 
				output_materials[mat.name]["key"]=mat.name
				output_materials[mat.name]["index"]=index
				output_materials[mat.name]["localname"]= localname
				output_materials[mat.name]["objectname"]= objectname
				output_materials[stock_mat_name]["stock"]= False
	#
	#
	#
	for index,mat in enumerate(ob.data.materials):
		if mat is not None:
			indexed_output_materials[index] = output_materials[mat.name]
			lookup_materials.append(output_materials[mat.name]["index"])	
	#
	return lookup_materials, output_materials, indexed_output_materials
