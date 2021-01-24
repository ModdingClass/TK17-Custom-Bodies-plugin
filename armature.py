import bpy
import mathutils
import math
import numpy as np
import os

from collections import OrderedDict
from mathutils import Vector
from mathutils import Matrix
from math import radians

def nozeros( vec, decimal_points = 6 ):
	return any( round( v, decimal_points ) for v in vec )

def flatten(mat):
	dim = len(mat)
	return [mat[j][i] for i in range(dim) for j in range(dim)]

sorted_bones = [] 
def sort_bones(ob, levels=50):
	def recurse(ob, parent, depth):
		if depth > levels: 
			return
		#print("  " * depth, ob.name)
		sorted_bones.append(ob)
		for child in ob.children:
			recurse(child, ob,  depth + 1)
	recurse(ob, ob.parent, 0)
	
def parentsForNode(obj):
	if obj.parent:
		return [obj.parent.name] + parentsForNode(obj.parent)
	return []

#function to hide all children of a node, including the node
def hide_children(object):
    object.hide = True
    for o in object.children:
        hide_children(o)


def select_children(object):
	if object is not None:
		object.select = True
		for o in object.children:
			select_children(o)



def getTransformations(translation, orientation, rotation):
	vec = Vector((translation))
	trans = Matrix.Translation((vec.z,vec.x,vec.y))
	rotationVec = Vector(orientation)
	rotationVec = Vector([radians(rotationVec.z),radians(rotationVec.x),radians(rotationVec.y)])	
	euler_rotation = mathutils.Euler((rotationVec.x, rotationVec.y, rotationVec.z), 'YZX')
	orient = euler_rotation.to_matrix().to_4x4()
	rotationVec = Vector(rotation)
	rotationVec = Vector([radians(rotationVec.z),radians(rotationVec.x),radians(rotationVec.y)])	
	euler_rotation = mathutils.Euler((rotationVec.x, rotationVec.y, rotationVec.z), 'YZX')
	rot = euler_rotation.to_matrix().to_4x4()
	return trans, orient, rot

def getGlobalTransformations(translation, orientation, rotation):
	vec = Vector((translation))
	trans = Matrix.Translation((vec.x,-vec.z,vec.y))
	rotationVec = Vector(orientation)
	rotationVec = Vector([radians(rotationVec.x),radians(-rotationVec.z),radians(rotationVec.y)])	
	euler_rotation = mathutils.Euler((rotationVec.x, rotationVec.y, rotationVec.z), 'XYZ')
	orient = euler_rotation.to_matrix().to_4x4()
	rotationVec = Vector(rotation)
	rotationVec = Vector([radians(rotationVec.x),radians(-rotationVec.z),radians(rotationVec.y)])	
	euler_rotation = mathutils.Euler((rotationVec.x, rotationVec.y, rotationVec.z), 'XYZ')
	rot = euler_rotation.to_matrix().to_4x4()
	return trans, orient, rot

def addTK17Transform(translation, orientation,rotation, name, parent) :
	trans,orient, rot = getGlobalTransformations (translation, orientation, rotation)
	scene = bpy.context.scene
	empty = bpy.data.objects.new(name, None)
	empty.show_axis = True
	if parent !="":
		empty.parent = bpy.data.objects[parent]
	empty.rotation_mode = 'XYZ'
	empty.matrix_basis = 	trans * orient * rot * empty.matrix_basis
	parentsArray  = parentsForNode(empty)
	scene.objects.link(empty)
	scene.update()	


def addTK17Bone(translation, orientation,rotation, name, parent) :
	trans,orient, rot = getTransformations (translation, orientation, rotation)
	if name in ["spine_jointEnd", "neck_jointEnd", "lower_jaw_jointEnd", "forehead_jointEnd", "cheek_R_jointEnd", "cheek_L_jointEnd", "head_jointEnd"] :
		#need to continue
		pass
	elif "_jointEnd" in name :
		#return
		pass
	else:
		pass
	scene = bpy.context.scene
	empty = bpy.data.objects.new(name, None)
	empty.show_axis = True
	if parent !="":
		empty.parent = bpy.data.objects[parent]
	#if name != "root" :
	#	empty.parent = bpy.data.objects[parent]
	empty.rotation_mode = 'YZX'
	#
	#if 1==0:
	if nozeros(Vector(rotation)):
		empty.matrix_basis = 	trans * orient * rot * empty.matrix_basis		
	else:
		vec = Vector((translation))
		empty.location = Vector((vec.z,vec.x,vec.y))
		rotationVec = Vector(orientation)
		empty.rotation_euler = Vector([radians(rotationVec.z),radians(rotationVec.x),radians(rotationVec.y)])
	parentsArray  = parentsForNode(empty)
	hip_R_joint_child = len([i for i in parentsArray if "hip_R_joint" in i]) > 0
	knee_R_joint_child = len([i for i in parentsArray if "knee_R_joint" in i]) > 0
	shoulder_L_joint_child = len([i for i in parentsArray if "shoulder_L_joint" in i]) > 0
	breast_L_joint_child = len([i for i in parentsArray if "breast_L_joint" in i]) > 0
	breast_R_joint_child = len([i for i in parentsArray if "breast_R_joint" in i]) > 0
	wrist_L_joint_child = len([i for i in parentsArray if "wrist_L_joint" in i]) > 0
	upper_lip_R_joint01_child = len([i for i in parentsArray if "upper_lip_R_joint01" in i]) > 0
	lower_lip_R_joint01_child = len([i for i in parentsArray if "lower_lip_R_joint01" in i]) > 0
	vagina_L_joint01_child = len([i for i in parentsArray if "vagina_L_joint01" in i]) > 0
	clavicle_L_joint_child = len([i for i in parentsArray if "clavicle_L_joint" in i]) > 0
	#butt_R_joint01_child = len([i for i in parentsArray if "butt_R_joint01" in i]) > 0
	lowerBodyList = [ "hip_R_joint", "vagina_L_joint01", "clavicle_L_joint"]
	breastFixList = ["breast_L_joint", "breast_scale_L_joint", "nipple_L_joint01", "nipple_L_jointEnd", "breast_deform01_R_joint01","breast_deform02_R_joint01", "breast_deform03_R_joint01","breast_deform01_R_jointEnd","breast_deform02_R_jointEnd","breast_deform03_R_jointEnd"]
	lipsFixList = ["upper_lip_R_joint01","upper_lip_R_joint02","upper_lip_R_joint03","upper_lip_R_jointEnd", "lower_lip_R_joint01","lower_lip_R_joint02","lower_lip_R_joint03","lower_lip_R_jointEnd"]
	headFixList = ["cheek_R_joint01", "cheek_R_jointEnd","ear_R_joint01", "ear_R_jointEnd", "forehead_joint01","forehead_jointEnd", "nose_joint01", "nose_joint01","nose_joint02","nose_jointEnd"]
	eyeFixList =["eye_socket_R_joint", "eye_brow_R_joint01","eye_brow_R_joint02", "eye_brow_R_jointEnd", "eye_R_joint"]
	specialCaseList = ["rib_R_jointEnd", "butt_R_jointEnd"]
	fixList = lowerBodyList + breastFixList +lipsFixList + eyeFixList + headFixList +specialCaseList
	empty["isFlipped"] = False
	if name in fixList or hip_R_joint_child or vagina_L_joint01_child or clavicle_L_joint_child : 
		#addXYZCorrectorEmpty (name)
		empty["isFlipped"] = True
	#if name == "wrist_L_joint":
	#	empty.rotation_euler.x = empty.rotation_euler.x + radians(180)	
	scene.objects.link(empty)
	scene.update()	


