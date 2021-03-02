bl_info = {
	"name": "Klub17 Armature Importer",
	"description": "Klub17 Armature Importer",
	"author": "hfg2",
	"version": (0, 1, 6),
	"blender": (2, 7, 9),
	"api": 51232,
	"location": "Toolpanel > Misc",
	"warning": "This code is still very much alpha!",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Import-Export"
}
import collections
import os
import sys
import subprocess
import shutil
import zipfile
import inspect
import math
import threading
import time
import bmesh
import bpy
import mathutils
import math
import importlib
from mathutils import Vector
from bpy.app.handlers import persistent
from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator
import bpy.utils.previews
import re
from tempfile import NamedTemporaryFile

import decimal
from .h5m import *
from .dictionaries import *
from .armature import *
from .parent_to_child_adjust_bone_length import *
from .rename_bones_in_armature import *
from .rename_bones_in_armature_back import *
from .symmetry_list import *
from .correct_final_rolls import *
from .armature_to_empty_conversion import *
from .exporter_empties_0 import *
from .exporter_mouth_fix import *
from .exporter_arms_fix import *
from .exporter_legs_fix import *
from .exporter_genitals_fix import *
from .exporter_breasts_fix import *
from .recalculate_BindInvMatrix import *
from .recalculate_BindInvMatrix_CTK import *
from .face_default import *
from .fake_bones import *
from .clear_armature_rotation import *
from .tools_message_box import *
from .exporter_body import *
from .importer_g3f import *
from .importer_g3f_morphs import *
from .exporter_fake_bones import *
from .exporter_z_cleanup_values import *
from .exporter_boilerplate import *
from .tools_duplicate_object_remove_mats_shapekeys import *


from bpy.app.handlers import persistent
from bpy.props import *
import mathutils
import bpy_extras.io_utils
from math import *
from mathutils import *
from .configobj import ConfigObj


if "bpy" in locals():
	import imp
	imp.reload(dictionaries)
	imp.reload(h5m)
	imp.reload(armature)
	imp.reload(parent_to_child_adjust_bone_length)
	imp.reload(rename_bones_in_armature)
	imp.reload(rename_bones_in_armature_back)
	imp.reload(symmetry_list)
	imp.reload(correct_final_rolls)
	imp.reload(armature_to_empty_conversion)
	imp.reload(exporter_empties_0)
	imp.reload(exporter_mouth_fix)
	imp.reload(exporter_arms_fix)
	imp.reload(exporter_legs_fix)
	imp.reload(exporter_genitals_fix)	
	imp.reload(exporter_breasts_fix)
	imp.reload(recalculate_BindInvMatrix)
	imp.reload(recalculate_BindInvMatrix_CTK)
	imp.reload(face_default)
	imp.reload(fake_bones)
	imp.reload(clear_armature_rotation)
	imp.reload(tools_message_box)
	imp.reload(exporter_body)
	imp.reload(importer_g3f)
	imp.reload(importer_g3f_morphs)
	imp.reload(exporter_fake_bones)
	imp.reload(exporter_z_cleanup_values)
	imp.reload(exporter_boilerplate)
	imp.reload(tools_duplicate_object_remove_mats_shapekeys)
	
	print("Reloaded multifiles")
else:
	from . import dictionaries
	from . import h5m
	from . import armature
	from . import parent_to_child_adjust_bone_length
	from . import rename_bones_in_armature
	from . import rename_bones_in_armature_back
	from . import symmetry_list
	from . import correct_final_rolls
	from . import armature_to_empty_conversion
	from . import exporter_empties_0
	from . import exporter_mouth_fix
	from . import exporter_arms_fix
	from . import exporter_legs_fix
	from . import exporter_genitals_fix	
	from . import exporter_breasts_fix	
	from . import recalculate_BindInvMatrix
	from . import recalculate_BindInvMatrix_CTK
	from . import face_default
	from . import fake_bones
	from . import clear_armature_rotation
	from . import tools_message_box
	from . import exporter_body
	from . import importer_g3f_morphs
	from . import exporter_fake_bones
	from . import exporter_z_cleanup_values
	from . import exporter_boilerplate
	from . import tools_duplicate_object_remove_mats_shapekeys
	
	
	print("Imported multifiles")

