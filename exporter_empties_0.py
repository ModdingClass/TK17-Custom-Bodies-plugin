import sys
import os
from math import radians
from math import degrees
from os.path import join

from .dictionaries import *
from . import globals

def export_joints_fix(exportfolderpath, bodyNo):
	pyBlock_MeshDataJointsArray = []
	
	adjusted_bones=""
	adjusted_bones =":Person\" + :person + \"Anim:Model01:root.SNode? . {\n"
	adjusted_bones = adjusted_bones +"\t.Translation (0f, 0.98419f, -0.031404294f);\n"
	adjusted_bones = adjusted_bones +"\t.Rotation (90f, -7.1250162f, 90f);\n};\n"
	#
	pyBlock_MeshDataJointsArray.append("TJoint :"+bpy.data.objects["_root"]["localName"])
	#bpy.data.armatures["Armature"].edit_bones.keys()


	for empty in bpy.data.objects:
		if  empty.type != 'EMPTY':
			continue
		if  empty.get("exportAsVillaJoint") is None or empty["exportAsVillaJoint"] == False :
			continue
		if empty.name!="_root":
			snippet = ":Person\" + :person + \"Anim:Model01:"
			snippet = snippet+empty.name[1:]
			snippet = snippet + ".SNode? . {\n";
			snippet = snippet+ "\t.JointOrientation ("   +" {:.6f}f,".format(degrees(empty.rotation_euler.y)+ 0)    +" {:.6f}f,".format(degrees(empty.rotation_euler.z)+ 0)    +" {:.6f}f".format(degrees(empty.rotation_euler.x)+ 0)   +" );\n"
			snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(empty.location.y+ 0)    +" {:.6f}f,".format(empty.location.z+ 0)    +" {:.6f}f".format(empty.location.x+ 0)   +" );\n"	
			snippet = snippet+ "\t.Rotation ( 0.0f, 0.0f, 0.0f );\n"
			snippet = snippet+ "};\n"
			snippet = snippet+""
			#print (snippet)
			adjusted_bones = adjusted_bones+snippet
			pyBlock_MeshDataJointsArray.append("TJoint :"+empty["localName"])
		#
	#
	#
	#Smouth_L_fix_group
	#Smouth_R_fix_group
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	print("joints saved to: "+file_path)
	f = open(file_path, 'a')
	f.write(adjusted_bones)
	f.close()
	#
	jointTemplate =''
	jointTemplate= '''
TJoint :custom_{jointName} . {{
	TNode.SNode SJoint :custom_S{jointName};
	TNode.Parent TJoint :{parentName};
	Object.Name "{jointName}";
}};
SJoint :custom_S{jointName} . {{
	SJoint.JointOrientation Vector3f( {rx}, {ry}, {rz} );
	SSimpleTransform.Translation Vector3f( {tx}, {ty}, {tz} );
	SSimpleTransform.Rotation Vector3f( 0, 0, 0 );
	Object.Name "S{jointName}";
}};
	'''

	#My name is {fname}, I'm {age}".format(fname = "John", age = 36)
	extra_bones = ''
	snippet = ''

	for empty in bpy.data.objects:
		if  empty.type != 'EMPTY':
			continue
		if  empty.get("exportAsVillaJoint") is None or empty["exportAsVillaJoint"] == False :
			continue
		if  empty.get("isCustomVillaJoint") is None or empty["isCustomVillaJoint"] == False :
			continue		
		txs="{:.6f}".format(empty.location.y+ 0)
		tys="{:.6f}".format(empty.location.z+ 0)
		tzs="{:.6f}".format(empty.location.x+ 0)
		rxs="{:.6f}".format(degrees(empty.rotation_euler.y)+ 0)
		rys="{:.6f}".format(degrees(empty.rotation_euler.z)+ 0)
		rzs="{:.6f}".format(degrees(empty.rotation_euler.x)+ 0)		
		#parentName=empty.parent.name[1:] #need to remove the _ from parent
		#parentName = joint_to_local_dict[parentName]
		jointName = empty.name[1:]
		parentName = empty.parent["localName"]
		snippet = jointTemplate.format(jointName=jointName,parentName=parentName, tx=txs, ty=tys, tz=tzs, rx=rxs, ry=rys, rz=rzs )
		snippet = snippet+ "\n"
		snippet = snippet+"\n"
		extra_bones = extra_bones+snippet
		pyBlock_MeshDataJointsArray.append("TJoint :"+empty["localName"])
		#
	file_path = exportfolderpath+'bsBlocks/extra_joints.bs_block'
	print("extra joints saved to: "+file_path)
	f = open(file_path, 'w')
	f.write(extra_bones)
	f.close()			
	#
	#
	#
	
	file_path = exportfolderpath+'bsBlocks/part3.2_1_content_MeshDataJointArray2.bs_block'
	print("JointArray saved to: "+file_path)
	f = open(file_path, 'w')
	f.write(', '.join(pyBlock_MeshDataJointsArray))
	f.close()
	


	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)



