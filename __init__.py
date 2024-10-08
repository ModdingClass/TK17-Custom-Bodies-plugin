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
from bpy_extras.io_utils import ExportHelper 
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
from .exporter_spine_fix import *
from .exporter_gens_fix import *
from .exporter_breasts_fix import *
from .recalculate_BindInvMatrix import *
from .recalculate_BindInvMatrix_CTK import *
from .face_default import *
from .fake_bones import *
from .clear_armature_rotation import *
from .tools_message_box import *
from .exporter_body import *
from .exporter_unreal import *
from .importer_g3f import *
from .importer_g3f_morphs import *
from .exporter_fake_bones import *
from .exporter_z_cleanup_values import *
from .exporter_boilerplate import *
from .tools_duplicate_object_remove_mats_shapekeys import *
from .helper_vgroups import *
from .g3f.importer_g3f_difeomorphic import *
from .g3f.difeomorphic_workflow import *
from .tools_import_export_vertex_groups_json import *
from .tools_import_export_shape_keys_json import *
from .tools_import_export_materials_json import *
from .tools_import_export_edit_bones_json import *
from .ik_tools import *

from .fbody_stats import *
from .strip_and_clean_op import *

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
    imp.reload(exporter_spine_fix)
    imp.reload(exporter_gens_fix)    
    imp.reload(exporter_breasts_fix)
    imp.reload(recalculate_BindInvMatrix)
    imp.reload(recalculate_BindInvMatrix_CTK)
    imp.reload(face_default)
    imp.reload(fake_bones)
    imp.reload(clear_armature_rotation)
    imp.reload(tools_message_box)
    imp.reload(exporter_body)
    imp.reload(exporter_unreal)
    imp.reload(importer_g3f)
    imp.reload(importer_g3f_morphs)
    imp.reload(exporter_fake_bones)
    imp.reload(exporter_z_cleanup_values)
    imp.reload(exporter_boilerplate)
    imp.reload(tools_duplicate_object_remove_mats_shapekeys)
    imp.reload(helper_vgroups)
    imp.reload(g3f.importer_g3f_difeomorphic)
    imp.reload(g3f.difeomorphic_workflow)
    imp.reload(g3f.difeomorphic_workflow_init_custom_vertex_indices)
    imp.reload(tools_import_export_vertex_groups_json)
    imp.reload(tools_import_export_shape_keys_json)
    imp.reload(tools_import_export_materials_json)
    imp.reload(fbody_stats)
    imp.reload(strip_and_clean_op)
    imp.reload(ik_tools)
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
    from . import exporter_spine_fix
    from . import exporter_gens_fix    
    from . import exporter_breasts_fix    
    from . import recalculate_BindInvMatrix
    from . import recalculate_BindInvMatrix_CTK
    from . import face_default
    from . import fake_bones
    from . import clear_armature_rotation
    from . import tools_message_box
    from . import exporter_body
    from . import exporter_unreal
    from . import importer_g3f_morphs
    from . import exporter_fake_bones
    from . import exporter_z_cleanup_values
    from . import exporter_boilerplate
    from . import tools_duplicate_object_remove_mats_shapekeys
    from . import helper_vgroups
    from .g3f import importer_g3f_difeomorphic
    from .g3f import difeomorphic_workflow
    from .g3f import difeomorphic_workflow_init_custom_vertex_indices
    from . import tools_import_export_vertex_groups_json
    from . import tools_import_export_shape_keys_json
    from . import tools_import_export_materials_json
    from . import fbody_stats
    from . import strip_and_clean_op    
    from . import ik_tools
    print("Imported multifiles")

version = 'v%s.%s'%(bl_info['version'][0],bl_info['version'][1])


fbody_global_matching_index_dict = OrderedDict()

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

    def update_func_exportfolderpathUnreal(self, context):
        #self.exportfolderpath = os.path.join(self.exportfolderpathUnreal,"")
        new_value = os.path.join(self.exportfolderpathUnreal,"")
        if new_value == self.exportfolderpathUnreal:
            pass
        else:
            self.exportfolderpathUnreal = new_value
        print("exportfolderpathUnreal: ", self.exportfolderpathUnreal)

    #exportfolderpath =  bpy.props.StringProperty(name="exportfolderpath", default='',subtype='DIR_PATH', update=update_func_exportfolderpath)
    
    filepath =  bpy.props.StringProperty(name="filepath", default='',subtype='FILE_PATH')
    filepath_h5m =  bpy.props.StringProperty(name="filepath_h5m", default='',subtype='FILE_PATH')

    fbxFilename =  bpy.props.StringProperty(name="fbxFilename", default='',subtype='FILE_NAME')

    exportfolderpath =  bpy.props.StringProperty(name="exportfolderpath", default='',subtype='DIR_PATH', update=update_func_exportfolderpath)
    exportfolderpathUnreal = bpy.props.StringProperty(name="exportfolderpathUnreal", default='',subtype='DIR_PATH', update=update_func_exportfolderpathUnreal)
    bodyNo = bpy.props.StringProperty(name="bodyNo",description="Body No", default="01")
    dontExportJointEnds = bpy.props.BoolProperty(name="dontExportJointEnds", description="Weightless jointEnds are not exported",    default=True)
    dontExportMaleJoints = bpy.props.BoolProperty(name="dontExportMaleJoints", description="Male specific joints are not exported",    default=True)

    includeGeograftsOnExport = bpy.props.BoolProperty(name="includeGeograftsOnExport", description="Bake children Geografts when exporting",    default=True)
    includeGeograftsOnExportUnreal = bpy.props.BoolProperty(name="includeGeograftsOnExportUnreal", description="Bake children Geografts when exporting",    default=True)
    createSubdivMeshOnExportUnreal = bpy.props.BoolProperty(name="createSubdivMeshOnExportUnreal", description="Add a subdivided mesh when exporting",    default=True)
    cleanTempMeshesOnExportUnreal = bpy.props.BoolProperty(name="cleanTempMeshesOnExportUnreal", description="Delete temp/work meshes after exporting",    default=True)