version = 'v%s.%s'%(bl_info['version'][0],bl_info['version'][1])




def delete_hierarchy(parent_obj_name):
	bpy.ops.object.select_all(action='DESELECT')
	obj = bpy.data.objects[parent_obj_name]
	obj.animation_data_clear()
	names = set()
	# Go over all the objects in the hierarchy like @zeffi suggested:
	def get_child_names(obj):
		for child in obj.children:
			names.add(child.name)
			if child.children:
				get_child_names(child)

	get_child_names(obj)

	print(names)
	objects = bpy.data.objects
	setattr(obj, 'select', True)
	[setattr(objects[n], 'select', True) for n in names]
	# Remove the animation from the all the child objects
	for child_name in names:
		bpy.data.objects[child_name].animation_data_clear()

	result = bpy.ops.object.delete()
	if result == {'FINISHED'}:
		print ("Successfully deleted object")
	else:
		print ("Could not delete object")



def load_config2(self,context) :
	scene = bpy.context.scene
	
## addon configuration file (config)
def load_config(self,context) :
	print ('load_config -> ()')
	scene = bpy.context.scene
	#tkarmature is a new object created in scene context 
	tkarmature = bpy.context.scene.tkarmature
	print('opening file: %s'%tkarmature.filepath)
	
	
def save_config(self,context) :
	print ('save_config -> ()')
	scene = bpy.context.scene
	tkarmature = bpy.context.scene.tkarmature
	print('opening file: %s'%tkarmature.filepath)

	
## ADDON INTERFACE CLASS
def ui_tab(elm,tab=0.05) :
	split = elm.split(tab)
	col = split.column()
	return split.column()

## MAIN CLASS
class TKARMATURE_vars(bpy.types.PropertyGroup) :
	## file ops
	def update_func_exportfolderpath(self, context):
		#self.exportfolderpath = os.path.join(self.exportfolderpath,"")
		new_value = os.path.join(self.exportfolderpath,"")
		if new_value == self.exportfolderpath:
			pass
		else:
			self.exportfolderpath = new_value
		print("exportfolderpath: ", self.exportfolderpath)
	
	exportfolderpath =  bpy.props.StringProperty(name="exportfolderpath", default='',subtype='DIR_PATH', update=update_func_exportfolderpath)
	
	filepath =  bpy.props.StringProperty(name="filepath", default='',subtype='FILE_PATH')
	filepath_h5m =  bpy.props.StringProperty(name="filepath_h5m", default='',subtype='FILE_PATH')
	exportfolderpath =  bpy.props.StringProperty(name="exportfolderpath", default='',subtype='DIR_PATH', update=update_func_exportfolderpath)
	bodyNo = bpy.props.StringProperty(name="bodyNo",description="Body No", default="01")
	dontExportJointEnds = bpy.props.BoolProperty(name="dontExportJointEnds", description="Weightless jointEnds are not exported",	default=True)




class ImporterPanel(bpy.types.Panel):
	"""Creates a Panel in the Tool Shelf"""
	bl_label = "Importer"
	bl_idname = "Importer Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "TK17 Body"
	def draw(self,context):
		layout=self.layout
		box = layout.box()
		scene=context.scene
		tkarmature  = scene.tkarmature
		#
		row=box.row(align=True)
		row.operator('tkarmature.create_armature',text='New Hardcoded Armature(F)',icon='OUTLINER_OB_ARMATURE')
		row.operator('tkarmature.import_armature',text='Import CTK Armature',icon='OUTLINER_OB_ARMATURE')
		row.operator('tkarmature.fake',text='              ')
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')
		row.operator('test.import_g3f_body',text='Import G3F body',icon='OBJECT_DATA')	
		row.operator('tkarmature.import_g3f_morph',text='Import G3F morph',icon='MOD_MASK')			
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')
		row.operator('test.import_generic_body',text='Import generic body',icon='OBJECT_DATA')	
		row.operator('tkarmature.fake',text='              ')
		
		

