import bpy, mathutils
import re
from collections import OrderedDict
import winsound
import ctypes
from ctypes import wintypes
import os
import time
from .utils import *
from .tools_message_box import *

from mathutils import Vector
from mathutils import Matrix
from math import radians

from math import degrees
from bpy_extras.io_utils import axis_conversion

import bpy
import json

def deselect_all_objects():
    bpy.ops.object.select_all(action='DESELECT')
    #for ob in bpy.context.selected_objects:
    #    ob.select = False

def operator_exists(idname):
    from bpy.ops import op_as_string
    try:
        op_as_string(idname)
        return True
    except:
        return False

def create_vertex_groups_dict(obj):
    # ensure we got the latest assignments and weights
    obj.update_from_editmode()
    mesh = obj.data
    # create vertex group lookup dictionary for names
    vgroup_names = {vgroup.index: vgroup.name for vgroup in obj.vertex_groups}
    # create dictionary of vertex group assignments per vertex
    vgroups = {v.index: [int(vgroup_names[g.group].lstrip("Group_")) for g in v.groups] for v in mesh.vertices}
    return vgroups

def save_to_csv(vgroups, filepath):
    with open(filepath, 'w') as csvfile:
        # Write header
        csvfile.write('Vertex_Index,Vertex_Groups\n')
        # Write data
        for vertex_index, groups in vgroups.items():
            # Enclose vertex groups in parentheses and join them as a string
            groups_str = '({})'.format(', '.join(map(str, groups)))
            csvfile.write('{},{}\n'.format(vertex_index, groups_str))


def assign_vertex_groups(obj):
    mesh = obj.data
    vertex_groups = []
    # Create vertex groups for each vertex
    for i in range(len(mesh.vertices)):
        group_name = "Group_{}".format(i)
        vertex_groups.append(group_name)
        obj.vertex_groups.new(name=group_name)
    # Assign vertices to their respective groups
    for v in mesh.vertices:
        obj.vertex_groups["Group_{}".format(v.index)].add([v.index], 1, 'REPLACE')


def strip_and_clean_selected_object():
    ob = bpy.context.active_object
    deselect_all_objects()
    ob.select = True
    bpy.context.scene.objects.active = ob    
    # Remove all materials
    ob.active_material_index = 0
    print("removing materials")
    for x in bpy.context.object.material_slots: #For all of the materials in the selected object:
        bpy.context.object.active_material_index = 0 #select the top material
        bpy.ops.object.material_slot_remove() #delete it    
    #for i in range(len(ob.material_slots)):
    #    bpy.ops.object.material_slot_remove({'object': ob})    
    print("removing materials DONME")
    # Remove all shape keys
    if ob.data.shape_keys:
        bpy.ops.object.shape_key_remove(all=True)
    # Remove all vertex groups
    bpy.ops.object.vertex_group_remove(all=True)


def duplicate_selected_object(newObjectName=None):
    if len(bpy.context.selected_objects)==0:
        ShowMessageBox("No object is selected", "Error", 'ERROR')
        return None              
    return duplicate_object_by_name( bpy.context.selected_objects[0].name , newObjectName)

def duplicate_object_by_name(sourceObjectName=None, newObjectName=None):
    if sourceObjectName is None:
        # Select the active object (assumes only one is selected)
        bpy.context.scene.objects.active = bpy.context.selected_objects[0]
    #
    if bpy.data.objects.get(sourceObjectName) is None:
        ShowMessageBox("Can't find object: "+sourceObjectName, "Error", 'ERROR')
        return None
    deselect_all_objects()
    ob = bpy.data.objects[sourceObjectName]
    ob.select = True
    bpy.context.scene.objects.active = ob
    # Duplicate the selected object
    bpy.ops.object.duplicate(linked=False)
    # The new duplicated object becomes the active object
    new_object = bpy.context.active_object
    if newObjectName is not None:
        new_object.name = newObjectName
    return new_object



