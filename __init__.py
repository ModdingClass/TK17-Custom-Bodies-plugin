bl_info = {
    "name": "Game Mod Tiny Tools",
    "author": "ModdingClass",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "description": "Game oriented tools for quick prototyping",
    "warning": "",
    "wiki_url": "",
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


from .utilz import *
from .armatures import *
from .materials import *
from .vertex_groups import *
from .shapekeys import *

if "bpy" in locals():
    import imp
    imp.reload(utilz)
    imp.reload(armatures)
    imp.reload(materials)
    imp.reload(vertex_groups)
    imp.reload(shapekeys)
    print("Reloaded multifiles")
else:
    from . import utilz
    from . import armatures
    from . import materials    
    from . import vertex_groups   
    from . import shapekeys  
    print("Imported multifiles")



# Operator for exporting armature data
class ARMATURE_OT_ExportArmatureDataToJson(bpy.types.Operator, ExportHelper):
    bl_idname = "export.armature_data_to_json"
    bl_label = "Export"
    bl_description = "Export armature data to JSON file"
    filename_ext = ".json"  # The file extension for the export

    # Filepath is handled by ExportHelper

    def execute(self, context):
        # Call the separated utility function to handle export
        result = export_armature_data(context, self.filepath)
        return result

# Operator for importing armature data
class ARMATURE_OT_ImportArmatureDataFromJson(bpy.types.Operator, ImportHelper):
    bl_idname = "import.armature_data_from_json"
    bl_label = "Import"
    bl_description = "Import armature data to JSON file"
    filename_ext = ".json"  # The file extension for the export

    # Filepath is handled by ImportHelper

    def execute(self, context):
        # Call the separated utility function to handle export
        result = import_armature_data(context, self.filepath)
        return result

# Operator for importing armature data
class ARMATURE_OT_CreateAndImportArmatureDataFromJson(bpy.types.Operator, ImportHelper):
    bl_idname = "import.create_and_import_armature_data_from_json"
    bl_label = "Import"
    bl_description = "Import new armature data to JSON file"
    filename_ext = ".json"  # The file extension for the export

    # Filepath is handled by ImportHelper

    def execute(self, context):
        # Call the separated utility function to handle export
        result = create_and_import_armature_data(context, self.filepath)
        return result    

# Panel for the exporter
class ARMATURE_PT_VXMod_armature_tools(bpy.types.Panel):
    bl_label = "VXMod Armature Tools"
    bl_idname = "ARMATURE_PT_VXMod_armature_tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    #
    @classmethod
    def poll(cls, context):
        # Check if the context is for an armature
        return context.object and context.object.type == 'ARMATURE'
    #
    def draw(self, context):
        layout = self.layout
        layout.operator("import.armature_data_from_json", text="Import Armature Data", icon='OUTLINER_DATA_ARMATURE')
        layout.operator("export.armature_data_to_json", text="Export Armature Data", icon='OUTLINER_DATA_ARMATURE')
    


def draw_add_custom_armature_importer_in_menu(self, context):
    layout = self.layout
    layout.operator("import.create_and_import_armature_data_from_json", text="Import From JSON file", icon='IMPORT')


# this class extends ExportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class EXPORT_OT_MaterialsToJson(Operator, ExportHelper):
    ''''''
    bl_idname = "export.materials_to_json"
    bl_label = "Export materials"
    bl_description = "Exports materials to a custom json file"

    filename_ext = ".json"  # ExportHelper mixin class uses this
    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        ob = bpy.context.object
        exportMaterialsToJsonFile(ob, self.filepath)
        return {'FINISHED'}


# this class extends ImportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class IMPORT_OT_MaterialsFromJson(Operator, ImportHelper):
    ''''''
    bl_idname = "import.materials_from_json"
    bl_label = "Import materials"
    bl_description = "Import materials from a custom json file"

    filter_glob = StringProperty(
        default='*.json',
        options={'HIDDEN'}
    )
    
    def execute(self, context):
        ob = bpy.context.object
        importMaterialsFromJsonFile(ob, self.filepath)
        return {'FINISHED'}
    

class OBJECT_OT_sort_materials(bpy.types.Operator):
    """Sort materials alphabetically in the material slots"""
    bl_idname = "object.sort_materials"
    bl_label = "Sort Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ob = context.object
        
        # Call the separate function to sort materials
        if not sort_materials_in_object(ob):
            self.report({'WARNING'}, "Object has no materials to sort")
            return {'CANCELLED'}

        return {'FINISHED'}


def draw_add_custom_sort_in_materials_dropdown_menu(self, context):
    self.layout.separator()
    self.layout.operator(
        OBJECT_OT_sort_materials.bl_idname, 
        text="Sort Materials", 
        icon='SORTALPHA'
    )
    self.layout.operator(
        IMPORT_OT_MaterialsFromJson.bl_idname, 
        text="Import Materials", 
        icon='IMPORT'
    )
    self.layout.operator(
        EXPORT_OT_MaterialsToJson.bl_idname, 
        text="Export Materials", 
        icon='EXPORT'
    )     



# this class extends ExportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class EXPORT_OT_VertexWeightsToJson(Operator, ExportHelper):
    ''''''
    bl_idname = "export.vertex_weights_to_json"
    bl_label = "Export weights to JSON"
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
class IMPORT_OT_VertexWeightsFromJson(Operator, ImportHelper):
    ''''''
    bl_idname = "import.vertex_weights_from_json"
    bl_label = "Import weights from JSON"
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

def draw_add_custom_functions_in_vertex_groups_dropdown_menu(self, context):
    self.layout.separator()
    self.layout.operator(
        IMPORT_OT_VertexWeightsFromJson.bl_idname, 
        text="Import Weights from JSON", 
        icon='IMPORT'
    )
    self.layout.operator(
        EXPORT_OT_VertexWeightsToJson.bl_idname, 
        text="Export Weights to JSON", 
        icon='EXPORT'
    )       


# this class extends ExportHelper !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class EXPORT_OT_Shapekeys_To_Json(Operator, ExportHelper):
    ''''''
    bl_idname = "export.shapekeys_to_json"
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
class IMPORT_OT_Shapekeys_From_Json(Operator, ImportHelper):
    ''''''
    bl_idname = "import.shapekeys_from_json"
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


class OBJECT_OT_split_shape_key_by_axis(bpy.types.Operator):
    """Split selected shape key into X, Y, Z components"""
    bl_idname = "object.split_shape_key_by_axis"
    bl_label = "Split Shape Key by Axis"
    bl_options = {'REGISTER', 'UNDO'}
    #
    @classmethod
    def poll(cls, context):
        obj = context.object
        if (1==1):
            print ("polling is True")
            return True
        if obj and obj.type == 'MESH':
            return len(obj.data.shape_keys.key_blocks) > 0 and any(keyblock.select for keyblock in obj.data.shape_keys.key_blocks)
        return False
    #    
    def execute(self, context):
        obj = context.object
        print("executed, but: {}".format( len(obj.data.shape_keys.key_blocks) > 0 and any(keyblock.select for keyblock in obj.data.shape_keys.key_blocks)))
        if obj and obj.type == 'MESH' and obj.active_shape_key_index > 0:
            split_shape_key_by_axis(obj, obj.active_shape_key_index)
            return {'FINISHED'}
        return {'CANCELLED'}


def draw_add_custom_functions_in_shapekeys_dropdown_menu(self, context):
    self.layout.separator()
    op_row = self.layout.row()
    op_row.operator(
        OBJECT_OT_split_shape_key_by_axis.bl_idname,
        text="Split Shapekey by Axis", 
        icon='MONKEY'
    )
    obj = context.object
    shape_keys = obj.data.shape_keys if obj and obj.type == 'MESH' else None
    # Check if there are shape keys and if any shape key is selected
    if ( obj.data.shape_keys != None and len(obj.data.shape_keys.key_blocks)>1 ):
        pass
    else:
        op_row.enabled=False
    self.layout.operator(
        IMPORT_OT_Shapekeys_From_Json.bl_idname, 
        text="Import Shapekeys from JSON", 
        icon='IMPORT'
    )
    op_row = self.layout.row()
    op_row.operator(
        EXPORT_OT_Shapekeys_To_Json.bl_idname, 
        text="Export Shapekeys to JSON", 
        icon='EXPORT'
    )
    if ( obj.data.shape_keys != None and len(obj.data.shape_keys.key_blocks)>1 ):
        pass
    else:
        op_row.enabled=False    





# Register and unregister classes
def register():
    bpy.utils.register_class(ARMATURE_OT_ExportArmatureDataToJson)
    bpy.utils.register_class(ARMATURE_OT_ImportArmatureDataFromJson)
    bpy.utils.register_class(ARMATURE_OT_CreateAndImportArmatureDataFromJson)
    bpy.types.INFO_MT_armature_add.append(draw_add_custom_armature_importer_in_menu)
    bpy.utils.register_class(ARMATURE_PT_VXMod_armature_tools)
    #    
    bpy.utils.register_class(IMPORT_OT_MaterialsFromJson)
    bpy.utils.register_class(EXPORT_OT_MaterialsToJson)    
    bpy.utils.register_class(OBJECT_OT_sort_materials)    
    bpy.types.MATERIAL_MT_specials.append(draw_add_custom_sort_in_materials_dropdown_menu)
    #
    bpy.utils.register_class(EXPORT_OT_VertexWeightsToJson)
    bpy.utils.register_class(IMPORT_OT_VertexWeightsFromJson)
    bpy.types.MESH_MT_vertex_group_specials.append(draw_add_custom_functions_in_vertex_groups_dropdown_menu)
    #
    bpy.utils.register_class(EXPORT_OT_Shapekeys_To_Json)
    bpy.utils.register_class(IMPORT_OT_Shapekeys_From_Json)
    bpy.types.MESH_MT_shape_key_specials.append(draw_add_custom_functions_in_shapekeys_dropdown_menu)
    

def unregister():
    bpy.utils.unregister_class(ARMATURE_OT_ExportArmatureDataToJson)
    bpy.utils.unregister_class(ARMATURE_OT_ImportArmatureDataFromJson)
    bpy.utils.unregister_class(ARMATURE_OT_CreateAndImportArmatureDataFromJson)    
    bpy.types.INFO_MT_armature_add.remove(draw_add_custom_armature_importer_in_menu)    
    bpy.utils.unregister_class(ARMATURE_PT_VXMod_armature_tools)
    #
    bpy.utils.unregister_class(IMPORT_OT_MaterialsFromJson)    
    bpy.utils.unregister_class(EXPORT_OT_MaterialsToJson)    
    bpy.utils.unregister_class(OBJECT_OT_sort_materials)
    bpy.types.MATERIAL_MT_specials.remove(draw_add_custom_sort_in_materials_dropdown_menu)  
    #
    bpy.utils.unregister_class(EXPORT_OT_VertexWeightsToJson)
    bpy.utils.unregister_class(IMPORT_OT_VertexWeightsFromJson)
    bpy.types.MESH_MT_vertex_group_specials.remove(draw_add_custom_functions_in_vertex_groups_dropdown_menu)
    #
    bpy.utils.unregister_class(EXPORT_OT_Shapekeys_To_Json)
    bpy.utils.unregister_class(IMPORT_OT_Shapekeys_From_Json)
    bpy.types.MESH_MT_shape_key_specials.remove(draw_add_custom_functions_in_shapekeys_dropdown_menu)    



if __name__ == "__main__":
    register()