class ImporterPanel(bpy.types.Panel):
    """Creates a Panel in the Tool Shelf"""
    bl_label = "Importer Armature"
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
        
class ImporterPanelFromObj(bpy.types.Panel):
    """Creates a Panel in the Tool Shelf"""
    bl_label = "Importer .Obj"
    bl_idname = "Importer Panel Obj Workflow"
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
        row.operator('tkarmature.fake',text='              ')
        row.operator('test.import_g3f_body',text='Import G3F body',icon='OBJECT_DATA')    
        row.operator('tkarmature.import_g3f_morph',text='Import G3F morph',icon='MOD_MASK')            
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('test.import_generic_body',text='Import generic body',icon='OBJECT_DATA')    
        row.operator('tkarmature.fake',text='              ')
        

class ImporterPanelDifeomorphic(bpy.types.Panel):
    """Creates a Panel in the Tool Shelf"""
    bl_label = "Importer Difeomorphic "
    bl_idname = "Importer Panel Difeomorphic Workflow"
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
        row.operator('tkarmature.fake',text='              ')
        row.operator('difeomorphic.import_g3f_body_difeomorphic',text='G3F'+u'→'+'VX body',icon='OBJECT_DATA')      
        row.operator('difeomorphic.adjust_rig_to_shape_difeomorphic',text='Adjust Rig to Difeomorphic',icon_value=custom_icons["wand_icon"].icon_id)
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('difeomorphic.switch_to_vx_vertex_groups',text='Switch Vertex Groups',icon='GROUP_VERTEX')    
        row.operator('tkarmature.fake',text='              ')   
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.fake',text='              ')
        row.operator('difeomorphic.armature_friendly_ik',text='Force friendly IK joints',icon_value=custom_icons["wand_icon"].icon_id)
        


class QuickPanel(bpy.types.Panel):
    """Creates a Panel in the Tool Shelf"""
    bl_label = "Quick"
    bl_idname = "QuickPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "TK17 Body"
    def draw(self,context):
        layout = self.layout
        
    def merge_vgroups_into_third(name, a,b,c):
        merge_vgroups_into_third (name,a,b,c)




def function_a():
    print("Function A")

def function_b(*args):
    print([a for a in args])


functions = [ function_a , function_b ]

class FunctionCall(Operator):
    bl_idname = "dp16.button_function"
    bl_label = "Button"
    bl_options = {'REGISTER', 'UNDO'}
    function_id = IntProperty()
    
    def execute(self,context):
        functions[self.function_id]()
        return {"FINISHED"}
        
class Functions(Operator):
    bl_idname = "dp16.quick_function"
    bl_label = "Functions"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self,context):
        return {"FINISHED"}
        
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self,context):
        box = self.layout.box()
        #row=box.row()
        for i,f in enumerate(functions):
            row=box.row() 
            btn = row.operator("dp16.button_function",text=f.__name__)
            btn.function_id = i



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
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.export_materials_to_json',text='Export materials',icon='MATERIAL_DATA')
        row.operator('tkarmature.import_materials_from_json',text='Import materials',icon='MATERIAL_DATA')
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.export_weights_to_json',text='Export weights',icon='GROUP_VERTEX')
        row.operator('tkarmature.import_weights_from_json',text='Import weights',icon='GROUP_VERTEX')
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.export_shapekeys_to_json',text='Export shapekeys',icon='SHAPEKEY_DATA')
        row.operator('tkarmature.import_shapekeys_from_json',text='Import shapekeys',icon='SHAPEKEY_DATA')        
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.add_empty_shapekeys',text='Add empty shapekeys',icon='SHAPEKEY_DATA')
        row.operator('tkarmature.fake',text='              ')
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.export_edit_bones_to_json',text='Export Edit Bones',icon='OUTLINER_DATA_ARMATURE')
        row.operator('tkarmature.import_edit_bones_from_json',text='Import Edit Bones',icon='OUTLINER_DATA_ARMATURE')        
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
        row.operator('tkarmature.hh_pose_ik',text='HH Pose IK',icon='OUTLINER_DATA_POSE')
        #row.operator('tkarmature.add_legs_ik',text='Ignore this',icon='POSE_DATA')
        row.operator('tkarmature.add_finger_hand_close_constraints',text='Finger Constraints',icon='CONSTRAINT_BONE')
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.add_custom_ik_bones',text='Custom IK('+u'β'+')',icon='OUTLINER_DATA_POSE')
        row.operator('tkarmature.fake',text='              ')

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
        row.operator('tkarmature.add_fake_shape_bones',text='Add Fake Shape Bones',icon='PMARKER')
        row.operator('tkarmature.remove_fake_bones',text='Remove Fake Bones',icon='PMARKER')
        row.operator('tkarmature.fake',text='              ')
        row=box.row(align=True)
        row.operator('tkarmature.add_fake_axis_bones',text='Add Fake Axis Bones',icon='PMARKER')
        row.operator('tkarmature.merge_fakes_in_single_object',text='Merge fakes',icon='OUTLINER_OB_GROUP_INSTANCE')
        row.operator('tkarmature.export_fake_bones',text='Export Fake Bones')
        row=box.row()
        row.separator()
        #row.operator('test.open_filebrowser',text='Import Blenda body',icon='OBJECT_DATA')    
        new_box = row.box()
        new_box.label(text="Don't Export")
        row=new_box.row(align=True)
        row.prop(tkarmature,'dontExportJointEnds',text="Weightless jointEnds")
        row.prop(tkarmature,'dontExportMaleJoints',text="Male specific joints")
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.fake',text='              ')
        


