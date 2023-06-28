import numpy as np
import math
from math import radians
from math import degrees
import os
from bpy_extras.io_utils import axis_conversion
from .dictionaries import *

def recalculateBindInverseMatrix(exportfolderpath, bodyNo):
	np.set_printoptions(precision=6)
	np.set_printoptions(suppress=True)
	#
	context = bpy.context
	m = axis_conversion(
			from_forward='-Y',
			from_up='Z',
			to_forward='-Y',
			to_up='X'
			).to_4x4()
	#
	n = axis_conversion(
			from_forward='-Y',
			from_up='Z',
			to_forward='-Z',
			to_up='Y'
			).to_4x4()
	#
	mat_rot = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')
	mat_rot2 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')
	#
	p = axis_conversion(
			from_forward='-Y',
			from_up='Z',
			to_forward='Z',
			to_up='Y'
			).to_4x4()
	#
	output = ""
	#
	pyBlock_JointNamesArray = []
	pyBlock_MeshDataJointsArray = []	
	#	
	my_joints = [] 
	#	
	def print_heir(ob, levels=50):
		def recurse(ob, parent, depth):
			if depth > levels: 
				return
			#print("  " * depth, ob.name)
			if  ob.type != 'EMPTY':
				return
			if  ob.get("exportAsVillaJoint") is None or ob["exportAsVillaJoint"] == False :
				return
			my_joints.append(ob)
			pyBlock_JointNamesArray.append(ob.name[1:])
			for child in ob.children:
				recurse(child, ob,  depth + 1)
		recurse(ob, ob.parent, 0)
	#
	#
	print_heir(bpy.data.objects["_root"])
	#
	np.set_printoptions(formatter={'float': '{: 0.6f}'.format})
	for empty_object in my_joints: #+['tail_joint01','tail_joint02','tail_joint03']:#[:1]:
		#empty_object = bpy.data.objects["_"+joint]
		blend_mat = (  p * empty_object.matrix_world  *  mat_rot2 * mat_rot).transposed().inverted()
		np_mat = np.array(blend_mat)#.reshape(16,-1).T
		stringinvbindmatrix = np.array2string(np_mat, max_line_width=1000, precision=10, suppress_small=False, separator=', ').replace("-0.000000", "0").replace("0.000000", "0").replace("1.000000", "1").replace("  "," ").replace("\n","").replace("[ ","[").replace("[","(").replace("]",")").replace("((","( (").replace("))",") )")
		output = output+"\t\t"+stringinvbindmatrix +", \n"
		pyBlock_MeshDataJointsArray.append("TJoint :"+empty_object["localName"])
		#print(stringinvbindmatrix)
		#print (""+stringinvbindmatrix+", ")# + " ["+stringinvbindmatrix)
	#
	#	
	output=output[:-3]
	#file_path = exportfolderpath+"bsBlocks/part4_1_BindMatrixInverse.bs_block"
	file_path = os.path.join(exportfolderpath,"bsBlocks")
	if not os.path.exists(file_path):
		os.makedirs(file_path)
	file_path = os.path.join(file_path,"part4_1_BindMatrixInverse.bs_block")
	print("recalculateBindInverseMatrix: "+file_path)
	f = open(file_path, 'w+')
	f.write(output)
	f.close()

	file_path = os.path.join(exportfolderpath,"bsBlocks")
	file_path = os.path.join(file_path,"part3.2_1_content_MeshDataJointArray.bs_block")
	print("joints array sent to: "+file_path)
	f = open(file_path, 'w+')
	f.write( " , ".join(pyBlock_MeshDataJointsArray))
	f.close()
	bodyObjData = bpy.data.objects["body_subdiv_cage"].data
	bodyObjData["orderedJoints"] = ",".join(pyBlock_JointNamesArray)

	#