class ToolsPanel(bpy.types.Panel):
	"""Creates a Panel in the Tool Shelf"""
	bl_label = "Tools"
	bl_idname = "Tools Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "TK17 Body"
	def draw(self,context):
		layout=self.layout
		box = layout.box()
		scene=context.scene
		tkarmature  = scene.tkarmature
		row=box.row(align=True)
		row.operator('tkarmature.rename_bones',text='Rename bones')
		row.operator('tkarmature.adjust_bones',text='Adjust parent bones to child')
		row.operator('tkarmature.fix_symmetry',text='Fix Symmetry',icon='MOD_MIRROR')
		row=box.row(align=True)
		row.operator('tkarmature.apply_armature_rotation',text='Apply Rotation')	
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.restore_tk_matrix',text='Restore Selected Bones')
		box.separator()
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.clone_as_weighted_object',text='Make Weighted Obj')
		row.operator('tkarmature.adjust_rig_to_shape',text='Adjust Rig to G3F Body',icon_value=custom_icons["wand_icon"].icon_id)
		
		#row.operator('tkarmature.fake',text='              ')
		#row=box.row(align=True)
		#row.operator('tkarmature.fake',text='              ') 
		#row.operator('tkarmature.fake',text='              ')
		#row.operator('tkarmature.add_fake_bones',text='Add Fake Bones')


class ConstraintsPanel(bpy.types.Panel):
	"""Creates a Panel in the Tool Shelf"""
	bl_label = "Constraints and IKs"
	bl_idname = "Constraints Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "TK17 Body"
	def draw(self,context):
		layout=self.layout
		box = layout.box()
		scene=context.scene
		tkarmature  = scene.tkarmature
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.add_legs_ik',text='Legs IK',icon='POSE_DATA')
		row.operator('tkarmature.add_finger_hand_close_constraints',text='Finger Constraints',icon='CONSTRAINT_BONE')
		

class FakeBonesPanel(bpy.types.Panel):
	"""Creates a Panel in the Tool Shelf"""
	bl_label = "Fake Bones"
	bl_idname = "Fake Bones Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "TK17 Body"
	def draw(self,context):
		layout=self.layout
		box = layout.box()
		scene=context.scene
		tkarmature  = scene.tkarmature
		row=box.row(align=True)
		row.operator('tkarmature.add_fake_bones',text='Add Fake Bones',icon='PMARKER')
		row.operator('tkarmature.remove_fake_bones',text='Remove Fake Bones',icon='PMARKER')
		row.operator('tkarmature.fake',text='              ')
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.export_fake_bones',text='Export Fake Bones')
		row=box.row()
		row.separator()
		#row.operator('test.open_filebrowser',text='Import Blenda body',icon='OBJECT_DATA')	
		row.prop(tkarmature,'dontExportJointEnds',text="Dont export jointEnds")
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.fake',text='              ')
		


class ExporterPanel(bpy.types.Panel):
	"""Creates a Panel in the Tool Shelf"""
	bl_label = "Exporter"
	bl_idname = "Exporter Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "TK17 Body"
	def draw(self,context):
		layout=self.layout
		box = layout.box()
		scene=context.scene
		tkarmature  = scene.tkarmature
		row=box.row(align=True)
		#row.operator('tkarmature.correct_final_rolls',text='Correct Rolls',icon='MODIFIER')
		row.operator('tkarmature.export_armature_to_empties',text='Armature to Empties',icon='OUTLINER_OB_EMPTY')
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.export_empties_to_files',text='Export Empties',icon='EXPORT')		
		#box.row().separator()
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')		
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.export_inverse_bind_matrix',text='Export InvBindMat',icon_value=custom_icons["matrix_icon"].icon_id)		
		#box.row().separator()
		row=box.row(align=True)
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.fake',text='              ')
		row.operator('tkarmature.export_body',text='Export (F)Body Mesh', icon='TIME')			
		row=box.row()
		subbox_exporter=row.box()
		subbox_row = subbox_exporter.row()
		icon='FILE_FOLDER'
		subbox_row.label(text='Folder location:',icon=icon)
		subbox_row = subbox_exporter.row()
		subbox_row.prop(tkarmature,'exportfolderpath',text='')		
		subbox_row = subbox_exporter.row()
		#subbox_row.label(text='Body#:',icon='QUESTION')
		subbox_row.prop(tkarmature,'bodyNo',text='Body#')



			