class ExporterPanelUnreal(bpy.types.Panel):
    """Creates a Panel in the Tool Shelf"""
    bl_label = "Exporter Unreal"
    bl_idname = "Exporter Panel Unreal"
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
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.fake',text='              ')
        #box.row().separator()
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')        
        row.operator('tkarmature.build_subdivision_vertex_matching_table',text='Build subdiv match', icon='GROUP_VERTEX')  
        row.operator('tkarmature.load_fbody_matching_index_dict_from_json',text='Load subdiv match',icon='GROUP_VERTEX')
        #box.row().separator()
        row=box.row(align=True)
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.fake',text='              ')
        row.operator('tkarmature.export_skeletalmesh_unreal',text='Export Unreal SkeletalMesh', icon='TIME')            
        row=box.row()
        
        #row.separator()
        
        #row.operator('test.open_filebrowser',text='Import Blenda body',icon='OBJECT_DATA')    
        new_box = row.box()
        new_box.label(text="Extra Export")
        row_extra=new_box.row(align=True)

        
        row_extra.prop(tkarmature,'createSubdivMeshOnExportUnreal',text="Create Subdiv")
        row_extra.alignment = 'RIGHT'
        row_extra.prop(tkarmature,'includeGeograftsOnExportUnreal',text="Include Geografts")
        row_extra=new_box.row(align=True)
        row_extra.prop(tkarmature,'cleanTempMeshesOnExportUnreal',text="Cleanup after export")
        

        row=box.row(align=True)
        subbox_exporter=row.box()
        subbox_row = subbox_exporter.row()
        
        icon='FILE_FOLDER'
        subbox_row.label(text='Folder location:',icon=icon)
        subbox_row = subbox_exporter.row()
        subbox_row.prop(tkarmature,'exportfolderpathUnreal',text='')        
        subbox_row = subbox_exporter.row()
        #subbox_row.label(text='Body#:',icon='QUESTION')
        subbox_row.prop(tkarmature,'fbxFilename',text='Fbx filename')



class ExporterPanelVX(bpy.types.Panel):
    """Creates a Panel in the Tool Shelf"""
    bl_label = "Exporter VX"
    bl_idname = "Exporter Panel VX"
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
        row.operator('tkarmature.export_armature_to_empties',text='Armature to Empties',icon='OUTLINER_OB_EMPTY') #use_mirror_x
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
        
        #row.separator()
        
        #row.operator('test.open_filebrowser',text='Import Blenda body',icon='OBJECT_DATA')    
        new_box = row.box()
        new_box.label(text="Extra Export")
        row_extra=new_box.row(align=True)
        row_extra.alignment = 'RIGHT'
        col_extra =row_extra.column()
        col_extra.alignment = 'RIGHT'
        col_extra.scale_x = 1
        #above is a hack to align the column to the right
        col_extra.prop(tkarmature,'includeGeograftsOnExport',text="Include Geografts")


        row=box.row(align=True)
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