def build_subdivision_vertex_matching_table(exportfolderpath, includeGeograftsOnExport) : 
    # a ton of boilerplate checks comes next
    if bpy.data.objects.get("body_subdiv_cage") is None:
        ShowMessageBox("Can't find object: body_subdiv_cage", "Error", 'ERROR')
        return None

    if bpy.data.objects["body_subdiv_cage"].hide :
        ShowMessageBox("'body_subdiv_cage' object is not visible!", "Error", 'ERROR')
        return None

    armature_modifier = next((mod for mod in bpy.data.objects["body_subdiv_cage"].modifiers if mod.type == 'ARMATURE'), None)
    armature_object = armature_modifier.object if armature_modifier else None

    if armature_object is None:
        ShowMessageBox("'body_subdiv_cage' object has no armature!", "Error", 'ERROR')
        return None        
    armature_object.hide = False
    
    exportfolderpath = os.path.join(exportfolderpath,"")    
    if not os.path.exists(exportfolderpath):
        os.makedirs(exportfolderpath)
    
    hiddenStatusGeografts = {}
    mergeGeografts = []
    anatomies = []
    ob = bpy.data.objects["body_subdiv_cage"]
    ob.select = True
    bpy.context.scene.objects.active = ob
    
    if not includeGeograftsOnExport:
        pass
    else:
        if ( operator_exists("daz.merge_geografts_fast") or operator_exists("daz.merge_geografts") or operator_exists("daz.merge_geografts_nondestructive")):
            pass
        else:
            ShowMessageBox("'Include Geografts' is checked, but can't find `modded` Difeomorphic addon for Blender", "Error", 'ERROR')
            return None
        if ob.data.get("mergeGeografts") is None:
                ShowMessageBox("'Include Geografts' is checked, but you are missing 'mergeGeografts' property in data block Custom Properties", "Error", 'ERROR')
                return None
        if len(ob.data["mergeGeografts"].strip()) == 0 :
                ShowMessageBox("'Include Geografts' is checked, but empty 'mergeGeografts' in data block Custom Properties", "Error", 'ERROR')
                return None
        mergeGeografts = ob.data["mergeGeografts"].split(",")
        if len(mergeGeografts)==0:
            ShowMessageBox("'Include Geografts' is checked, but empty 'mergeGeografts' in data block Custom Properties", "Error", 'ERROR')
            return None
        else:
            for geo in mergeGeografts:
                ob = bpy.data.objects.get(geo)
                if ob is None:
                    ShowMessageBox("'Include Geografts' is checked, but the object with name: "+geo+" is missing", "Error", 'ERROR')    
                    return None
                if ob.type != 'MESH':
                    ShowMessageBox("'Include Geografts' is checked, but the object with name: "+geo+" is not a Mesh type", "Error", 'ERROR')    
                    return None       
                hiddenStatusGeografts[ob.name] = ob.hide      
                if ob.hide :
                    ob.hide = False # we need to show it
                    #ShowMessageBox("Geograft object '"+ ob.name +"' is not visible!", "Error", 'ERROR')
                    #return None                

    ob = bpy.data.objects["body_subdiv_cage"]
    ob.select = True
    bpy.context.scene.objects.active = ob
    bpy.ops.object.duplicate(linked=False)
    fbody = bpy.context.scene.objects.active
    fbody.name = "fbody_from_subdivide_operator"
    
    if includeGeograftsOnExport:
        print("includeGeograftsOnExport is ON")
        #deselect_all_objects()       
        #
        #
        for geo in mergeGeografts:
            deselect_all_objects()
            ob = bpy.data.objects[geo]
            ob.select = True
            bpy.context.scene.objects.active = ob
            bpy.ops.object.duplicate(linked=False)
            geoClone = bpy.context.scene.objects.active
            geoClone.parent = fbody
            anatomies.append(geoClone)
            bpy.data.objects[geo].hide = hiddenStatusGeografts[ob.name] # we need to restore the hidden status
        #
        deselect_all_objects()
        #
        for geo in anatomies:
            geo.select = True
            bpy.context.scene.objects.active = geo        
        fbody.select=True
        bpy.context.scene.objects.active = fbody
        fbody.select=True
        if ( operator_exists("daz.merge_geografts_nondestructive") ):
            print("daz.merge_geografts_nondestructive is available :)")
            bpy.ops.daz.merge_geografts_nondestructive()        
        elif ( operator_exists("daz.merge_geografts_fast") ):
            print("daz.merge_geografts_fast is available")
            bpy.ops.daz.merge_geografts_fast()
        else: 
            print("daz.merge_geografts fallback :(")
            bpy.ops.daz.merge_geografts()
    
    
    deselect_all_objects()
    fbody.select=True
    bpy.context.scene.objects.active = fbody
    #remove everything that is not required from fbody
    strip_and_clean_selected_object()
    # Remove all shape keys from fbody_hires
    if fbody.data.shape_keys:
        bpy.ops.object.shape_key_remove(all=True)    
    # Clear all modifiers
    for modifier in fbody.modifiers:
        fbody.modifiers.remove(modifier)
    #
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    # Clear existing vertex groups
    fbody.vertex_groups.clear()
    #
    # Iterate over all vertices in the mesh
    for i, vertex in enumerate(fbody.data.vertices):
        # Create a new vertex group named after the vertex index
        vg = fbody.vertex_groups.new(name=str(i))
        #
        # Add the vertex to the group with a weight of 1.0
        vg.add([i], 1.0, 'ADD')
        #
    print("Assigned weights to all fbody vertices.")    
    #
    #
    ob = bpy.context.scene.objects.active
    print("Creating fbody_hires!") 
    fbody_hires = duplicate_object_by_name("fbody_from_subdivide_operator","fbody_from_subsurf_modifier")
    bpy.context.scene.objects.active = fbody_hires
    # Remove all shape keys from fbody_hires
    if fbody_hires.data.shape_keys:
        bpy.ops.object.shape_key_remove(all=True)
    #
    # Clear all modifiers
    for modifier in fbody_hires.modifiers:
        fbody_hires.modifiers.remove(modifier)
    # Add a Subdivision Surface modifier
    bpy.ops.object.modifier_add(type='SUBSURF')
    subsurf_modifier = fbody_hires.modifiers[-1] # get the last modifier (hence -1)
    subsurf_modifier.levels = 1  # Set the subdivision levels as needed
    # Apply the Subdivision Surface modifier
    bpy.ops.object.modifier_apply( modifier = subsurf_modifier.name )
    #
    fbody.select = True        
    #
    bpy.context.scene.objects.active = fbody
    # Switch to Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')
    # Subdivide the selected vertices
    bpy.ops.mesh.subdivide()
    # Switch back to Object Mode (optional)
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    deselect_all_objects()
    # lets create the lookup dict for fbody (subdiv operator in edit mode)
    fbody.select = True        
    #
    bpy.context.scene.objects.active = fbody
    #
    vertex_groups_dict = {}
    # Ensure the object exists and is a mesh
    if fbody and fbody.type == 'MESH':
        # Initialize an empty dictionary to store vertex groups for each vertex
        # Loop through all vertices in the mesh
        for vertex in fbody.data.vertices:
            # List to store the vertex group indices for the current vertex
            group_indices = []
            # Loop through the vertex groups assigned to the vertex
            for group_element in vertex.groups:
                # Get the group index
                group_indices.append(str(group_element.group))
            # Sort the group indices
            group_indices.sort(key=int)
            # Concatenate the group indices with underscores and add to dictionary
            vertex_groups_dict[vertex.index] = "_".join(group_indices)
        # Print the resulting dictionary
        print(vertex_groups_dict)
    else:
        print("The specified object either does not exist or is not a mesh.")
    # lets create the lookup dict for fbody_hires (subsurf modifier)
    deselect_all_objects()
    fbody_hires.select = True        
    #
    bpy.context.scene.objects.active = fbody_hires
    #
    vertex_groups_dict_backwards = {}
    # Ensure the object exists and is a mesh
    if fbody_hires and fbody_hires.type == 'MESH':
        # Initialize an empty dictionary to store vertex groups for each vertex\
        # Loop through all vertices in the mesh
        for vertex in fbody_hires.data.vertices:
            # List to store the vertex group indices for the current vertex
            group_indices = []
            # Loop through the vertex groups assigned to the vertex
            for group_element in vertex.groups:
                # Get the group index
                group_indices.append(str(group_element.group))
            # Sort the group indices
            group_indices.sort(key=int)
            # Concatenate the group indices with underscores and add to dictionary
            vertex_groups_dict_backwards["_".join(group_indices)] = vertex.index
        # Print the resulting dictionary
        print(vertex_groups_dict_backwards)
    else:
        print("The specified object either does not exist or is not a mesh.")
    #
    deselect_all_objects()
    # lets create the final matching lookup dict 
    fbody.select = True        
    #
    bpy.context.scene.objects.active = fbody
    # Ensure the object exists and is a mesh
    if fbody and fbody.type == 'MESH':
        fbody_matching_index_dict = OrderedDict()
        # Loop through all vertices in the mesh
        for vertex in fbody.data.vertices:
            fbody_matching_index_dict[vertex.index]=vertex_groups_dict_backwards[vertex_groups_dict[vertex.index]]
            fbody_matching_index_dict
        # Convert dictionary to a JSON string
        dict_as_string = json.dumps(fbody_matching_index_dict)
        # Store it in the Scene's custom properties
        #or maybe not?!?!
        #bpy.context.scene['my_global_fbody_matching_index_dict'] = dict_as_string
        # Specify the file path where you want to save the JSON file
        # Make sure you have permission to write to this location
        file_path = os.path.join(exportfolderpath,"fbody_matching_index_dict.json")
        # Save the lookup table to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(fbody_matching_index_dict, json_file)
        print("Lookup table saved to:", file_path)


