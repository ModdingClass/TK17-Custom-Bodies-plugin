import bpy, mathutils
import re
from collections import OrderedDict

ob = bpy.data.objects["body_subdiv_cage"]
me = ob.data

output_materials = OrderedDict()
#output_materials = { mat.name : [i, False]        for i, mat in enumerate(ob.data.materials)}

# first we create the list of all materials with their blender material index, and set for all the processed flag as false

for index, stock_mat in enumerate(stock_materials):
	stock_mat_name = stock_mat[0] # stock_mat[0] is the name
	output_materials[stock_mat_name]={} 
	output_materials[stock_mat_name]["key"]=stock_mat_name 
	output_materials[stock_mat_name]["index"]=index
	output_materials[stock_mat_name]["local"]="local_"+stock_mat[1]
	output_materials[stock_mat_name]["objectname"]=stock_mat_name + "_SG"
	output_materials[stock_mat_name]["stock"]= True

print (index)

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

lookup_materials=[]
indexed_output_materials = OrderedDict()


for index,mat in enumerate(ob.data.materials):
	if mat is not None:
		indexed_output_materials[index] = output_materials[mat.name]
		lookup_materials.append(output_materials[mat.name]["index"])	


indexed_output_materials
lookup_materials