def addBonesFromHardcodedValue():
	if (True == True):
		#{--
		#;(0, 0, 0)
		#7.1250162
		addTK17Bone(   (0, 0, 0 )  ,   ( 0, 0, 0 ),  ( 90, -7.1250162, 90 )    , "root","")
		#addTK17Bone(   (0, 0, 0 )  ,   ( 0, 0, 0 ),  ( 0, 0, 7.1250162 )    , "root","")
		#addTK17Bone( (0, 0.98419, -0.031404294 ) , ( 0, 0, 0 ), ( 0, 0, 7.1250162 ) , 'root','')
		#addTK17Bone( (0, 0, 0 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'root','')
		addTK17Bone( (-0.11643519, 0.0081185568, 0 ) , ( -90,  -90,  0  )  , ( 0, 0, 0 ) , 'anus_joint','root')
		addTK17Bone( (-0.074394509, 0.046304256, 0.008 ) , ( 90,  0,  -37.489288  )  , ( 0, 0, 0 ) , 'vagina_L_joint01','root')
		addTK17Bone( (-0.043407869, 0, 0.0045066359 ) , ( -149.63573,  0,  90  )  , ( 0, 0, 0 ) , 'vagina_L_jointEnd','vagina_L_joint01')
		addTK17Bone( (-0.074394509, 0.046304256, -0.008 ) , ( 90,  0,  142.51071  )  , ( 360, 0, 360 ) , 'vagina_R_joint01','root')
		addTK17Bone( (0.043407869, 0, -0.0045066359 ) , ( 30.364271,  0,  90  )  , ( 0, 0, 0 ) , 'vagina_R_jointEnd','vagina_R_joint01')
		addTK17Bone( (-0.047841728, -0.038221464, 0.07788647 ) , ( -90,  0,  -98.7616  )  , ( 0, 0, 0 ) , 'butt_L_joint01','root')
		addTK17Bone( (0.065647066, 0, 0 ) , ( 91.636574,  0,  -90  )  , ( 0, 0, 0 ) , 'butt_L_jointEnd','butt_L_joint01')
		addTK17Bone( (-0.047841728, -0.038221464, -0.078 ) , ( -90,  0,  -98.7616  )  , ( 0, 0, 0 ) , 'butt_R_joint01','root')
		addTK17Bone( (0.065647066, 0, 0 ) , ( 91.636574,  0,  -90  )  , ( 0, 0, 0 ) , 'butt_R_jointEnd','butt_R_joint01')
		addTK17Bone( (-0.088699527, 0.085588045, 0 ) , ( 0,  0,  151.07358  )  , ( 0, 0, 0 ) , 'testicles_joint01','root')
		addTK17Bone( (0.03216207, 0, 0 ) , ( 0,  0,  17.037767  )  , ( 0, 0, 0 ) , 'testicles_joint02','testicles_joint01')
		addTK17Bone( (0.035958286, 0, 0 ) , ( 94.763641,  -90,  0  )  , ( 0, 0, 0 ) , 'testicles_jointEnd','testicles_joint02')
		addTK17Bone( (-0.052909896, 0.10569026, 0 ) , ( 0,  0,  137.24707  )  , ( 0, 0, 0 ) , 'penis_joint01','root')
		addTK17Bone( (0.031490196, 0, 0 ) , ( 0,  0,  14.446558  )  , ( 0, 0, 0 ) , 'penis_joint02','penis_joint01')
		addTK17Bone( (0.036600363, 0, 0 ) , ( 0,  0,  8.1867323  )  , ( 0, 0, 0 ) , 'penis_joint03','penis_joint02')
		addTK17Bone( (0.039840519, 0, 0 ) , ( 102.99461,  -90,  0  )  , ( 0, 0, 0 ) , 'penis_jointEnd','penis_joint03')
		addTK17Bone( (-0.020929646, 0.017115666, 0.112832 ) , ( 0,  0,  166.95436  )  , ( 0, 0, 0 ) , 'hip_L_joint','root')
		addTK17Bone( (0.4432528, -0.0017294659, 0 ) , ( 0,  0,  16.94171  )  , ( 0, 0, 0 ) , 'knee_L_joint','hip_L_joint')
		addTK17Bone( (0.43836197, 0, 0 ) , ( -180,  0,  -65.026237  )  , ( -5.315916e-06, 0, 0 ) , 'ankle_L_joint','knee_L_joint')
		addTK17Bone( (0.12638146, 0, 0 ) , ( 0,  0,  33.251144  )  , ( 3.4150946e-06, 0, 0 ) , 'ball_L_joint','ankle_L_joint')
		addTK17Bone( (0.097554028, 0, 0 ) , ( -2.743705,  90,  0  )  , ( 0, 0, 0 ) , 'toe_L_joint','ball_L_joint')
		addTK17Bone( (0.048167203, -0.00078487588, 0.00082114269 ) , ( 90,  13.746578,  2.7437053  )  , ( 0, 0, 0 ) , 'toe_deform01_L_joint01','ball_L_joint')
		addTK17Bone( (0.036767941, 0, 0 ) , ( -90,  0,  -76.253418  )  , ( 0, 0, 0 ) , 'toe_deform01_L_jointEnd','toe_deform01_L_joint01')
		addTK17Bone( (0.039374188, -0.00097012328, -0.032512531 ) , ( 90,  12.166531,  2.7437053  )  , ( 0, 0, 0 ) , 'toe_deform02_L_joint01','ball_L_joint')
		addTK17Bone( (0.028718958, 0, 0 ) , ( -90,  0,  -77.833466  )  , ( 0, 0, 0 ) , 'toe_deform02_L_jointEnd','toe_deform02_L_joint01')
		addTK17Bone( (-0.020929646, 0.017115666, -0.11283169 ) , ( 0,  0,  -13.045637  )  , ( 0, 0, 0 ) , 'hip_R_joint','root')
		addTK17Bone( (-0.4432528, 0.0017294659, 0 ) , ( 0,  0,  16.94171  )  , ( 0, 0, 7.1492905e-05 ) , 'knee_R_joint','hip_R_joint')
		addTK17Bone( (-0.43836197, 0, 0 ) , ( 180,  0,  -65.026237  )  , ( 3.1112293e-06, 0, 0 ) , 'ankle_R_joint','knee_R_joint')
		addTK17Bone( (-0.12638146, 0, 0 ) , ( 0,  0,  33.251144  )  , ( -1.4787794e-06, 0, 0 ) , 'ball_R_joint','ankle_R_joint')
		addTK17Bone( (-0.097554028, 0, 0 ) , ( -2.743705,  90,  0  )  , ( 0, 0, 0 ) , 'toe_R_joint','ball_R_joint')
		addTK17Bone( (-0.048167188, 0.00078491418, -0.0008206864 ) , ( 90,  13.746583,  2.7437048  )  , ( 0, 0, 0 ) , 'toe_deform01_R_joint01','ball_R_joint')
		addTK17Bone( (-0.036767948, 0, 0 ) , ( -90,  0,  -76.253418  )  , ( 0, 0, 0 ) , 'toe_deform01_R_jointEnd','toe_deform01_R_joint01')
		addTK17Bone( (-0.039374173, 0.00097013445, 0.032513313 ) , ( 90,  12.166535,  2.7437048  )  , ( 0, 0, 0 ) , 'toe_deform02_R_joint01','ball_R_joint')
		addTK17Bone( (-0.028718526, 0, 0 ) , ( -90,  0,  -77.833466  )  , ( 0, 0, 0 ) , 'toe_deform02_R_jointEnd','toe_deform02_R_joint01')
		addTK17Bone( ( 0, 0, 0  ) , ( 90,  0,  -6.635  )  , ( 0, 0, 0 ) , 'spine_joint01','root')
		addTK17Bone( (0.1135106459, 0, 0 ) , ( 0,  -0.42314085,  0  )  , ( 0, 0, 0 ) , 'spine_joint02','spine_joint01')
		addTK17Bone( (-0.00094830978, 0, -0.0654295 ) , ( 0,  89.93335,  0  )  , ( 0, 0, 0 ) , 'stomach_joint01','spine_joint02')
		addTK17Bone( (0.07659173, 0, 0 ) , ( 90,  0,  90  )  , ( 0, 0, 0 ) , 'stomach_jointEnd','stomach_joint01')
		addTK17Bone( (0.1211563945, 0, 0 ) , ( 0,  -0.62239087,  0  )  , ( 0, 0, 0 ) , 'spine_joint03','spine_joint02')
		addTK17Bone( (-0.0014060538, 0.0956528, -0.04569504 ) , ( 0,  90.55574,  0  )  , ( 0, 0, 0 ) , 'rib_L_joint01','spine_joint03')
		addTK17Bone( (0.0776199, 0, 0 ) , ( -90,  0,  90  )  , ( 0, 0, 0 ) , 'rib_L_jointEnd','rib_L_joint01')
		addTK17Bone( (-0.0014029481, -0.095652826, -0.04569507 ) , ( 180,  89.44426,  180  )  , ( 0, 0, 0 ) , 'rib_R_joint01','spine_joint03')
		addTK17Bone( (0.077619925, 0, 0 ) , ( 90,  0,  90  )  , ( 0, 0, 0 ) , 'rib_R_jointEnd','rib_R_joint01')
		addTK17Bone( (0.12765756, 0, 0 ) , ( 0,  0.53489178,  0  )  , ( 0, 0, 0 ) , 'spine_joint04','spine_joint03')
		addTK17Bone( (0.033933386, 0.0663397, -0.061905816 ) , ( 22.169832,  -32.481556,  -12.350241  )  , ( 0, 0, 0 ) , 'breast_L_joint','spine_joint04')
		addTK17Bone( (-0.073957615, 0, 0 ) , ( 0,  -71.873276,  0  )  , ( 0, 0, 0 ) , 'breast_scale_L_joint','breast_L_joint')
		addTK17Bone( (-0.067325272, 0, 0 ) , ( 0,  -1.5266745,  0  )  , ( 0, 0, 0 ) , 'nipple_L_joint01','breast_scale_L_joint')
		addTK17Bone( (-0.0087084556, 0, 0 ) , ( 90,  -0.50702906,  0  )  , ( 0, 0, 0 ) , 'nipple_L_jointEnd','nipple_L_joint01')
		addTK17Bone( ( 0, 0, 0  ) , ( -11.561043,  23.313871,  -145.12247  )  , ( 0, 0, 0 ) , 'breast_deform01_L_joint01','breast_scale_L_joint')
		addTK17Bone( (0.071436748, 0, -1.7064352e-06 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'breast_deform01_L_jointEnd','breast_deform01_L_joint01')
		addTK17Bone( ( 0, 0, 0  ) , ( -0.45403409,  -48.1916,  -178.63318  )  , ( 0, 0, 0 ) , 'breast_deform02_L_joint01','breast_scale_L_joint')
		addTK17Bone( (0.073019817, 0, -1.9734418e-06 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'breast_deform02_L_jointEnd','breast_deform02_L_joint01')
		addTK17Bone( ( 0, 0, 0  ) , ( 12.418375,  22.921894,  141.54634  )  , ( 0, 0, 0 ) , 'breast_deform03_L_joint01','breast_scale_L_joint')
		addTK17Bone( (0.069439188, 0, -4.3985779e-06 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'breast_deform03_L_jointEnd','breast_deform03_L_joint01')
		addTK17Bone( (0.03393387, -0.066339657, -0.06190585 ) , ( 22.169832,  147.51845,  12.350241  )  , ( 0, 0, 0 ) , 'breast_R_joint','spine_joint04')
		addTK17Bone( (0.073957436, 0, 0 ) , ( 0,  -71.873276,  0  )  , ( 0, 0, 0 ) , 'breast_scale_R_joint','breast_R_joint')
		addTK17Bone( (0.0673252, 0, 0 ) , ( 0,  -1.5266745,  0  )  , ( 0, 0, 0 ) , 'nipple_R_joint01','breast_scale_R_joint')
		addTK17Bone( (0.0087093385, 0, 0 ) , ( 90,  -0.50702906,  0  )  , ( 0, 0, 0 ) , 'nipple_R_jointEnd','nipple_R_joint01')
		addTK17Bone( ( 0, 0, 0  ) , ( -11.561043,  23.313871,  -145.12247  )  , ( 0, 0, 0 ) , 'breast_deform01_R_joint01','breast_scale_R_joint')
		addTK17Bone( (-0.071435817, 0, 0 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'breast_deform01_R_jointEnd','breast_deform01_R_joint01')
		addTK17Bone( ( 0, 0, 0  ) , ( -0.45403409,  -48.1916,  -178.63318  )  , ( 0, 0, 0 ) , 'breast_deform02_R_joint01','breast_scale_R_joint')
		addTK17Bone( (-0.073021129, 0, 0 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'breast_deform02_R_jointEnd','breast_deform02_R_joint01')
		addTK17Bone( ( 0, 0, 0  ) , ( 12.418375,  22.921894,  141.54634  )  , ( 0, 0, 0 ) , 'breast_deform03_R_joint01','breast_scale_R_joint')
		addTK17Bone( (-0.06943582, 0, 0 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'breast_deform03_R_jointEnd','breast_deform03_R_joint01')
		addTK17Bone( (0.1017823145, 0, 0 ) , ( 0,  -0.19204162,  0  )  , ( 0, 0, 0 ) , 'spine_jointEnd','spine_joint04')
		addTK17Bone( (0.076593883, 0, 0 ) , ( 0,  9.7023716,  0  )  , ( 0, 0, 0 ) , 'neck_joint01','spine_jointEnd')
		#
		#
		#-----------------addTK17Bone(   (0, 0, 0 )  ,   ( 0, 0, 0 ),  ( 0, 0, 7.1250162 )    , "root","")
		addTK17Bone( (-0.026015548, 0.0489839, -0.055562779 ) , ( 100.778,  28.161,  -84.866  )  , ( 0, 0, 0 ) , 'clavicle_L_joint','neck_joint01')
		addTK17Bone( (-0.1251177, 0, 0 ) , ( 0,  0,  19.149282  )  , ( -4.5658915e-05, 6.5000105, 0 ) , 'shoulder_L_joint','clavicle_L_joint')
		addTK17Bone( (-0.29089859, 0, 0 ) , ( 0,  0,  27.265728  )  , ( 0, 0, 0 ) , 'elbow_L_joint','shoulder_L_joint')
		addTK17Bone( (-0.11663311, 0, 3.7998313e-06 ) , ( -90,  0,  0  )  , ( 0, 0, 0 ) , 'forearm_L_joint','elbow_L_joint')
		addTK17Bone( (-0.15327427, 3.2597879e-06, 0 ) , ( 0, 0, 180 ) , ( 6.690374e-05, 0.00055939768, -0.00030231389 ) , 'wrist_L_joint','forearm_L_joint')   #we inject a 180 joint orientation here because .RotationAxis( 0f, 0f, 180f );
		addTK17Bone( (0.027041, 0.0090658534, -0.027353426 ) , ( -50,  -33.093,  -177.566  )  , ( 0, 0, 0 ) , 'finger01_L_joint01','wrist_L_joint')
		addTK17Bone( (-0.044952333, -0.0022839732, 0 ) , ( 0,  7.5,  13.616971  )  , ( 0, 0, 0 ) , 'finger01_L_joint02','finger01_L_joint01')
		addTK17Bone( (-0.024779227, -0.0019665915, 1.1152764e-06 ) , ( 0,  0,  12.215965  )  , ( 0, 0, 0 ) , 'finger01_L_joint03','finger01_L_joint02')
		addTK17Bone( (-0.029914655, -0.0001108094948, -4.7701619e-06 ) , ( 0,  0,  152.28918  )  , ( 0, 0, 0 ) , 'finger01_L_jointEnd','finger01_L_joint03')
		addTK17Bone( (0.0348319, -0.0022508614, -0.019061903 ) , ( -4.329,  -8.561,  170.719  )  , ( 0, 0, 0 ) , 'finger02_L_joint01','wrist_L_joint')
		addTK17Bone( (-0.05577077, 0, 0 ) , ( -4.5,  0,  14.060472  )  , ( 0, 0, 0 ) , 'finger02_L_joint02','finger02_L_joint01')
		addTK17Bone( (-0.032087836, 0.0012480114, 0 ) , ( 0,  0,  3.4309056  )  , ( 0, 0, 0 ) , 'finger02_L_joint03','finger02_L_joint02')
		addTK17Bone( (-0.025970517, 0.00088519527, 0 ) , ( 0,  0,  -0.473  )  , ( 0, 0, 0 ) , 'finger02_L_joint04','finger02_L_joint03')
		addTK17Bone( (-0.021580048, -0.00015863318, 0 ) , ( 0,  0,  165.822  )  , ( 0, 0, 0 ) , 'finger02_L_jointEnd','finger02_L_joint04')
		addTK17Bone( (0.0367169, -0.005422459, -0.0051491633 ) , ( -4.281,  0.414,  170.043  )  , ( 0, 0, 0 ) , 'finger03_L_joint01','wrist_L_joint')
		addTK17Bone( (-0.055771105, 6.9938806e-06, 0 ) , ( 10,  -1.5,  13.5  )  , ( 0, 0, 0 ) , 'finger03_L_joint02','finger03_L_joint01')
		addTK17Bone( (-0.034229141, 0.0013223231, 0 ) , ( 0,  0,  2.4653971  )  , ( 0, 0, 0 ) , 'finger03_L_joint03','finger03_L_joint02')
		addTK17Bone( (-0.02803468, 0.00073731539, 0 ) , ( 0,  0,  -1.790976  )  , ( 0, 0, 0 ) , 'finger03_L_joint04','finger03_L_joint03')
		addTK17Bone( (-0.0239445, -0.00077033497, 0 ) , ( 0,  0,  165.82193  )  , ( 0, 0, 0 ) , 'finger03_L_jointEnd','finger03_L_joint04')
		addTK17Bone( (0.03571973, -0.0038376555, 0.0076874923 ) , ( -3.575,  8.736,  174.486  )  , ( 0, 0, 0 ) , 'finger04_L_joint01','wrist_L_joint')
		addTK17Bone( (-0.051718585, 0.00098681089, 0 ) , ( 15,  0,  6.607  )  , ( 0, 0, 0 ) , 'finger04_L_joint02','finger04_L_joint01')
		addTK17Bone( (-0.034228556, 0.0013237986, 0 ) , ( 2.2608085e-06,  0,  2.4653971  )  , ( 0, 0, 0 ) , 'finger04_L_joint03','finger04_L_joint02')
		addTK17Bone( (-0.028035164, 0.00073698378, 0 ) , ( 0,  0,  -1.790976  )  , ( 0, 0, 0 ) , 'finger04_L_joint04','finger04_L_joint03')
		addTK17Bone( (-0.025545767, -0.00036946358, 0 ) , ( 1.2091363e-06,  0,  165.82193  )  , ( 0, 0, 0 ) , 'finger04_L_jointEnd','finger04_L_joint04')
		addTK17Bone( (0.03232801, 0.00080252939, 0.018503578 ) , ( -4.538,  19.359,  168.567  )  , ( 0, 0, 0 ) , 'finger05_L_joint01','wrist_L_joint')
		addTK17Bone( (-0.049039204, -0.0063234563, 0.00023499712 ) , ( 24,  -1,  11.717  )  , ( 0, 0, 0 ) , 'finger05_L_joint02','finger05_L_joint01')
		addTK17Bone( (-0.026569683, 0.0010226016, 0 ) , ( 2.0915695e-06,  0,  1  )  , ( 0, 0, 0 ) , 'finger05_L_joint03','finger05_L_joint02')
		addTK17Bone( (-0.020462746, -0.00013862793, 0 ) , ( 4.0113996e-06,  0,  -3.6718934  )  , ( 0, 0, 0 ) , 'finger05_L_joint04','finger05_L_joint03')
		addTK17Bone( (-0.019582551, -0.0017780437, 0 ) , ( 2.6504866e-05,  2.1186415e-06,  165.82193  )  , ( 0, 0, 0 ) , 'finger05_L_jointEnd','finger05_L_joint04')
		#
		#
		addTK17Bone( (-0.026015352, -0.0489839, -0.05556275 ) , ( -79.222,  -28.161,  -95.134  )  , ( 0, 0, 0 ) , 'clavicle_R_joint','neck_joint01')
		addTK17Bone( (0.12511747, 0, 0 ) , ( 0,  0,  19.149282  )  , ( 4.5658915e-05, 6.5000105, 0 ) , 'shoulder_R_joint','clavicle_R_joint')
		addTK17Bone( (0.29089841, 0, 1.7227893e-06 ) , ( 0,  0,  27.265728  )  , ( 0, 0, 0 ) , 'elbow_R_joint','shoulder_R_joint')
		addTK17Bone( (0.11663324, 0, -3.2166761e-06 ) , ( -90,  0,  0  )  , ( 0, 0, 0 ) , 'forearm_R_joint','elbow_R_joint')
		addTK17Bone( (0.15327445, -4.0245804e-06, 0 ) , ( 0, 0, 0 ) , ( 6.690374e-05, 0.00055939768, -0.00030231389 ) , 'wrist_R_joint','forearm_R_joint')
		addTK17Bone( (0.0270408, 0.0090658376, 0.02735349 ) , ( -50,  -33.093,  2.434  )  , ( 0, 0, 0 ) , 'finger01_R_joint01','wrist_R_joint')
		addTK17Bone( (0.044952907, 0.0022870076, 2.7470371e-06 ) , ( 0,  7.5,  13.616971  )  , ( 0, 0, 0 ) , 'finger01_R_joint02','finger01_R_joint01')
		addTK17Bone( (0.02477828, 0.00196381, -3.7278264e-06 ) , ( 0,  0,  12.215965  )  , ( 0, 0, 0 ) , 'finger01_R_joint03','finger01_R_joint02')
		addTK17Bone( (0.029915491, 0.000112142734, 6.1607811e-06 ) , ( 0,  0,  152.28918  )  , ( 0, 0, 0 ) , 'finger01_R_jointEnd','finger01_R_joint03')
		addTK17Bone( (0.034831721, -0.0022508705, 0.019061908 ) , ( -4.329,  -8.561,  -9.281  )  , ( 0, 0, 0 ) , 'finger02_R_joint01','wrist_R_joint')
		addTK17Bone( (0.055770684, 0, 0 ) , ( -4.5,  0,  14.060472  )  , ( 0, 0, 0 ) , 'finger02_R_joint02','finger02_R_joint01')
		addTK17Bone( (0.032088645, -0.0012448726, 0 ) , ( 0,  0,  3.4309056  )  , ( 0, 0, 0 ) , 'finger02_R_joint03','finger02_R_joint02')
		addTK17Bone( (0.025971094, -0.00088127865, 0 ) , ( 0,  0,  -0.473  )  , ( 0, 0, 0 ) , 'finger02_R_joint04','finger02_R_joint03')
		addTK17Bone( (0.021580068, 0.00015606913, 0 ) , ( 0,  0,  165.822  )  , ( 0, 0, 0 ) , 'finger02_R_jointEnd','finger02_R_joint04')
		addTK17Bone( (0.036716808, -0.0054224562, 0.0051491777 ) , ( -4.281,  0.414,  -9.957  )  , ( 0, 0, 0 ) , 'finger03_R_joint01','wrist_R_joint')
		addTK17Bone( (0.05577096, -7.1413347e-06, 0 ) , ( 10,  -1.5,  13.5  )  , ( 0, 0, 0 ) , 'finger03_R_joint02','finger03_R_joint01')
		addTK17Bone( (0.034229431, -0.0013225561, 0 ) , ( 0,  0,  2.4653971  )  , ( 0, 0, 0 ) , 'finger03_R_joint03','finger03_R_joint02')
		addTK17Bone( (0.028035186, -0.0007349978, 0 ) , ( 0,  0,  -1.790976  )  , ( 0, 0, 0 ) , 'finger03_R_joint04','finger03_R_joint03')
		addTK17Bone( (0.023945259, 0.00077390013, 0 ) , ( 0,  0,  165.82193  )  , ( 0, 0, 0 ) , 'finger03_R_jointEnd','finger03_R_joint04')
		addTK17Bone( (0.035719711, -0.0038376434, -0.0076874918 ) , ( -3.575,  8.736,  -5.514  )  , ( 0, 0, 0 ) , 'finger04_R_joint01','wrist_R_joint')
		addTK17Bone( (0.051718544, -0.00098716735, 0 ) , ( 15,  0,  6.607  )  , ( 0, 0, 0 ) , 'finger04_R_joint02','finger04_R_joint01')
		addTK17Bone( (0.034228593, -0.0013246302, 0 ) , ( 0,  0,  2.4653971  )  , ( 0, 0, 0 ) , 'finger04_R_joint03','finger04_R_joint02')
		addTK17Bone( (0.028035874, -0.00073288957, -1.0934416e-06 ) , ( 0,  0,  -1.790976  )  , ( 0, 0, 0 ) , 'finger04_R_joint04','finger04_R_joint03')
		addTK17Bone( (0.025546048, 0.00036992491, 0 ) , ( -1.6947803e-06,  0,  165.82193  )  , ( 0, 0, 0 ) , 'finger04_R_jointEnd','finger04_R_joint04')
		addTK17Bone( (0.032328054, 0.00080254948, -0.018503586 ) , ( -4.538,  19.359,  -11.433  )  , ( 0, 0, 0 ) , 'finger05_R_joint01','wrist_R_joint')
		addTK17Bone( (0.049039245, 0.0063233529, -0.00023505285 ) , ( 24,  -1,  11.717  )  , ( 0, 0, 0 ) , 'finger05_R_joint02','finger05_R_joint01')
		addTK17Bone( (0.026569454, -0.0010208145, 0 ) , ( 0,  0,  1  )  , ( 0, 0, 0 ) , 'finger05_R_joint03','finger05_R_joint02')
		addTK17Bone( (0.020464076, 0.00014253389, -1.7374842e-06 ) , ( 5.722994e-06,  0,  -3.6718934  )  , ( 0, 0, 0 ) , 'finger05_R_joint04','finger05_R_joint03')
		addTK17Bone( (0.019581646, 0.0017750047, 1.3131448e-06 ) , ( 2.5846904e-05,  1.8967539e-06,  165.82193  )  , ( 0, 0, 0 ) , 'finger05_R_jointEnd','finger05_R_joint04')
		addTK17Bone( (0.057289507, 0, 0 ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'neck_jointEnd','neck_joint01')
		addTK17Bone( (0.063364767, 0, 0.0065263966 ) , ( 0,  -9.241,  0  )  , ( 0, 0, 0 ) , 'head_joint01','neck_jointEnd')
		addTK17Bone( ( 0, 0, 0  ) , ( 0, 0, 0 ) , ( 0, 0, 0 ) , 'head_joint02','head_joint01')
		addTK17Bone( (0.1851493, 0, 0 ) , ( 179.75183,  0,  90  )  , ( 0, 0, 0 ) , 'head_jointEnd','head_joint02')
		addTK17Bone( (0.047308434, 0, -0.1194366738 ) , ( 0,  -10.177103,  180  )  , ( 0, 0, -360 ) , 'forehead_joint01','head_joint02')
		addTK17Bone( (-0.024121732, 0, 0 ) , ( 169.57419,  0,  -90  )  , ( 0, 0, 0 ) , 'forehead_jointEnd','forehead_joint01')
		addTK17Bone( (0.021159774, 0.0499147, -0.064211346 ) , ( -25.139944,  62.435097,  157.46184  )  , ( 0, 0, 0 ) , 'cheek_L_joint01','head_joint02')
		addTK17Bone( (0.037414048, 0, 5.5876008e-06 ) , ( 64.889458,  4.8634748,  -79.745918  )  , ( 0, 0, 0 ) , 'cheek_L_jointEnd','cheek_L_joint01')
		addTK17Bone( (0.021158574, -0.049914677, -0.064211331 ) , ( 154.86006,  -62.435097,  22.538168  )  , ( 0, 0, 0 ) , 'cheek_R_joint01','head_joint02')
		addTK17Bone( (-0.03741147, 0, 0 ) , ( 64.889458,  4.8634748,  -79.745918  )  , ( 0, 0, 0 ) , 'cheek_R_jointEnd','cheek_R_joint01')
		addTK17Bone( (0.031983055, 0.0758534, -0.014261107 ) , ( 0,  7.2121744,  180  )  , ( 0, 0, 0 ) , 'ear_L_joint01','head_joint02')
		addTK17Bone( (0.026958896, 0, 0 ) , ( 6.9634686,  0,  -90  )  , ( 0, 0, 0 ) , 'ear_L_jointEnd','ear_L_joint01')
		addTK17Bone( (0.031984262, -0.075853437, -0.014261103 ) , ( -180,  -7.2121744,  0  )  , ( 0, 0, 0 ) , 'ear_R_joint01','head_joint02')
		addTK17Bone( (-0.026961459, 0, 0 ) , ( 6.9634686,  0,  -90  )  , ( 0, 0, 0 ) , 'ear_R_jointEnd','ear_R_joint01')
		addTK17Bone( (0.047308434, 0, -0.1194366738 ) , ( 0,  2.1966031,  0  )  , ( 0, 0, 0 ) , 'nose_joint01','head_joint02')
		addTK17Bone( (-0.037152488, 0, 0 ) , ( 0,  -88.677994,  -180  )  , ( 0, 0, 0 ) , 'nose_joint02','nose_joint01')
		addTK17Bone( (-0.0202144, 0, 0 ) , ( 88.876694,  0,  -90  )  , ( 0, 0, 0 ) , 'nose_jointEnd','nose_joint02')
		addTK17Bone( (-0.011866385, 0.0497831, -0.081294566 ) , ( 67.589127,  47.728825,  -119.3288345  )  , ( 180, 180, -180 ) , 'upper_lip_L_joint01','head_joint02')
		addTK17Bone( (0.036876492, 0, 1.9504012e-06 ) , ( 3.8127766,  33.704464,  11.153666  )  , ( 0, 0, 0 ) , 'upper_lip_L_joint02','upper_lip_L_joint01')
		addTK17Bone( (0.016489189, 0, 0 ) , ( -5.6228004,  -10.385857,  22.867685  )  , ( 0, 0, 0 ) , 'upper_lip_L_joint03','upper_lip_L_joint02')
		addTK17Bone( (0.017326185, 0, 0 ) , ( 91.027107,  2.9025409,  -160.50323  )  , ( 0, 0, 0 ) , 'upper_lip_L_jointEnd','upper_lip_L_joint03')
		addTK17Bone( (-0.011868767, -0.049783133, -0.081294626 ) , ( -112.41087,  -47.728825,  -60.671169  )  , ( 0, 0, 0 ) , 'upper_lip_R_joint01','head_joint02')
		addTK17Bone( (-0.036875825, 0, 0 ) , ( 3.8114159,  33.672421,  11.151284  )  , ( 0, 0, 0 ) , 'upper_lip_R_joint02','upper_lip_R_joint01')
		addTK17Bone( (-0.016338509, 0, 0 ) , ( -5.6099687,  -10.331266,  22.864193  )  , ( 0, 0, 0 ) , 'upper_lip_R_joint03','upper_lip_R_joint02')
		addTK17Bone( (-0.017283283, 0, 0 ) , ( 91.035393,  2.9261374,  -160.50423  )  , ( 0, 0, 0 ) , 'upper_lip_R_jointEnd','upper_lip_R_joint03')
		addTK17Bone( (0.044199962, 0.03, -0.064204641 ) , ( -180,  89.75161,  0  )  , ( 0, 0, 0 ) , 'eye_socket_L_joint','head_joint02')
		addTK17Bone( (0.0542515, 0.0167764, -0.0181003 ) , ( -0.00031110836,  0.52842313,  -100.6724548  )  , ( 0, 0, 0 ) , 'eye_brow_L_joint01','eye_socket_L_joint')
		addTK17Bone( (0.029272685, 0, 0 ) , ( 0.21926138,  -24.609423,  -22.251284  )  , ( 0, 0, 0 ) , 'eye_brow_L_joint02','eye_brow_L_joint01')
		addTK17Bone( (0.013605733, 0, 0 ) , ( 102.89612,  17.151382,  33.765743  )  , ( 0, 0, 0 ) , 'eye_brow_L_jointEnd','eye_brow_L_joint02')
		addTK17Bone( (0.043050896, 0, 0 ) , ( 89.747169,  -3.1793165,  -90.699318  )  , ( 0, 0, 0 ) , 'eye_L_joint','eye_socket_L_joint')
		addTK17Bone( (0.044199962, -0.03, -0.064204641 ) , ( 0,  -89.75161,  -180  )  , ( 0, 0, 0 ) , 'eye_socket_R_joint','head_joint02')
		addTK17Bone( (-0.0542515, -0.0167764, 0.0181003 ) , ( -0.00031125688,  0.52842313,  -100.6724548  )  , ( 0, 0, 0 ) , 'eye_brow_R_joint01','eye_socket_R_joint')
		addTK17Bone( (-0.029272685, 0, 0 ) , ( 0.21926105,  -24.609421,  -22.251284  )  , ( 0, 0, 0 ) , 'eye_brow_R_joint02','eye_brow_R_joint01')
		addTK17Bone( (-0.013605733, 0, 0 ) , ( 102.89612,  17.151382,  33.765743  )  , ( 0, 0, 0 ) , 'eye_brow_R_jointEnd','eye_brow_R_joint02')
		addTK17Bone( (-0.0430509, 0, 0 ) , ( 89.747169,  -3.1793158,  -90.699318  )  , ( 0, 0, 0 ) , 'eye_R_joint','eye_socket_R_joint')
		addTK17Bone( (-0.009535322, 0, -0.018110782 ) , ( 90,  34.172157,  180  )  , ( 360, 0, 0 ) , 'lower_jaw_joint01','head_joint02')
		addTK17Bone( (0.030158687, 0, 0 ) , ( -180,  0,  -22.48103  )  , ( 0, 0, 0 ) , 'lower_jaw_jointEnd','lower_jaw_joint01')
		addTK17Bone( (0.037222072, 0, 0 ) , ( 0,  0,  19.701273  )  , ( 0, 0, 0 ) , 'chin_joint01','lower_jaw_jointEnd')
		addTK17Bone( (0.04334604, 0, 0 ) , ( -13.894247,  90,  0  )  , ( 0, 0, 0 ) , 'chin_jointEnd','chin_joint01')
		addTK17Bone( (0.052382234, -0.040051937, -0.04697606 ) , ( -91.485771,  34.487484,  121.30071  )  , ( -180, 180, 180 ) , 'lower_lip_R_joint01','lower_jaw_joint01')
		addTK17Bone( (-0.033197936, 0, 0 ) , ( -0.53817004,  -4.9634919,  14.401619  )  , ( 0, 0, 0 ) , 'lower_lip_R_joint02','lower_lip_R_joint01')
		addTK17Bone( (-0.015946811, 0, 0 ) , ( 1.0961326,  -3.0563121,  22.346766  )  , ( 0, 0, 0 ) , 'lower_lip_R_joint03','lower_lip_R_joint02')
		addTK17Bone( (-0.016967295, 0, 0 ) , ( 88.164955,  -5.4077697,  -161.22426  )  , ( 0, 0, 0 ) , 'lower_lip_R_jointEnd','lower_lip_R_joint03')
		addTK17Bone( (0.052383676, -0.040050954, 0.0469761 ) , ( -91.485771,  34.487484,  -58.699287  )  , ( 0, 0, 0 ) , 'lower_lip_L_joint01','lower_jaw_joint01')
		addTK17Bone( (0.033197861, 0, 2.1324595e-06 ) , ( -0.53817004,  -4.9634919,  14.401619  )  , ( 0, 0, 0 ) , 'lower_lip_L_joint02','lower_lip_L_joint01')
		addTK17Bone( (0.015946407, 0, -8.3578261e-06 ) , ( 1.0961326,  -3.0563121,  22.346766  )  , ( 0, 0, 0 ) , 'lower_lip_L_joint03','lower_lip_L_joint02')
		addTK17Bone( (0.016967608, 0, 1.9150691e-06 ) , ( 88.164955,  -5.4077697,  -161.22426  )  , ( 0, 0, 0 ) , 'lower_lip_L_jointEnd','lower_lip_L_joint03')
		#
		#addTK17Bone( (0.038907621, -0.0032027592, 0 ) , ( 0,0,0 ) , ( 124.17216, -90, 0  ) , 'tongue_pos_group','lower_jaw_joint01')
		#addTK17Bone( (0, 0, 0 ) , ( 90, -43.60162, 90 ) , ( 0, 0, 15  ) , 'tongue_joint01','tongue_pos_group')
		#addTK17Bone( (0.013234313, 0, 0 ) , ( 0, 0, 1.4552643 ) , ( 0, 0, 0  ) , 'tongue_joint02','tongue_joint01')
		#addTK17Bone( (0.013178268, 0, 0 ) , ( 0, 0, 28.636478 ) , ( 0, 0, 0  ) , 'tongue_joint03','tongue_joint02')
		#addTK17Bone( (0.012801229, 0, 0 ) , ( 0, 0, 15.6187315 ) , ( 0, 0, 0  ) , 'tongue_joint04','tongue_joint03')
		#addTK17Bone( (0.011361554, 0, 0 ) , ( 0, 0, 7.49264 ) , ( 0, 0, 0  ) , 'tongue_joint05','tongue_joint04')
		#addTK17Bone( (0.013714936, 0, 0 ) , ( 155.4445, -90, 0 ) , ( 0, 0, 0  ) , 'tongue_jointEnd','tongue_joint05')
		#
		#
		#IGNORE IT for now
		#addTK17Transform( ( 0, 1.52488, -0.031850725 ) , ( 180, 0.2126652, 90 ) , ( 0, 0, 0  ) , 'spine_ikHandle','') #spine_ikHandle
		#
		#addTK17Bone( (0, 0, 0 ) , ( 0,0,0 ) , (0, 0, 0  ) , 'tip_toe_L_group','root')
		#addTK17Bone( (-0.00016799147, 0.0113661, 0.241317 ) , ( 0,0,0 ) , (0, 0, 0  ) , 'tip_toe_L_group_pivot','root')
		#addTK17Bone( ( 0.00019925147, 0, 0.000105514795 ) , ( 0,0,0 ) , (0, 0, 0  ) , 'ball_L_group','tip_toe_L_group')
		#addTK17Bone( ( -0.00016800423, 0.0160358, 0.14387479 ) , ( 0,0,0 ) , (0, 0, 0  ) , 'ball_L_group_pivot','ball_L_group')
		#addTK17Bone( ( 0, 0,0 ) , ( 0,0,0 ) , (0, 0, 0  ) , 'leg_L_ikHandle','ball_L_group')
		#addTK17Bone( (  -0.00016801599, 0.0903118, 0.0416234 ) , ( 0,0,0 ) , (0, 0, 0  ) , 'leg_L_ikHandle_pivot','leg_L_ikHandle')
		#addTK17Bone( (0, 0, 0) , ( 0,0,0 ) , (0, 0, 0  ) , '_mouth_L_fix_group','_head_joint02')
		#addTK17Bone( (0, 0, 0) , ( 0,0,0 ) , (0, 0, 0  ) , '_mouth_R_fix_group','_head_joint02')
	#

def addBonesFromCtkAnimSkeleton(path_to_file):
	output= ""
	joints_dict = OrderedDict()
	parenting_dict = {}
	np.set_printoptions(precision=6)
	np.set_printoptions(suppress=True)
	
	#G:\\rv\\z\\TheKlub17_fresh\\Toolz\\CollaTKane\\Resources\\AnimSkeleton(highheel01_on).txt
	#C:\\Users\\Neon\\Desktop\\AnimSkeleton(custom_output).txt
	with open(path_to_file) as f:
		matrix_lines = [line.lstrip().rstrip() for line in f]
	
	
	script_file = os.path.realpath(__file__)
	directory = os.path.dirname(script_file)
	path_to_file_joints_dump = os.path.join(directory, "joints_dump.txt")
	path_to_file_joints_parents_dump = os.path.join(directory, "joints_parents_dump.txt")
	
	with open(path_to_file_joints_dump) as f:
		joint_lines = [line.rstrip() for line in f]
	
	#extract joint - parent relation
	with open(path_to_file_joints_parents_dump) as f:
		parenting_lines = [line.rstrip() for line in f]
	
	#lets build parenting relationship
	for idx,row in enumerate(parenting_lines):
		rowsplit = row.split(" ")
		parenting_dict[rowsplit[0]]=rowsplit[1]
	
	
	for idx,row in enumerate(matrix_lines):
		if len(row.strip())>0:
			rowsplit = row.split(" ", 1)
			joint = rowsplit[0]
			inv_matrix_text = rowsplit[1]
			inv_matrix = np.fromstring(inv_matrix_text, dtype=np.double, sep=' ')
			inv_matrix = inv_matrix.T.reshape(4,4)
			global_matrix = np.linalg.inv(inv_matrix) 
			data = {'joint':joint, 'global_matrix' : global_matrix, 'parent': parenting_dict[joint], 'local_matrix':None }
			joints_dict[joint] = data
	
	
	#init - local matrix for root joint is same as global
	joints_dict['root']['local_matrix'] = joints_dict['root']['global_matrix'] 
	
	
	#recalculate local matrix for all joints, as local * parent_global
	for idx,joint in enumerate(joints_dict):
		if joint not in 'root':
			parent_name = joints_dict[joint]['parent']
			print(joint+": "+parent_name)
			parent_matrix = joints_dict[parent_name]['global_matrix']
			joints_dict[joint]['local_matrix'] = np.matmul(joints_dict[joint]['global_matrix'] ,np.linalg.inv(parent_matrix) ) #
	#
	#
	m = joints_dict["spine_joint02"]["local_matrix"].T
	blendmat = mathutils.Matrix(m)
	loc, rot, sca = blendmat.decompose()
	print("mat is: ")
	print(loc)
	for idx,joint in enumerate(joints_dict):
		#if joint not in 'root':
		parent_name = joints_dict[joint]['parent']
		#print("["+joint+": "+parent_name+"]")
		local_matrix = joints_dict[joint]['local_matrix'].T
		print (local_matrix)
		blendmat = mathutils.Matrix(local_matrix)
		loc, rot, sca = blendmat.decompose()
		rot_euler = rot.to_euler()
		rx = math.degrees(rot_euler.x)
		ry = math.degrees(rot_euler.y)
		rz = math.degrees(rot_euler.z)
		#print(loc)
		#print("adding:"+joint+"+<"+parent_name+ " = "+str(loc.x)+", "+str(loc.y)+ ", "+str(loc.z)+ " <> "+str(rx)+", "+str(ry)+", "+ str(rz))
		if joint in ['root']:
			addTK17Bone(   (0, 0, 0 )  ,   ( 0, 0, 0 ),  ( rx, ry, rz )    , joint,"")
		else:
			print("adding ["+joint+": "+parent_name+"]")
			addTK17Bone(   (loc)  ,   ( 0, 0, 0 ),  ( rx, ry, rz )    , joint, parent_name)
		#



def pre_import_armature():
	for o in bpy.context.scene.objects:
		o.hide = False
	#
	bpy.ops.object.select_all(action='DESELECT')
	#
	armature = bpy.context.scene.objects.get("Armature")
	if armature is not None:
		armature.select = True
	#
	root_empty = bpy.context.scene.objects.get("root")
	select_children(root_empty)
	bpy.ops.object.delete()
	#
	bpy.ops.object.select_all(action='DESELECT')



def post_import_armature():
	#bpy.ops.object.mode_set(mode="OBJECT")
	#
	#
	#
	scene = bpy.context.scene
	#Create armature and armature object
	armature = bpy.data.armatures.new('Armature')
	armature_object = bpy.data.objects.new('Armature', armature)
	armature_object.layers[0] = True
	armature_object.layers[1] = True
	#Link armature object to our scene
	bpy.context.scene.objects.link(armature_object)
	#Make a coding shortcut
	armature_data = bpy.data.objects['Armature']
	armature_data.data.name = "Armature"
	#Must make armature active and in edit mode to create a bone
	bpy.context.scene.objects.active = armature_data
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	armature_matrix_world = armature_data.matrix_world
	#
	for ob in bpy.data.objects:
		#print ("object: " + ob.name)
		if ob.type == 'EMPTY' and "corrector" not in ob.name:
			editBone = bpy.context.object.data.edit_bones.new(ob.name)
			parentsArray  = parentsForNode(ob)
			head_joint01_child = len([i for i in parentsArray if "head_joint01" in i]) > 0
			ankles_child = len([i for i in parentsArray if "ankle" in i]) > 0
			breast_child = len([i for i in parentsArray if "breast" in i]) > 0
			upper_lip_R_joint01_child = len([i for i in parentsArray if "upper_lip_R_joint01" in i]) > 0
			lower_lip_R_joint01_child = len([i for i in parentsArray if "lower_lip_R_joint01" in i]) > 0
			upper_lip_L_joint01_child = len([i for i in parentsArray if "upper_lip_L_joint01" in i]) > 0
			lower_lip_L_joint01_child = len([i for i in parentsArray if "lower_lip_L_joint01" in i]) > 0		
			editBone.head = Vector([0, 0, 0])
			length = 0.1
			if "_jointEnd" in ob.name:
				length = 0.02		
			if "anus" in ob.name:
				length = 0.06				
			if "finger" in ob.name:
				length = 0.025
			if "shoulder" in ob.name:
				length = 0.25
			if "forearm" in ob.name:
				length = 0.13			
			if "hip" in ob.name or "knee" in ob.name:
				length = 0.4			
			if "wrist" in ob.name:
				length = 0.04		
			if "finger" in ob.name and "joint01" in ob.name:
				length = 0.04				
			if head_joint01_child:
				length=0.02
			if ankles_child:
				length=0.04
			if breast_child or "breast_" in ob.name:
				length=0.065			
			if "penis" in ob.name or "testicles" in ob.name or "vagina" in ob.name:
				length = 0.03		
			if ob.name in  ["upper_lip_R_joint01", "lower_lip_R_joint01", "upper_lip_L_joint01", "lower_lip_L_joint01", "cheek_R_joint01", "cheek_L_joint01" ]:
				length = 0.03			
			if upper_lip_R_joint01_child or lower_lip_R_joint01_child or upper_lip_L_joint01_child or lower_lip_L_joint01_child:
				length = 0.015
			if ob.name in ["neck_joint01", "neck_jointEnd", "spine_jointEnd", "head_joint01"]:
				length = 0.05
			if ob.name in ["nose_joint01"]:
				length = 0.035
			if ob.name in ["butt_L_joint01","butt_R_joint01","rib_R_joint01","rib_L_joint01", "stomach_joint01" ]:
				length = 0.06			
			if ob.name in ["nipple_R_joint01","nipple_R_jointEnd","nipple_L_joint01","nipple_L_jointEnd", "breast_deform03_R_jointEnd","breast_deform03_L_jointEnd","breast_deform02_R_jointEnd","breast_deform02_L_jointEnd","breast_deform01_L_jointEnd","breast_deform01_R_jointEnd" ]:
				length = 0.01						
			if "tongue" in ob.name:
				length = 0.012			
			editBone.tail = Vector([0, 0, length])
			editBone.matrix =  armature_matrix_world.inverted() * ob.matrix_world
			if ob.get("isFlipped") is not None and ob["isFlipped"] == True :
				editBone.length *= -1
				editBone["isFlipped"] = True
			else:
				editBone["isFlipped"] = False
			if editBone.name == "wrist_L_joint":
				editBone.length = -editBone.length;
			editBone["iRoll"] = math.degrees(editBone.roll)
			if "_jointEnd" in ob.name:
				if ob.name in ["spine_jointEnd", "neck_jointEnd", "lower_jaw_jointEnd", "forehead_jointEnd", "head_jointEnd"] :
					pass
				else:
					editBone.use_deform = False
					editBone.layers[1] = True
					editBone.layers[0] = False
			scene.update()
	#
	#
	#
	# lets create the parenting, we need to loop again
	for ob in bpy.data.objects:
		#print ("object: " + ob.name)
		if ob.type == 'EMPTY':
			editBone = bpy.context.object.data.edit_bones[ob.name]
			parent = ob.parent
			if parent is not None:
				editBone.parent = bpy.context.object.data.edit_bones[parent.name]
				#print ("object none: " + ob.name)
	#
	#TK17 to blender axis conversion	
	from bpy_extras.io_utils import axis_conversion
	context = bpy.context
	m = axis_conversion(
			from_forward='Z',
			from_up='Y',
			to_forward='-Y',
			to_up='Z'
			).to_4x4()
	#
	root_empty_object = bpy.data.objects["root"]
	#root_empty_object.matrix_world = m * root_empty_object.matrix_world
	#armature_object.matrix_world = m * armature_object.matrix_world
	#
	#hide all children of a node, including the node 
	hide_children(bpy.data.objects["root"])
	#
	#lets show back some nodes
	#bpy.data.objects["root"].hide = False
	#bpy.data.objects["clavicle_L_joint"].hide = False
	#bpy.data.objects["clavicle_L_joint"].hide = False
	#bpy.data.objects["neck_jointEnd"].hide = False
	#bpy.data.objects["nose_joint01"].hide = False
	#bpy.data.objects["forehead_joint01"].hide = False
	#bpy.data.objects["tongue_joint01"].hide = False
	#elbow = bpy.context.object.data.edit_bones["elbow_L_joint"]
	#bpy.data.objects["hip_L_joint"].hide = False
	#
	bpy.data.objects["root"].location.z= 0.98419
	bpy.data.objects["root"].location.y= 0.031404294
	bpy.data.objects["Armature"].location.z= 0.98419
	bpy.data.objects["Armature"].location.y= 0.031404294
	#bpy.data.objects["Armature"].rotation_euler.x += math.radians(7.1250162)
	#
	bpy.data.objects["Armature"].rotation_euler.z= math.radians(-90)
	bpy.data.objects["root"].rotation_euler.x= math.radians(90 + 7.1250162)
	bpy.data.objects["root"].rotation_euler.y= 0
	bpy.data.objects["root"].rotation_euler.z= 0
	#armature.z = -90
	#root.x= 90 + 7.1250162
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	#
	armature_object.select = True
	bpy.context.scene.objects.active = armature_object
	bpy.ops.object.transform_apply(rotation = True)
	#armature_object.layers[1] = True
	bpy.data.armatures['Armature'].layers[0] = True
	bpy.data.armatures['Armature'].layers[1] = True
	context.area.tag_redraw()
	bpy.ops.wm.redraw_timer(type='DRAW', iterations=1)

	