def load_fbody_matching_index_dict_from_json(exportfolderpath, includeGeograftsOnExport) : 
    #
    #if 'my_global_fbody_matching_index_dict' in bpy.context.scene:
    #    stored_string = bpy.context.scene['my_global_fbody_matching_index_dict']
    # Load the JSON data from the file
    file_path = os.path.join(exportfolderpath,"fbody_matching_index_dict.json")
    with open(file_path, 'r') as json_file:
        loaded_dict = json.load(json_file)
    # Convert the keys back to integers
    int_key_dict = {int(k): v for k, v in loaded_dict.items()}
    # Optionally convert it back to an OrderedDict if needed
    loaded_ordered_dict = OrderedDict(int_key_dict)
    print(loaded_ordered_dict)  # Output: {'a': 1, 'b': 2, 'c': 3}
    print(loaded_ordered_dict[0])
    #


def export_to_unreal(exportfolderpath,exportFilename, includeGeograftsOnExport) : #exportfolderpath,
    #
    # a ton of boilerplate checks comes next
    if bpy.data.objects.get("body_subdiv_cage") is None:
        ShowMessageBox("Can't find object: body_subdiv_cage", "Error", 'ERROR')
        return None

    if bpy.data.objects["body_subdiv_cage"].hide :
        ShowMessageBox("'body_subdiv_cage' object is not visible!", "Error", 'ERROR')
        return None

    armature_modifier = next((mod for mod in bpy.data.objects["body_subdiv_cage"].modifiers if mod.type == 'ARMATURE'), None)
    armature_object = armature_modifier.object if armature_modifier else None

    if armature_object is None:
        ShowMessageBox("'body_subdiv_cage' object has no armature!", "Error", 'ERROR')
        return None        
    armature_object.hide = False

    exportfolderpath = os.path.join(exportfolderpath,"")    
    if not os.path.exists(exportfolderpath):
        os.makedirs(exportfolderpath)
    
    hiddenStatusGeografts = {}
    mergeGeografts = []
    anatomies = []
    ob = bpy.data.objects["body_subdiv_cage"]
    ob.select = True
    bpy.context.scene.objects.active = ob
    
    if not includeGeograftsOnExport:
        pass
    else:
        if ( operator_exists("daz.merge_geografts_fast") or operator_exists("daz.merge_geografts") or operator_exists("daz.merge_geografts_nondestructive")):
            pass
        else:
            ShowMessageBox("'Include Geografts' is checked, but can't find `modded` Difeomorphic addon for Blender", "Error", 'ERROR')
            return None
        if ob.data.get("mergeGeografts") is None:
                ShowMessageBox("'Include Geografts' is checked, but you are missing 'mergeGeografts' property in data block Custom Properties", "Error", 'ERROR')
                return None
        if len(ob.data["mergeGeografts"].strip()) == 0 :
                ShowMessageBox("'Include Geografts' is checked, but empty 'mergeGeografts' in data block Custom Properties", "Error", 'ERROR')
                return None
        mergeGeografts = ob.data["mergeGeografts"].split(",")
        if len(mergeGeografts)==0:
            ShowMessageBox("'Include Geografts' is checked, but empty 'mergeGeografts' in data block Custom Properties", "Error", 'ERROR')
            return None
        else:
            for geo in mergeGeografts:
                ob = bpy.data.objects.get(geo)
                if ob is None:
                    ShowMessageBox("'Include Geografts' is checked, but the object with name: "+geo+" is missing", "Error", 'ERROR')    
                    return None
                if ob.type != 'MESH':
                    ShowMessageBox("'Include Geografts' is checked, but the object with name: "+geo+" is not a Mesh type", "Error", 'ERROR')    
                    return None       
                hiddenStatusGeografts[ob.name] = ob.hide      
                if ob.hide :
                    ob.hide = False # we need to show it
                    #ShowMessageBox("Geograft object '"+ ob.name +"' is not visible!", "Error", 'ERROR')
                    #return None                

    ob = bpy.data.objects["body_subdiv_cage"]
    ob.select = True
    bpy.context.scene.objects.active = ob
    bpy.ops.object.duplicate(linked=False)
    fbody = bpy.context.scene.objects.active
    fbody.name = "fbody"
    
    if includeGeograftsOnExport:
        #deselect_all_objects()       
        #
        #
        for geo in mergeGeografts:
            deselect_all_objects()
            ob = bpy.data.objects[geo]
            ob.select = True
            bpy.context.scene.objects.active = ob
            bpy.ops.object.duplicate(linked=False)
            geoClone = bpy.context.scene.objects.active
            geoClone.parent = fbody
            anatomies.append(geoClone)
            bpy.data.objects[geo].hide = hiddenStatusGeografts[ob.name] # we need to restore the hidden status
        #
        deselect_all_objects()
        #
        for geo in anatomies:
            geo.select = True
            bpy.context.scene.objects.active = geo        
        fbody.select=True
        bpy.context.scene.objects.active = fbody
        fbody.select=True
        if ( operator_exists("daz.merge_geografts_nondestructive") ):
            print("daz.merge_geografts_nondestructive is available :)")
            bpy.ops.daz.merge_geografts_nondestructive()        
        elif ( operator_exists("daz.merge_geografts_fast") ):
            print("daz.merge_geografts_fast is available")
            bpy.ops.daz.merge_geografts_fast()
        else: 
            print("daz.merge_geografts fallback :(")
            bpy.ops.daz.merge_geografts()
    
    
    deselect_all_objects()
    fbody.select=True
    bpy.context.scene.objects.active = fbody
    # Clear all modifiers
    for modifier in fbody.modifiers:
        fbody.modifiers.remove(modifier)


    ob = bpy.context.scene.objects.active
    print("Creating fbody_hires!") 
    fbody_hires = duplicate_object_by_name("fbody","fbody_hires")
    bpy.context.scene.objects.active = fbody_hires
    # Remove all shape keys from fbody_hires
    if fbody_hires.data.shape_keys:
        bpy.ops.object.shape_key_remove(all=True)
    #
    # Clear all modifiers
    for modifier in fbody_hires.modifiers:
        fbody_hires.modifiers.remove(modifier)
    # Add a Subdivision Surface modifier
    bpy.ops.object.modifier_add(type='SUBSURF')
    subsurf_modifier = fbody_hires.modifiers[-1] # get the last modifier (hence -1)
    subsurf_modifier.levels = 1  # Set the subdivision levels as needed
    # Apply the Subdivision Surface modifier
    bpy.ops.object.modifier_apply( modifier = subsurf_modifier.name )
    #
    print("Creating fbody_stripped!") 
    fbody_stripped = duplicate_object_by_name("fbody","fbody_stripped")
    deselect_all_objects()
    fbody_stripped.select=True
    bpy.context.scene.objects.active = fbody_stripped
    print("strip_and_clean_selected_object!") 
    strip_and_clean_selected_object()
    print("strip_and_clean_selected_object! DOENE") 
    """     # Remove all materials
    #fbody_stripped.data.materials.clear()
    fbody_stripped.active_material_index = 0
    for i in range(len(fbody_stripped.material_slots)):
        bpy.ops.object.material_slot_remove({'object': fbody_stripped})    
    # Remove all shape keys
    if fbody_stripped.data.shape_keys:
        bpy.ops.object.shape_key_remove(all=True)
    # Remove all vertex groups
    bpy.ops.object.vertex_group_remove(all=True)
    """
    
    # Clear all modifiers
    for modifier in fbody_stripped.modifiers:
        fbody_stripped.modifiers.remove(modifier)
    #
    deselect_all_objects()
    fbody.select = True        
    #
    bpy.context.scene.objects.active = fbody

    if fbody.data.shape_keys is None:
        print("Source object has no shape keys!") 
    else:
        sk_counter = len(fbody.data.shape_keys.key_blocks)
        for idx in range(1, sk_counter):
            fbody.select = True
            bpy.context.scene.objects.active = fbody
            fbody.active_shape_key_index = idx
            skname = fbody.active_shape_key.name
            print("Copying Shape Key - ", skname)
            chupacabra_morph = duplicate_object_by_name("fbody_stripped","chupacabramorph_"+skname)
            deselect_all_objects()
            fbody.select = True
            chupacabra_morph.select = True
            bpy.context.scene.objects.active = chupacabra_morph
            bpy.ops.object.shape_key_transfer()
            chupacabra_morph.active_shape_key_index = chupacabra_morph.data.shape_keys.key_blocks.keys().index(skname)
            bpy.ops.object.shape_key_clear()
            chupacabra_morph.data.shape_keys.key_blocks[skname].value = 1.0
            # set index to Basis shapekey and remove it
            chupacabra_morph.active_shape_key_index = 0
            bpy.ops.object.shape_key_remove(all=False)
            # Apply the shapekey
            print("Apply the shapekey - ", skname)
            #bpy.ops.object.shape_key_add(from_mix=True)
            # Remove the real shapekey which now is the Basis
            bpy.ops.object.shape_key_remove(all=True)
            # Add a Subdivision Surface modifier
            print("Apply subdiv... ")
            bpy.ops.object.modifier_add(type='SUBSURF')
            chupacabra_subsurf_modifier = chupacabra_morph.modifiers[-1] # get the last modifier (hence -1)
            chupacabra_subsurf_modifier.levels = 1  # Set the subdivision levels as needed
            # Apply the Subdivision Surface modifier
            bpy.ops.object.modifier_apply( modifier = chupacabra_subsurf_modifier.name )  
            chupacabra_subsurf_modifier = None 
            deselect_all_objects()
            chupacabra_morph.select=True
            fbody_hires.select=True
            bpy.context.scene.objects.active = fbody_hires
            print("Execute join_shapes")
            bpy.ops.object.join_shapes()
            deselect_all_objects()
            chupacabra_morph.select=True
            bpy.context.scene.objects.active = chupacabra_morph
            print("Deleting object: "+chupacabra_morph.name)
            chupacabra_morph = None
            bpy.ops.object.delete()
    #
    deselect_all_objects()
    fbody_hires.select=True
    bpy.context.scene.objects.active = fbody_hires
    # get its shapekeys
    if fbody_hires.data.shape_keys != None:
        shape_keys = fbody_hires.data.shape_keys.key_blocks
        for index, key in enumerate(shape_keys):
            if key.name != "Basis":
                try: key.name = key.name[len("chupacabramorph_"):]   #prefix with MorphTarget_ ???
                except: pass    
    #
    deselect_all_objects()
    fbody_stripped.select=True
    bpy.context.scene.objects.active = fbody_stripped
    print("Deleting object: "+fbody_stripped.name)
    fbody_stripped = None
    bpy.ops.object.delete()
    #
    p = axis_conversion(
        from_forward='Y',
        from_up='Z',
        to_forward='X',
        to_up='Y'
        ).to_4x4()
    #
    deselect_all_objects()
    armature_object.select=True
    bpy.context.scene.objects.active = armature_object
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.duplicate(linked=False)
    armature_clone = bpy.context.scene.objects.active
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    armature_clone.rotation_euler[0] = radians(90)
    bpy.ops.object.transform_apply(rotation=True)
    armature_clone.scale = Vector((100,100,100))
    bpy.ops.object.transform_apply(scale = True)
    armature_clone.name='skeleton'


    emptyLodGroup = bpy.data.objects.new( "fbodyLodGroup", None )
    emptyLodGroup["fbx_type"] = "LodGroup"
    emptyLodGroup["lookupVertexIdTable"] = "some/path/on/computer"
    bpy.context.scene.objects.link( emptyLodGroup )
    emptyLodGroup.select=True
    bpy.context.scene.objects.active = emptyLodGroup
    emptyLodGroup.scale = Vector((100,100,100))
    bpy.ops.object.transform_apply(scale = True)
    #fbody_hires.parent = emptyLodGroup
    #fbody.parent = emptyLodGroup

    #add the armature modifier
    deselect_all_objects()
    fbody_hires.select=True
    bpy.context.scene.objects.active = fbody_hires
    fbody_hires.rotation_euler[0] = radians(90)
    bpy.ops.object.transform_apply(rotation=True)    
    fbody_hires.scale = Vector((100,100,100))
    bpy.ops.object.transform_apply(scale = True)    
    # Add the armature modifier
    bpy.ops.object.modifier_add(type='ARMATURE')
    armature_modifier = fbody_hires.modifiers[-1]
    # Set the armature object for the modifier
    armature_modifier.object = armature_clone
    
    #add the armature modifier
    deselect_all_objects()
    fbody.select=True
    bpy.context.scene.objects.active = fbody
    fbody.rotation_euler[0] = radians(90)
    bpy.ops.object.transform_apply(rotation=True)   
    fbody.scale = Vector((100,100,100))
    bpy.ops.object.transform_apply(scale = True)      
    # Add the armature modifier
    bpy.ops.object.modifier_add(type='ARMATURE')
    armature_modifier = fbody.modifiers[-1]
    # Set the armature object for the modifier
    armature_modifier.object = armature_clone

    #rename them
    fbody.name = "fbody_LOD1"
    fbody_hires.name = "fbody_LOD0"
    #the order in which we set the parent is important it seems, otherwise in Unreal it will appear in the wrong order
    fbody_hires.parent = emptyLodGroup
    bpy.context.scene.update()	
    fbody.parent = emptyLodGroup
    bpy.context.scene.update()	
	

    emptyLodGroup.parent = armature_clone

    fix_translation_orientation_scale_for_unreal(armature_clone)


    bpy.context.scene.unit_settings.system = 'METRIC'
    #bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'  # You can also set 'CENTIMETERS'
    bpy.context.scene.unit_settings.scale_length = 0.01

    #fbx export:
    emptyLodGroup.select=True
    fbody_hires.select=True
    fbody.select=True
    armature_clone.select=True
    bpy.context.scene.objects.active = armature_clone
    export_params = {
    "filepath": os.path.join(exportfolderpath,exportFilename),#"SK_Belle.fbx"
    "check_existing": False,
    "filter_glob": "*.fbx",
    "version": 'BIN7400',
    "ui_tab": 'MAIN',
    "use_selection": True,
    "global_scale": 1.0,
    "apply_unit_scale": True,
    "apply_scale_options": 'FBX_SCALE_NONE',
    "bake_space_transform": False,
    "object_types": {'ARMATURE', 'EMPTY', 'MESH' }, #'OTHER'
    "use_mesh_modifiers": False,
    "use_mesh_modifiers_render": False,
    "mesh_smooth_type": 'FACE',
    "use_mesh_edges": False,
    "use_tspace": True,
    "use_custom_props": True,
    "add_leaf_bones": False,
    "primary_bone_axis": 'Y',
    "secondary_bone_axis": 'X',
    "use_armature_deform_only": True,
    "armature_nodetype": 'NULL', # ???????
    "bake_anim": False,
    "bake_anim_use_all_bones": False,
    "bake_anim_use_nla_strips": False,
    "bake_anim_use_all_actions": False,
    "bake_anim_force_startend_keying": False,
    "bake_anim_step": 1.0,
    "bake_anim_simplify_factor": 1.0,
    "use_anim": False,
    "use_anim_action_all": False,
    "use_default_take": False,
    "use_anim_optimize": False,
    "anim_optimize_precision": 6.0,
    "path_mode": 'COPY',
    "embed_textures": True,
    "batch_mode": 'OFF',
    "use_batch_own_dir": True,
    "use_metadata": True,
    }

    bpy.ops.export_scene.fbx(**export_params)

    bpy.context.scene.unit_settings.system = 'NONE'
    bpy.context.scene.unit_settings.scale_length = 1.0 
    #
    #if includeGeograftsOnExport:
    #    bpy.ops.object.delete()
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


    ctypes.windll.user32.FlashWindow(ctypes.windll.user32.GetActiveWindow(), True )



def fix_translation_orientation_scale_for_unreal(armature_object):
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    if (armature_object.rotation_euler.x!=0 or armature_object.rotation_euler.y!=0 or armature_object.rotation_euler.z!=0):
        print("Armature has a rotation applied, fix that first")
        ShowMessageBox("Armature has a rotation applied, fix that first", "Error", 'ERROR')
        return None
    
    mirror_x_flag = armature_object.data.use_mirror_x
    armature_object.data.use_mirror_x = False

    

    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    
    bpy.ops.object.transform_apply(location = True)

    armature_object.rotation_euler.z= radians(0)#90
    bpy.ops.object.transform_apply(rotation = True)
    #

    #armature_object.scale = Vector((100,100,100))
    #bpy.ops.object.transform_apply(scale = True)


    """
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ebones = armature_object.data.edit_bones
    ebones["root"].head  = Vector((0,0,0))
    tail = ebones["root"].tail.copy()
    ebones["root"].tail = Vector((0,0,tail.z))
    """
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)