class OT_fake(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.fake"
	bl_label = ""

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		return {'FINISHED'}


class OT_add_legs_ik(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.add_legs_ik"
	bl_label = ""
	bl_description = "Add IK to the legs. Useful for posing and creating inverse bind matrix for high heels poses"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		ShowMessageBox("Not implemented", "Warning", 'INFO')
		return {'FINISHED'}		
		
class OT_add_finger_hand_close_constraints(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.add_finger_hand_close_constraints"
	bl_label = ""
	bl_description = "Add finger constraints useful for hand closing"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		ShowMessageBox("Not implemented", "Warning", 'INFO')
		return {'FINISHED'}			


class OT_correct_final_rolls(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.correct_final_rolls"
	bl_label = ""
	bl_description = "Add a required -90 rotation to the armature before exporting"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		armature_object = bpy.data.objects["Armature"]
		fix_rolls(armature_object)
		return {'FINISHED'}
		
		
		

class OT_adjust_rig_to_shape(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.adjust_rig_to_shape"
	bl_label = ""
	bl_description = "Adjust armature to shape of the custom g3f body."

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		
		script_file = os.path.realpath(__file__)
		directory = os.path.dirname(script_file)
		
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_0_init_vertex_groups.py")).read())
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_1_functions.py")).read())
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_3_start_boilerplate.py")).read())
		#
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_4_calculate_body.py")).read())
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_4_calculate_head.py")).read())
		#
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_5_preinit_boilerplate.py")).read())
		#
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_5_run_body.py")).read())
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_5_run_head.py")).read())
		#
		exec(open(os.path.join(directory,"g3f","script_autofix_armature_9_end_boilerplate.py")).read())
		return {'FINISHED'}		

		
class OT_clone_as_weighted_object(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.clone_as_weighted_object"
	bl_label = ""
	bl_description = "Duplicate an object but clears materials, shapekeys and modifiers from it. \nUseful to make a copy of the object and keep the weights for later use."

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		duplicate_object_keep_only_VG()
		return {'FINISHED'}		


class OT_apply_armature_rotation(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.apply_armature_rotation"
	bl_label = ""
	bl_description = "Removes any rotation applied to armature so editing is not bugged"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		apply_armature_rotation()
		return {'FINISHED'}		

class OT_restore_bone_tk_matrix(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.restore_tk_matrix"
	bl_label = ""
	bl_description = "Restore selected bones' matrix"
	
	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		ob=context.active_object
		armature_matrix_world = ob.matrix_world
		bpy.ops.object.mode_set( mode = 'EDIT' , toggle=False)
		#
		mirror_x_flag = bpy.data.armatures[ob.data.name].use_mirror_x
		bpy.data.armatures[ob.data.name].use_mirror_x = False
		#
		for editBone in ob.data.edit_bones:
			if not editBone.select:continue
			editBone.use_connect = False
			if editBone.get("originalHead") is not None:
				editBone.head = editBone["originalHead"]
			if editBone.get("originalTail") is not None:
				editBone.tail = editBone["originalTail"]
			if editBone.get("originalRoll") is not None:
				editBone.roll = editBone["originalRoll"]
			#matr=bone["originalMatrix"] #"orig o b.pose.bones[bone.name].hfg_bone.tk_matrix
			#bone.matrix= matr
			#bone.matrix = armature_matrix_world * bone.matrix
		
		bpy.ops.object.mode_set( mode = 'OBJECT' , toggle=False)
		bpy.data.armatures[ob.data.name].use_mirror_x = mirror_x_flag
		return {'FINISHED'}

class hfg_bone_collection(bpy.types.PropertyGroup):
	tk_matrix = FloatVectorProperty(name="Original Matrix" , size=16 , subtype="MATRIX")


class OT_remove_fake_bones(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.remove_fake_bones"
	bl_label = ""
	bl_description = "Remove all fake bones in the scene"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		remove_fake_bones()
		return {'FINISHED'}

class OT_add_fake_bones(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.add_fake_bones"
	bl_label = ""
	bl_description = "Add fake bones in the scene"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		remove_fake_bones()
		add_fake_bones()
		return {'FINISHED'}

class OT_export_fake_bones(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.export_fake_bones"
	bl_label = ""
	bl_description = "Export fake bones in the scene"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		if os.path.isdir(tkarmature.exportfolderpath):
			print ("Saving to: "+tkarmature.exportfolderpath)
		else:
			ShowMessageBox("Missing the export folder", "Error", 'ERROR')
			return {'FINISHED'}		
		export_fake_bones(tkarmature.exportfolderpath,tkarmature.bodyNo, tkarmature.dontExportJointEnds)
		return {'FINISHED'}



class OT_fix_symmetry(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.fix_symmetry"
	bl_label = ""
	bl_description = "Symmetrize bone rolls from good bones to flipped bones"
	
	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		fix_symmetry()
		return {'FINISHED'}



class OT_rename_bones(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.rename_bones"
	bl_label = ""
	bl_description = "Rename bones to make them mirror friendly"
	
	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		rename_bones()
		return {'FINISHED'}

class OT_rename_bones_back(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.rename_bones_back"
	bl_label = ""

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		rename_bones_back()
		return {'FINISHED'}


class OT_adjust_bones(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.adjust_bones"
	bl_label = ""
	bl_description = "Parent bone tail is set to child bone head and bones become connected"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		adjust_editbones_length()
		return {'FINISHED'}

def flatten(mat):
	dim = len(mat)
	return [mat[j][i] for i in range(dim) for j in range(dim)]
					  
class OT_create_armature(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.create_armature"
	bl_label = ""
	bl_description = "Import a hardcoded armature for Female"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		#create_armature() #old function
		pre_import_armature()
		addBonesFromHardcodedValue()
		post_import_armature()
		prev_mode =  bpy.data.objects["Armature"].mode
		bpy.ops.object.mode_set(mode='EDIT')
		for editBone in bpy.context.object.data.edit_bones:
			editBone["originalHead"] = editBone.head
			editBone["originalTail"] = editBone.tail
			editBone["originalRoll"] = editBone.roll
		#for posebone in bpy.data.objects["Armature"].pose.bones:
		#	editbone = bpy.data.objects["Armature"].data.edit_bones[posebone.name]
		#	editbone["originalMatrix"] = flatten(bpy.context.object.data.bones[posebone.name].matrix)
		#				#	posebone.hfg_bone.tk_matrix = flatten(posebone.bone.matrix_local)
		bpy.ops.object.mode_set(mode=prev_mode)
		return {'FINISHED'}


class OT_import_armature(bpy.types.Operator, ImportHelper):
	''''''
	bl_idname = "tkarmature.import_armature"
	bl_label = "Import TXT File"
	bl_description = "Import armature for CollaTkane txt anim file"


	filter_glob = StringProperty(
		default='*.txt',
		options={'HIDDEN'}
	)
	
	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		bpy.ops.object.select_all(action='DESELECT')
		print('Selected file:', self.filepath)
		path_to_file = self.filepath
		#print('Extra Processing:', self.extra_processing)
		pre_import_armature()
		addBonesFromCtkAnimSkeleton(path_to_file)
		post_import_armature()				
		prev_mode =  bpy.data.objects["Armature"].mode
		bpy.ops.object.mode_set(mode='EDIT')
		for editBone in bpy.context.object.data.edit_bones:
			editBone["originalHead"] = editBone.head
			editBone["originalTail"] = editBone.tail
			editBone["originalRoll"] = editBone.roll
		#for posebone in bpy.data.objects["Armature"].pose.bones:
		#	editbone = bpy.data.objects["Armature"].data.edit_bones[posebone.name]
		#	editbone["originalMatrix"] = flatten(bpy.context.object.data.bones[posebone.name].matrix)
		#				#	posebone.hfg_bone.tk_matrix = flatten(posebone.bone.matrix_local)
		bpy.ops.object.mode_set(mode=prev_mode)
		return {'FINISHED'}



class OT_Export_Armature_To_Empties(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.export_armature_to_empties"
	bl_label = ""
	bl_description = "Create _empties for export"
	
	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		try: 
			_root_object = bpy.data.objects["_root"]
			print("_root_object: "+_root_object.name)
			delete_hierarchy("_root")
		except: 
			print("_root object missing")
		#if 1==1:
		#	return {'FINISHED'}
		bpy.ops.object.select_all(action='DESELECT')			
		armature_object = bpy.data.objects["Armature"]
		armature_object.select = True
		bpy.context.scene.objects.active = armature_object
		regenerate_empties(armature_object)
		return {'FINISHED'}
		
		
class OT_Load_Config(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.import_level_def"
	bl_label = ""

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		load_config(self,context)
		return {'FINISHED'}
		
class OT_Export_Inverse_Bind_Matrix(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.export_inverse_bind_matrix"
	bl_label = ""
	bl_description = "Export Inverse Bind Matrix for body and CollaTkane"
	
	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		if os.path.isdir(tkarmature.exportfolderpath):
			print ("Saving to: "+tkarmature.exportfolderpath)
		else:
			ShowMessageBox("Missing the export folder", "Error", 'ERROR')
			return {'FINISHED'}
		recalculateBindInverseMatrix(tkarmature.exportfolderpath, tkarmature.bodyNo)
		recalculateBindInverseMatrixCTK(tkarmature.exportfolderpath, tkarmature.bodyNo)
		ShowMessageBox("Inverse Bind Matrix files exported", "Success", 'INFO')
		return {'FINISHED'}
		
class OT_Export_Empties_To_Files(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.export_empties_to_files"
	bl_label = ""
	bl_description = "Final step, magic is going to happen!"
	
	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		if os.path.isdir(tkarmature.exportfolderpath):
			print ("Saving to: "+tkarmature.exportfolderpath)
		else:
			ShowMessageBox("Missing the export folder", "Error", 'ERROR')
			return {'FINISHED'}
		export_boilerplate_header(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_joints_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_mouth_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_arms_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_legs_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_breasts_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_anus_default(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_face_default(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_values_cleanup(tkarmature.exportfolderpath, tkarmature.bodyNo)
		export_boilerplate_tail(tkarmature.exportfolderpath, tkarmature.bodyNo)
		file_path = tkarmature.exportfolderpath+"AcBody"+tkarmature.bodyNo+"Collision.bs"
		ShowMessageBox("Exported to "+file_path, "Success", 'INFO')
		return {'FINISHED'}
		
class OT_Export_Body(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.export_body"
	bl_label = ""
	bl_description = "Export body snippets"
	
	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		if os.path.isdir(tkarmature.exportfolderpath):
			print ("Saving to: "+tkarmature.exportfolderpath)
		else:
			ShowMessageBox("Missing the export folder", "Error", 'ERROR')
			return {'FINISHED'}		
		export_body(tkarmature.exportfolderpath, tkarmature.bodyNo)
		return {'FINISHED'}
		
# this class extends ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Import_G3F_Body(Operator, ImportHelper):
	''''''
	bl_idname = "test.import_g3f_body"
	bl_label = "Pick Obj file"
	bl_description = "Import G3F body from obj file"

	filter_glob = StringProperty(
		default='*.obj',
		options={'HIDDEN'}
	)
	extra_processing = BoolProperty(
		name='Process object after import',
		description='Fix materials, UV name, add vertex groups, add shapes, and other fixes',
		default=True
	)
	
	def execute(self, context):
		bpy.context.scene.objects.active = None
		for obj in bpy.data.objects:
			obj.select = False		
		bpy.ops.object.select_all(action='DESELECT')
		print('Selected file:', self.filepath)
		path_to_file = self.filepath
		print('Extra Processing:', self.extra_processing)
		bpy.ops.import_scene.obj(filepath = path_to_file,split_mode='OFF')
		obj_object = bpy.context.selected_objects[0] ####<--Fix
		bpy.context.scene.objects.active = obj_object
		print('Imported name: ', obj_object.name)		
		import_g3f()
		return {'FINISHED'}
	
# when implemented this class should extend ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Import_G3F_Morph(Operator, ImportHelper):
	''''''
	bl_idname = "tkarmature.import_g3f_morph"
	bl_label = "Pick Obj file"
	bl_description = "Import G3F morph body from obj file"
	
	filter_glob = StringProperty(
		default='*.obj',
		options={'HIDDEN'}
	)
	extra_processing = BoolProperty(
		name='Process object after import',
		description='Fix materials, UV name, add vertex groups, add shapes, and other fixes',
		default=True
	)
	
	def execute(self, context):
		base_body_mesh = None
		if (bpy.context.scene.objects.active != None):
			if (bpy.context.scene.objects.active.select == True):
				base_body_mesh = bpy.context.scene.objects.active
		bpy.context.scene.objects.active = None
		for obj in bpy.data.objects:
			obj.select = False		
		bpy.ops.object.select_all(action='DESELECT')
		print('Selected file:', self.filepath)
		path_to_file = self.filepath
		print('Extra Processing:', self.extra_processing)
		encoding = 'utf-8'
		pattern ='usemtl\\s*.*\\n'
		matched = re.compile(pattern).search
		with open(path_to_file, encoding=encoding) as input_file:
			with NamedTemporaryFile(mode='w', encoding=encoding,suffix='.obj', dir=os.path.dirname(path_to_file), delete=False) as outfile:
				for line in input_file:
					if not matched(line):
						print(line, end='', file=outfile)
				outfile.close()
				bpy.ops.import_scene.obj(filepath = outfile.name,split_mode='OFF')
				morph_object = bpy.context.selected_objects[0] ####<--Fix
				bpy.context.scene.objects.active = morph_object
				head, tail = os.path.split(path_to_file)
				new_morph_name = os.path.splitext(tail)[0]
				morph_object.name = new_morph_name
				print('Imported name: ', morph_object.name)	
				import_g3f_morph(base_body_mesh, morph_object)
				os.remove(outfile.name)
		return {'FINISHED'}


# this class extends ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Import_Blenda_Body(Operator, ImportHelper):
	''''''
	bl_idname = "test.import_generic_body"
	bl_label = "Pick Obj file"
	bl_description = "Import generic body from obj file"

	filter_glob = StringProperty(
		default='*.obj',
		options={'HIDDEN'}
	)
	extra_processing = BoolProperty(
		name='Process object after import',
		description='Fix materials, UV name, add vertex groups, add shapes, and other fixes',
		default=True
	)
	
	def execute(self, context):
		bpy.ops.object.select_all(action='DESELECT')
		print('Selected file:', self.filepath)
		path_to_file = self.filepath
		print('Extra Processing:', self.extra_processing)
		bpy.ops.import_scene.obj(filepath = path_to_file,split_mode='OFF')
		obj_object = bpy.context.selected_objects[0] ####<--Fix
		print('Imported name: ', obj_object.name)		
		return {'FINISHED'}



@bpy.app.handlers.persistent
def post_ob_data_updated(scene):
	ob = scene.objects.active
	if ob is not None and ob.type=='ARMATURE' and ob.data.is_updated: #
		print (ob.type)
		print("%s - Armature Object data is_updated (post)" % ob.data.name)
		mode = ob.mode
		if mode=="EDIT":
			for eb in ob.data.edit_bones:
				pb = ob.pose.bones[eb.name]
				pb.dp_helper.shouldUpdate = False
				pb.dp_helper.roll = eb.roll
			for eb in ob.data.edit_bones:
				pb = ob.pose.bones[eb.name]
				pb.dp_helper.shouldUpdate = True




class OT_sync_rolls(bpy.types.Operator):
	''''''
	bl_idname = "tkarmature.sync_rolls"
	bl_label = ""
	bl_description = "Sync bone rolls"

	group = bpy.props.StringProperty(name="ALL")

	def execute(self, context):
		scene  = bpy.context.scene
		tkarmature  = scene.tkarmature
		ob = context.active_object
		mode = ob.mode
		if mode!="EDIT":
			bpy.ops.object.mode_set(mode='EDIT')
		for eb in ob.data.edit_bones:
			pb = ob.pose.bones[eb.name]
			pb.dp_helper.shouldUpdate = False
			pb.dp_helper.roll = eb.roll
		for eb in ob.data.edit_bones:
			pb = ob.pose.bones[eb.name]
			pb.dp_helper.shouldUpdate = True
		bpy.ops.object.mode_set(mode=mode) #Restore previous mode
		return {'FINISHED'}


def item_pose_draw(self, context):
	layout = self.layout
	ob = context.active_object
	row = layout.row()
	if ob.type == 'ARMATURE' and ob.mode in { "POSE" , "EDIT"}:
		bone = context.active_bone
		if bone:
			row = layout.row()
			bone = ob.pose.bones[bone.name] #Property group is in Pose Bone, not in Edit Bone therefore  
			row.label(icon='MESH_CONE')
			row.prop(bone.dp_helper, "roll", text=bone.name)
			row = layout.row()
			row.operator('tkarmature.sync_rolls',text='Sync rolls',icon='PMARKER')
			
def pbone_roll_update(self,context):
	if (self.shouldUpdate):
		mode = context.active_object.mode
		if mode != 'EDIT':
			bpy.ops.object.mode_set(mode='EDIT')
		context.active_bone.roll = self.roll
		bpy.ops.object.mode_set(mode=mode) #Restore previous mode
	else:
		print ("not going to update it!")


class DpPoseBoneHelper(bpy.types.PropertyGroup):
	roll = FloatProperty(subtype = 'ANGLE', update = pbone_roll_update)
	shouldUpdate = BoolProperty(name="Allow Update",description="A bool property for Allow Update",default = True)


@persistent
def addon_handler(scene):
	bpy.app.handlers.scene_update_post.remove(addon_handler)
	tkarmature = bpy.data.scenes[0].tkarmature
	#tkarmature.updated = 0
	# todo
	#load_config('','')
	#bsLookupRead()
	return {'FINISHED'}

@persistent
def load_post_handler(dummyArg):
	load_config2('','')
	#load_config('','')
	#bsLookupRead()
	#return {'FINISHED'}
	
#bpy.app.handlers.load_post.append(load_post_handler)

def register() :
	global custom_icons
	custom_icons = bpy.utils.previews.new()
	script_path = os.path.realpath(__file__)
	directory = os.path.dirname(script_path)
	icons_dir = os.path.join(directory, "icons")
	custom_icons.load("matrix_icon", os.path.join(icons_dir, "matrix.png"), 'IMAGE')
	custom_icons.load("wand_icon", os.path.join(icons_dir, "auto-fix.png"), 'IMAGE')
	custom_icons.load("ik_arm_icon", os.path.join(icons_dir, "ik_arm.png"), 'IMAGE')
	#bpy.utils.register_class(TKARMATURE_panel)
	#
	#when there are many classes or a packages submodule has its own classes it can be tedious to list them all for registration. For more convenient loading bpy.utils.register_module (module)
	#Internally Blender collects subclasses on registrable types, storing them by the module in which they are defined. By passing the module name to bpy.utils.register_module Blender can register all classes created by this module and its submodules.
	bpy.utils.register_module(__name__)
	bpy.types.PoseBone.hfg_bone=bpy.props.PointerProperty(type=hfg_bone_collection)
	bpy.types.Scene.tkarmature = bpy.props.PointerProperty(type=TKARMATURE_vars)	
	tkarmature = bpy.types.Scene.tkarmature	
	#bpy.app.handlers.scene_update_post.append(addon_handler)
	bpy.types.PoseBone.dp_helper = PointerProperty(type = DpPoseBoneHelper)
	bpy.types.VIEW3D_PT_view3d_name.append(item_pose_draw)
	bpy.app.handlers.scene_update_post.append(post_ob_data_updated)
	

def unregister() :
	global custom_icons
	bpy.utils.previews.remove(custom_icons)
	del bpy.types.Scene.tkarmature
	del bpy.types.PoseBone.hfg_bone
	bpy.types.VIEW3D_PT_view3d_name.remove(item_pose_draw)
	bpy.app.handlers.scene_update_post.clear()
	#when there are many classes or a packages submodule has its own classes it can be tedious to list them all for un-registration. For more convenient loading bpy.utils.unregister_module (module)
	#Internally Blender collects subclasses on registrable types, storing them by the module in which they are defined. By passing the module name to bpy.utils.register_module Blender can register all classes created by this module and its submodules.
	bpy.utils.unregister_module(__name__)  

if __name__ == "__main__":
	register()
#
#https://gist.github.com/tin2tin/ce4696795ad918448dfbad56668ed4d5
#https://sinestesia.co/blog/tutorials/using-uilists-in-blender/