class OT_hh_pose_ik(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.hh_pose_ik"
    bl_label = ""
    bl_description = "High Heels Pose IK"

    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        create_HHPoseIk(bpy.context.scene.objects["Armature"])
        return {'FINISHED'}        



class OT_add_custom_ik_bones(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.add_custom_ik_bones"
    bl_label = ""
    u = u'β'
    s = u.encode('utf8')
    bl_description = "Temporary Add IK to the body (beta)"

    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        create_IKs(bpy.context.scene.objects["Armature"])
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


# this class extends ExportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Exports_Materials_To_Json(Operator, ExportHelper):
    ''''''
    bl_idname = "tkarmature.export_materials_to_json"
    bl_label = "Export materials"
    bl_description = "Exports materials to a custom json file"

    filename_ext = ".json"  # ExportHelper mixin class uses this
    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        #bpy.context.scene.objects.active = None
        #for obj in bpy.data.objects:
        #    obj.select = False        
        #bpy.ops.object.select_all(action='DESELECT')
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        exportMaterialsToJsonFile(ob, path_to_file)
        return {'FINISHED'}
    

# this class extends ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Import_Materials_From_Json(Operator, ImportHelper):
    ''''''
    bl_idname = "tkarmature.import_materials_from_json"
    bl_label = "Import materials"
    bl_description = "Import materials from a custom json file"

    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        #bpy.context.scene.objects.active = None
        #for obj in bpy.data.objects:
        #    obj.select = False        
        #bpy.ops.object.select_all(action='DESELECT')
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        importMaterialsFromJsonFile(ob, path_to_file)
        return {'FINISHED'}
    




#        row.operator('tkarmature.export_edit_bones_to_json',text='Export Edit Bones',icon='OUTLINER_DATA_ARMATURE')
#        row.operator('tkarmature.import_edit_bones_from_json',text='Import Edit Bones',icon='OUTLINER_DATA_ARMATURE')      
# this class extends ExportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Exports_Edit_Bones_To_Json(Operator, ExportHelper):
    ''''''
    bl_idname = "tkarmature.export_edit_bones_to_json"
    bl_label = "Export Edit Bones"
    bl_description = "Exports Edit Bones data to a custom json file"

    filename_ext = ".json"  # ExportHelper mixin class uses this
    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        #bpy.context.scene.objects.active = None
        #for obj in bpy.data.objects:
        #    obj.select = False        
        #bpy.ops.object.select_all(action='DESELECT')
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        exportEditBonesToJsonFile(ob, path_to_file)
        return {'FINISHED'}
    

# this class extends ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Import_Edit_Bones_From_Json(Operator, ImportHelper):
    ''''''
    bl_idname = "tkarmature.import_edit_bones_from_json"
    bl_label = "Import Edit Bones"
    bl_description = "Import Edit Bones data from a custom json file"

    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        #bpy.context.scene.objects.active = None
        #for obj in bpy.data.objects:
        #    obj.select = False        
        #bpy.ops.object.select_all(action='DESELECT')
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        importEditBonesFromJsonFile(ob, path_to_file)
        return {'FINISHED'}
    





















#        row.operator('tkarmature.export_weights_to_json',text='Export weights')
#        row.operator('tkarmature.import_weights_from_json',text='Import weights')

# this class extends ExportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Exports_Weights_To_Json(Operator, ExportHelper):
    ''''''
    bl_idname = "tkarmature.export_weights_to_json"
    bl_label = "Export weights"
    bl_description = "Exports weights to a custom json file"

    filename_ext = ".json"  # ExportHelper mixin class uses this
    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        #bpy.context.scene.objects.active = None
        #for obj in bpy.data.objects:
        #    obj.select = False        
        #bpy.ops.object.select_all(action='DESELECT')
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        exportVertexGroupsToJsonFile(ob, path_to_file)
        return {'FINISHED'}
    

# this class extends ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Import_Weights_From_Json(Operator, ImportHelper):
    ''''''
    bl_idname = "tkarmature.import_weights_from_json"
    bl_label = "Import weights"
    bl_description = "Import weights from a custom json file"

    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        #bpy.context.scene.objects.active = None
        #for obj in bpy.data.objects:
        #    obj.select = False        
        #bpy.ops.object.select_all(action='DESELECT')
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        importVertexGroupsFromJsonFile(ob, path_to_file)
        return {'FINISHED'}
    

#        row.operator('tkarmature.export_shapekeys_to_json',text='Export shapekeys',icon='SHAPEKEY_DATA')
#        row.operator('tkarmature.import_shapekeys_from_json',text='Import shapekeys',icon='SHAPEKEY_DATA')  

# this class extends ExportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Exports_Shapekeys_To_Json(Operator, ExportHelper):
    ''''''
    bl_idname = "tkarmature.export_shapekeys_to_json"
    bl_label = "Export shapekeys"
    bl_description = "Exports shapekeys to a custom json file"

    filename_ext = ".json"  # ExportHelper mixin class uses this
    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        exportShapeKeysToJsonFile(ob, path_to_file)
        return {'FINISHED'}
    

# this class extends ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class OT_Import_Shapekeys_From_Json(Operator, ImportHelper):
    ''''''
    bl_idname = "tkarmature.import_shapekeys_from_json"
    bl_label = "Import shapekeys"
    bl_description = "Import shapekeys from a custom json file"
    filename_ext = ".json"  # ExportHelper mixin class uses this
    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        print('Selected file:', self.filepath)
        path_to_file = self.filepath
        ob = bpy.context.object
        importShapeKeysFromJsonFile(ob, path_to_file)
        return {'FINISHED'}


class OT_add_empty_shapekeys(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.add_empty_shapekeys"
    bl_label = ""
    bl_description = "Add empty shapekeys for VX body."

    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        add_empty_shapekeys_for_vx_body()
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

class OT_add_fake_shape_bones(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.add_fake_shape_bones"
    bl_label = ""
    bl_description = "Add fake shape bones in the scene"

    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        remove_fake_bones()
        add_fake_bones("rhomb_bone")
        return {'FINISHED'}

class OT_add_fake_axis_bones(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.add_fake_axis_bones"
    bl_label = ""
    bl_description = "Add fake axis bones in the scene"

    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        remove_fake_bones()
        add_fake_bones("new_axis_bone")
        return {'FINISHED'}

class OT_merge_fakes_in_single_object(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.merge_fakes_in_single_object"
    bl_label = ""
    bl_description = "Merge fake bones into a single mesh object (for export)"

    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        merge_fake_bones_into_single_mesh_object(tkarmature.dontExportJointEnds, tkarmature.dontExportMaleJoints)
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
        export_fake_bones(tkarmature.exportfolderpath,tkarmature.bodyNo, tkarmature.dontExportJointEnds, tkarmature.dontExportMaleJoints)
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
        #    editbone = bpy.data.objects["Armature"].data.edit_bones[posebone.name]
        #    editbone["originalMatrix"] = flatten(bpy.context.object.data.bones[posebone.name].matrix)
        #                #    posebone.hfg_bone.tk_matrix = flatten(posebone.bone.matrix_local)
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
        #    editbone = bpy.data.objects["Armature"].data.edit_bones[posebone.name]
        #    editbone["originalMatrix"] = flatten(bpy.context.object.data.bones[posebone.name].matrix)
        #                #    posebone.hfg_bone.tk_matrix = flatten(posebone.bone.matrix_local)
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
            print("_root object missing, nothing to delete...")
        #if 1==1:
        #    return {'FINISHED'}
        bpy.ops.object.select_all(action='DESELECT')            
        armature_object = bpy.data.objects["Armature"]
        #we need to disable mirroring when exporting the armature values, as this is going to mess up values
        mirror_option = armature_object.data.use_mirror_x
        armature_object.data.use_mirror_x = False
        armature_object.select = True
        bpy.context.scene.objects.active = armature_object
        regenerate_empties(armature_object)
        regenerate_empties_hands(armature_object)
        regenerate_empties_ik(armature_object)
        #we need to restore mirroring settings back
        armature_object.data.use_mirror_x = mirror_option
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
        ob = bpy.data.objects[ "Armature"]
        if ob.get("HHPoseValuesL") is None:
            ob["HHPoseValuesL"] = {}
        if ob.get("HHPoseValuesR") is None:
            ob["HHPoseValuesR"] = {}            
        export_boilerplate_header(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_joints_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_mouth_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_arms_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_legs_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_breasts_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_spine_fix(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_anus_default(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_face_default(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_values_cleanup(tkarmature.exportfolderpath, tkarmature.bodyNo)
        export_boilerplate_tail(tkarmature.exportfolderpath, tkarmature.bodyNo)
        file_path = tkarmature.exportfolderpath+"AcBody"+tkarmature.bodyNo+"Collision.bs"
        ShowMessageBox("Exported to "+file_path, "Success", 'INFO')
        return {'FINISHED'}


class OT_Import_fbody_matching_index_dict_from_json(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.load_fbody_matching_index_dict_from_json"
    bl_label = ""
    bl_description = "Load subdivision vertex matching table from json"
    
    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        if os.path.isdir(tkarmature.exportfolderpathUnreal):
            load_fbody_matching_index_dict_from_json(tkarmature.exportfolderpathUnreal, tkarmature.includeGeograftsOnExportUnreal)
            if tkarmature.createSubdivMeshOnExportUnreal:
                #fbx_type : LodGroup
                print ("Creating the lod group parent empty: "+"fbx_type : LodGroup")
        else:
            ShowMessageBox("Missing the import/export folder", "Error", 'ERROR')
            return {'FINISHED'}        
        return {'FINISHED'}


class OT_Export_subdivision_vertex_matching_table(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.build_subdivision_vertex_matching_table"
    bl_label = ""
    bl_description = "Build subdivision vertex matching table"
    
    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        if os.path.isdir(tkarmature.exportfolderpathUnreal):
            print ("Exporting to: "+tkarmature.exportfolderpathUnreal)
            build_subdivision_vertex_matching_table(tkarmature.exportfolderpathUnreal, tkarmature.includeGeograftsOnExportUnreal, tkarmature.cleanTempMeshesOnExportUnreal)
            if tkarmature.createSubdivMeshOnExportUnreal:
                #fbx_type : LodGroup
                print ("Creating the lod group parent empty: "+"fbx_type : LodGroup")
        else:
            ShowMessageBox("Missing the export folder", "Error", 'ERROR')
            return {'FINISHED'}        
        return {'FINISHED'}

class OT_Export_SkeletalMeshUnreal(bpy.types.Operator):
    ''''''
    bl_idname = "tkarmature.export_skeletalmesh_unreal"
    bl_label = ""
    bl_description = "Export SkeletalMesh for Unreal"
    
    group = bpy.props.StringProperty(name="ALL")

    def execute(self, context):
        scene  = bpy.context.scene
        tkarmature  = scene.tkarmature
        if os.path.isdir(tkarmature.exportfolderpathUnreal):
            print ("Exporting to: "+tkarmature.exportfolderpathUnreal)
            export_to_unreal_v2(tkarmature.exportfolderpathUnreal,tkarmature.fbxFilename, tkarmature.includeGeograftsOnExportUnreal, tkarmature.cleanTempMeshesOnExportUnreal)
            if tkarmature.createSubdivMeshOnExportUnreal:
                #fbx_type : LodGroup
                print ("Creating the lod group parent empty: "+"fbx_type : LodGroup")
        else:
            ShowMessageBox("Missing the export folder", "Error", 'ERROR')
            return {'FINISHED'}        
        #export_body(tkarmature.exportfolderpath, tkarmature.bodyNo, tkarmature.includeGeograftsOnExport)
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
        export_body(tkarmature.exportfolderpath, tkarmature.bodyNo, tkarmature.includeGeograftsOnExport)
        return {'FINISHED'}
        

class OT_Import_G3F_Body_Difeomorphic(bpy.types.Operator):
    ''''''
    bl_idname = "difeomorphic.import_g3f_body_difeomorphic"
    bl_label = ""
    bl_description = "Convert G3F body from Difeomorphic into a VX body"    
    def execute(self, context):
        obj_object = bpy.context.selected_objects[0] ####<--Fix
        bpy.context.scene.objects.active = obj_object
        print('Imported name: ', obj_object.name)        
        import_g3f_difeomorphic()
        return {'FINISHED'}




class OT_Armature_Friendly_IK(bpy.types.Operator):
    ''''''
    bl_idname = "difeomorphic.armature_friendly_ik"
    bl_label = ""
    bl_description = "Make armature bones to be friendly/maximum compatibility with IK systems. For example straight legs."
    def execute(self, context):
        scene  = bpy.context.scene
        #tkarmature  = scene.tkarmature
        armature_make_friendly_ik_joints(bpy.data.objects['Armature'])
        return {'FINISHED'}        



class OT_Import_G3F_Rig_Difeomorphic(bpy.types.Operator):
    ''''''
    bl_idname = "difeomorphic.adjust_rig_to_shape_difeomorphic"
    bl_label = ""
    bl_description = "Adjust object rig \"Armature\" to a Difeomorphic imported armature/body"    
    def execute(self, context):
        #obj_object = bpy.context.selected_objects[0] ####<--Fix
        #bpy.context.scene.objects.active = obj_object
        #print('Imported name: ', obj_object.name)        
        alignArmatureToDifeomorphic()
        #extractSpecificBonesFromG3FArmatureFastVersion
        fixFingersJointEndsDifeomorphic("Armature")
        fixToesJointEndsDifeomorphic("Armature")
        fixJointsUsedAsEffectors("Armature")
        fixHeadJointsDifeomorphic("Armature")
        fixSpineJointsDifeomorphic("Armature")
        bpy.ops.object.mode_set(mode='OBJECT')
        isCompatibleBody = check_vertices_count_of_the_body("Genesis 3 Female Mesh",17418)
        if isCompatibleBody:
            print("body is compatible")
            ShowMessageBox("Body vertex count is OK, need to abort", "Warning", 'INFO')
        else:
            ShowMessageBox("Body vertex count is not matching, need to abort", "Warning", 'INFO')
        return {'FINISHED'}

class OT_Switch_To_VX_Vertex_Groups(bpy.types.Operator):
    ''''''
    bl_idname = "difeomorphic.switch_to_vx_vertex_groups"
    bl_label = ""
    bl_description = "Convert vertex groups from Daz to VX"    
    def execute(self, context):
        toe_deform01_joint01_L = {
            "toe_deform01_joint01.L" : ["lBigToe", "lBigToe_2"]
        }
        toe_deform01_joint01_R = {
            "toe_deform01_joint01.R" : ["rBigToe", "rBigToe_2"]
        }  
        toe_deform02_joint01_L = {
            "toe_deform02_joint01.L" : ["lSmallToe1", "lSmallToe2", "lSmallToe3", "lSmallToe4", "lSmallToe1_2", "lSmallToe2_2", "lSmallToe3_2", "lSmallToe4_2"]
        }   
        toe_deform02_joint01_R = {
            "toe_deform02_joint01.R" : ["rSmallToe1", "rSmallToe2", "rSmallToe3", "rSmallToe4", "rSmallToe1_2", "rSmallToe2_2", "rSmallToe3_2", "rSmallToe4_2"]
        } 
        ankle_joint_L = {
            "ankle_joint.L" : [ "lFoot","lHeel","lMetatarsals"]
        }
        ankle_joint_R = {
            "ankle_joint.R" : [ "rFoot","rHeel","rMetatarsals"]
        }
        '''ball_joint_L = {
            "ball_joint.L" : [ "lMetatarsals"]
        }
        ball_joint_R = {
            "ball_joint.R" : [ "rMetatarsals"]
        }  '''      
        ball_joint_L = {
            "ball_joint.L" : [ "lMetatarsals","lBigToe","lSmallToe1", "lSmallToe2", "lSmallToe3", "lSmallToe4"]
        }
        ball_joint_R = {
            "ball_joint.R" : [ "rMetatarsals","rBigToe","rSmallToe1", "rSmallToe2", "rSmallToe3", "rSmallToe4"]
        }
        hip_joint_L = {
            "hip_joint.L" : [ "lThighBend","lThighTwist"]
        }
        hip_joint_R = {
            "hip_joint.R" : ["rThighBend", "rThighTwist"]
        }
        shoulder_joint_L = {
            "shoulder_joint.L" : ["lShldrBend", "lShldrTwist"]
        }
        shoulder_joint_R = {
            "shoulder_joint.R" : ["rShldrBend", "rShldrTwist"]
        }
        head_joint02 = {
            "head_joint02": ['head', 'upperTeeth', 'lowerJaw', 'lEye', 'rEye', 'lEar', 'rEar','rBrowInner', 'rBrowMid', 'rBrowOuter', 'lBrowInner', 'lBrowMid', 'lBrowOuter', 'CenterBrow', 'MidNoseBridge', 'lEyelidInner', 'lEyelidUpperInner', 'lEyelidUpper', 'lEyelidUpperOuter', 'lEyelidOuter', 'lEyelidLowerOuter', 'lEyelidLower', 'lEyelidLowerInner', 'rEyelidInner', 'rEyelidUpperInner', 'rEyelidUpper', 'rEyelidUpperOuter', 'rEyelidOuter', 'rEyelidLowerOuter', 'rEyelidLower', 'rEyelidLowerInner', 'lSquintInner', 'lSquintOuter', 'rSquintInner', 'rSquintOuter', 'lCheekUpper', 'rCheekUpper', 'Nose', 'lNostril', 'rNostril', 'lLipBelowNose', 'rLipBelowNose', 'lLipUpperOuter', 'lLipUpperInner', 'LipUpperMiddle', 'rLipUpperInner', 'rLipUpperOuter', 'lLipNasolabialCrease', 'rLipNasolabialCrease', 'lNasolabialUpper', 'rNasolabialUpper', 'lNasolabialMiddle', 'rNasolabialMiddle', 'tongue01', 'lNasolabialLower', 'rNasolabialLower', 'lNasolabialMouthCorner', 'rNasolabialMouthCorner', 'lLipCorner', 'lLipLowerOuter', 'lLipLowerInner', 'LipLowerMiddle', 'rLipLowerInner', 'rLipLowerOuter', 'rLipCorner', 'LipBelow', 'Chin', 'lCheekLower', 'rCheekLower', 'BelowJaw', 'lJawClench', 'rJawClench']
        }





        genesis3Toes = {
            "lFoot" : ["lMetatarsals"],
            "rFoot" : ["rMetatarsals"],
            "lToe" : ["lBigToe", "lSmallToe1", "lSmallToe2", "lSmallToe3", "lSmallToe4", "lBigToe_2", "lSmallToe1_2", "lSmallToe2_2", "lSmallToe3_2", "lSmallToe4_2"],
            "rToe" : ["rBigToe", "rSmallToe1", "rSmallToe2", "rSmallToe3", "rSmallToe4", "rBigToe_2", "rSmallToe1_2", "rSmallToe2_2", "rSmallToe3_2", "rSmallToe4_2"]
        }        
        obj_object = bpy.context.selected_objects[0] ####<--Fix
        bpy.context.scene.objects.active = obj_object
        mergeSubgroupsIntoGroup(obj_object, toe_deform01_joint01_L)
        mergeSubgroupsIntoGroup(obj_object, toe_deform01_joint01_R)
        mergeSubgroupsIntoGroup(obj_object, toe_deform02_joint01_L)
        mergeSubgroupsIntoGroup(obj_object, toe_deform02_joint01_R)
        #
        mergeSubgroupsIntoGroup(obj_object, ball_joint_L) 
        mergeSubgroupsIntoGroup(obj_object, ball_joint_R) 
        #
        mergeSubgroupsIntoGroup(obj_object, ankle_joint_L) 
        mergeSubgroupsIntoGroup(obj_object, ankle_joint_R) 
        mergeSubgroupsIntoGroup(obj_object, hip_joint_L)                
        mergeSubgroupsIntoGroup(obj_object, hip_joint_R)   
        mergeSubgroupsIntoGroup(obj_object, shoulder_joint_L)  
        mergeSubgroupsIntoGroup(obj_object, shoulder_joint_R)  
        mergeSubgroupsIntoGroup(obj_object, head_joint02)  
        #
        head_weights_matching = [
        ["head", "head", "head_joint02"],
        ["Chin", "Chin", "chin_joint01"],
        ["LipBelow", "BelowJaw", "lower_jaw_jointEnd"],
        ["lowerJaw","lJawClench","rJawClench","lower_jaw_joint01"],
        ["Nose","MidNoseBridge","lNostril","rNostril","nose_joint02"],
        ["lNasolabialUpper","lNasolabialMiddle","lCheekUpper","lCheekLower","cheek_joint01.L"],
        ["rNasolabialUpper","rNasolabialMiddle","rCheekUpper","rCheekLower","cheek_joint01.R"],
        ["rNasolabialLower","lower_lip_joint01.R"],
        ["lNasolabialLower","lower_lip_joint01.L"],
        ["lLipCorner","lLipLowerOuter","lower_lip_joint02.L"],
        ["rLipCorner","rLipLowerOuter","lower_lip_joint02.R"],
        ["lLipLowerInner","lower_lip_joint03.L"],
        ["rLipLowerInner","lower_lip_joint03.R"],
        ["LipLowerMiddle","lower_lip_jointEnd.L"],
        ["LipLowerMiddle","lower_lip_jointEnd.R"],
        ["lNasolabialMiddle","upper_lip_joint01.L"],
        ["rNasolabialMiddle","upper_lip_joint01.R"],
        ["lLipUpperOuter","lLipNasolabialCrease","upper_lip_joint02.L"],
        ["rLipUpperOuter","rLipNasolabialCrease","upper_lip_joint02.R"],
        ["lLipBelowNose","lLipUpperInner","upper_lip_joint03.L"],
        ["rLipBelowNose","rLipUpperInner","upper_lip_joint03.R"],
        ["LipUpperMiddle","upper_lip_jointEnd.L"],
        ["LipUpperMiddle","upper_lip_jointEnd.R"],
        ["lBrowInner","eye_brow_joint01.L"],
        ["rBrowInner","eye_brow_joint01.R"],
        ["lBrowMid","eye_brow_joint02.L"],
        ["rBrowMid","eye_brow_joint02.R"],
        ["lBrowOuter","eye_brow_jointEnd.L"],
        ["rBrowOuter","eye_brow_jointEnd.R"],
        ["CenterBrow","forehead_jointEnd"],
        ["lEar","ear_joint01.L"],
        ["rEar","ear_joint01.R"]
        ]        
        for row in head_weights_matching:
            param = {row[-1]:row[:-1]} #row[-1] - get last element (vx bone)   ------   row[:-1] returns the list without the last element (daz bones)
            mergeSubgroupsIntoGroup(obj_object, param)  
        #
        #obj_object = bpy.context.active_object
        modifierVertexWeightMixL = obj_object.modifiers.new("modifierVertexWeightMixL", type='VERTEX_WEIGHT_MIX')
        modifierVertexWeightMixL.vertex_group_a = "ball_joint.L"
        modifierVertexWeightMixL.vertex_group_b = "ankle_joint.L"
        modifierVertexWeightMixL.mix_mode = 'SUB'
        modifierVertexWeightMixL.mix_set = 'A'
        #bpy.ops.object.modifier_apply(modifier="customVertexWeightMix")
        #         
        modifierVertexWeightMixR = obj_object.modifiers.new("modifierVertexWeightMixR", type='VERTEX_WEIGHT_MIX')
        modifierVertexWeightMixR.vertex_group_a = "ball_joint.R"
        modifierVertexWeightMixR.vertex_group_b = "ankle_joint.R"
        modifierVertexWeightMixR.mix_mode = 'SUB'
        modifierVertexWeightMixR.mix_set = 'A'
        #bpy.ops.object.modifier_apply(modifier="customVertexWeightMix")        
        #
        #
        for row in spine_weights_matching + leg_weights_matching + hand_weights_matching:
            firstName= row[0]
            secondName= row[1]
            newName= row[2]
            print("Renaming vertex group {0} into {1}".format(firstName,newName))
            if firstName == secondName:
                renameVertexGroup(obj_object, firstName, newName)
        #
        #
        #for row in spine_weights_matching + leg_weights_matching + hand_weights_matching:
        #    vertexGroupForDelete = row[0] 
        #    deleteVertexGroup(obj_object, vertexGroupForDelete)              
        for vg in vertexGroupsForRemoval:
            deleteVertexGroup(obj_object, vg)
        #mergeSubgroupsIntoGroup(obj_object, genesis3Toes)

        #add any missing vertex groups
        all_vertex_groups = ['root', 'spine_joint01', 'spine_joint02', 'spine_joint03', 'spine_joint04', 'spine_jointEnd', 'neck_joint01', 'neck_jointEnd', 'head_joint01', 'head_joint02', 'lower_jaw_joint01', 'lower_jaw_jointEnd', 'chin_joint01', 'chin_jointEnd', 'lower_lip_joint01.R', 'lower_lip_joint02.R', 'lower_lip_joint03.R', 'lower_lip_jointEnd.R', 'lower_lip_joint01.L', 'lower_lip_joint02.L', 'lower_lip_joint03.L', 'lower_lip_jointEnd.L', 'upper_lip_joint01.L', 'upper_lip_joint02.L', 'upper_lip_joint03.L', 'upper_lip_jointEnd.L', 'upper_lip_joint01.R', 'upper_lip_joint02.R', 'upper_lip_joint03.R', 'upper_lip_jointEnd.R', 'eye_socket_joint.L', 'eye_joint.L', 'eye_brow_joint01.L', 'eye_brow_joint02.L', 'eye_brow_jointEnd.L', 'eye_socket_joint.R', 'eye_joint.R', 'eye_brow_joint01.R', 'eye_brow_joint02.R', 'eye_brow_jointEnd.R', 'nose_joint01', 'nose_joint02', 'nose_jointEnd', 'forehead_joint01', 'forehead_jointEnd', 'cheek_joint01.L', 'cheek_jointEnd.L', 'cheek_joint01.R', 'cheek_jointEnd.R', 'ear_joint01.L', 'ear_jointEnd.L', 'ear_joint01.R', 'ear_jointEnd.R', 'head_jointEnd', 'clavicle_joint.L', 'shoulder_joint.L', 'elbow_joint.L', 'forearm_joint.L', 'wrist_joint.L', 'finger01_joint01.L', 'finger01_joint02.L', 'finger01_joint03.L', 'finger01_jointEnd.L', 'finger02_joint01.L', 'finger02_joint02.L', 'finger02_joint03.L', 'finger02_joint04.L', 'finger02_jointEnd.L', 'finger03_joint01.L', 'finger03_joint02.L', 'finger03_joint03.L', 'finger03_joint04.L', 'finger03_jointEnd.L', 'finger04_joint01.L', 'finger04_joint02.L', 'finger04_joint03.L', 'finger04_joint04.L', 'finger04_jointEnd.L', 'finger05_joint01.L', 'finger05_joint02.L', 'finger05_joint03.L', 'finger05_joint04.L', 'finger05_jointEnd.L', 'clavicle_joint.R', 'shoulder_joint.R', 'elbow_joint.R', 'forearm_joint.R', 'wrist_joint.R', 'finger01_joint01.R', 'finger01_joint02.R', 'finger01_joint03.R', 'finger01_jointEnd.R', 'finger02_joint01.R', 'finger02_joint02.R', 'finger02_joint03.R', 'finger02_joint04.R', 'finger02_jointEnd.R', 'finger03_joint01.R', 'finger03_joint02.R', 'finger03_joint03.R', 'finger03_joint04.R', 'finger03_jointEnd.R', 'finger04_joint01.R', 'finger04_joint02.R', 'finger04_joint03.R', 'finger04_joint04.R', 'finger04_jointEnd.R', 'finger05_joint01.R', 'finger05_joint02.R', 'finger05_joint03.R', 'finger05_joint04.R', 'finger05_jointEnd.R', 'breast_joint.L', 'breast_scale_joint.L', 'nipple_joint01.L', 'nipple_jointEnd.L', 'breast_deform01_joint01.L', 'breast_deform01_jointEnd.L', 'breast_deform02_joint01.L', 'breast_deform02_jointEnd.L', 'breast_deform03_joint01.L', 'breast_deform03_jointEnd.L', 'breast_joint.R', 'breast_scale_joint.R', 'nipple_joint01.R', 'nipple_jointEnd.R', 'breast_deform01_joint01.R', 'breast_deform01_jointEnd.R', 'breast_deform02_joint01.R', 'breast_deform02_jointEnd.R', 'breast_deform03_joint01.R', 'breast_deform03_jointEnd.R', 'rib_joint01.L', 'rib_jointEnd.L', 'rib_joint01.R', 'rib_jointEnd.R', 'stomach_joint01', 'stomach_jointEnd', 'hip_joint.L', 'knee_joint.L', 'ankle_joint.L', 'ball_joint.L', 'toe_joint.L', 'toe_deform01_joint01.L', 'toe_deform01_jointEnd.L', 'toe_deform02_joint01.L', 'toe_deform02_jointEnd.L', 'hip_joint.R', 'knee_joint.R', 'ankle_joint.R', 'ball_joint.R', 'toe_joint.R', 'toe_deform01_joint01.R', 'toe_deform01_jointEnd.R', 'toe_deform02_joint01.R', 'toe_deform02_jointEnd.R', 'penis_joint01', 'penis_joint02', 'penis_joint03', 'penis_jointEnd', 'testicles_joint01', 'testicles_joint02', 'testicles_jointEnd', 'vagina_joint01.L', 'vagina_joint01.R', 'vagina_jointEnd.L', 'vagina_jointEnd.R', 'butt_joint01.L', 'butt_jointEnd.L', 'butt_joint01.R', 'butt_jointEnd.R', 'anus_joint']
        for group in all_vertex_groups:
            if group in obj_object.vertex_groups.keys():
                pass
            else:
                vg = obj_object.vertex_groups.new(group)

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
    #bpy.app.handlers.scene_update_post.append(post_ob_data_updated)
    

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