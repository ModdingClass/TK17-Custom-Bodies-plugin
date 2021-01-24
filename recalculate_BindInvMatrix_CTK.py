import numpy as np
import math
from math import radians
from math import degrees
import os
from bpy_extras.io_utils import axis_conversion
from .dictionaries import *

def recalculateBindInverseMatrixCTK(exportfolderpath, bodyNo):
	np.set_printoptions(precision=6)
	np.set_printoptions(suppress=True)
	context = bpy.context
	m = axis_conversion(
			from_forward='-Y',
			from_up='Z',
			to_forward='-Y',
			to_up='X'
			).to_4x4()

	n = axis_conversion(
			from_forward='-Y',
			from_up='Z',
			to_forward='-Z',
			to_up='Y'
			).to_4x4()


	#geometryMatrix = mathutils.Matrix( ( [ 1, 0, 0, 0 ], [ 0, 0.99596441, 0.089749388, 0 ], [ 0, -0.089749388, 0.99596441, 0 ], [ 0, 1.6074985, 0.028200639, 1 ] ) )
	#geometryMatrix.transpose()

	mat_rot = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')
	mat_rot2 = mathutils.Matrix.Rotation(math.radians(90.0), 4, 'Z')

	p = axis_conversion(
			from_forward='-Y',
			from_up='Z',
			to_forward='Z',
			to_up='Y'
			).to_4x4()

	
	np.set_printoptions(formatter={'float': '{: 0.6f}'.format})
	
	output=""
	for joint in animSkeletonValues:
		empty_object = bpy.data.objects["_"+joint]
		blend_mat = ( p  * empty_object.matrix_world *  mat_rot2 * mat_rot ).transposed().inverted() 
		reverted_blend_mat = blend_mat.inverted().transposed()
		np_mat = np.array(blend_mat).reshape(16,-1).T
		stringinvbindmatrix = np.array2string(np_mat, max_line_width=1000, precision=6, suppress_small=True, separator=' ').strip("[]").replace("-0.000000", "0").replace("0.000000", "0").replace("1.000000", "1").replace("  "," ")
		output+=(empty_object.name[1:] + " "+stringinvbindmatrix+"\n")

	file_path = os.path.join(exportfolderpath,"AnimSkeleton("+bodyNo+").txt")
	print("recalculateBindInverseMatrixCTK: "+file_path)
	f = open(file_path, 'w+')
	f.write(output)
	f.close()
	#



