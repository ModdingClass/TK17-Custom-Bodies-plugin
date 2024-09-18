import bpy
import json
import math
from collections import OrderedDict
from pathlib import Path

from .utilz import *

# Utility function to export armature data
def export_armature_data(context, filepath):
    armature = context.object

    if armature and armature.type == 'ARMATURE':
        if has_non_default_transforms(armature):
            show_warning("Warning: The armature has non-default transforms (location, rotation, or scale). The exported armature might not match the original armature's appearance exactly.")
        
        original_mode = context.mode

        # Switch to Edit Mode if necessary
        if context.mode != 'EDIT_ARMATURE':
            bpy.ops.object.mode_set(mode='EDIT')

        bones_data = []
        for bone in armature.data.edit_bones:
            bone_info = OrderedDict([
                ("name", bone.name),
                ("head", ["{:.6f}".format(bone.head.x), "{:.6f}".format(bone.head.y), "{:.6f}".format(bone.head.z)]),
                ("tail", ["{:.6f}".format(bone.tail.x), "{:.6f}".format(bone.tail.y), "{:.6f}".format(bone.tail.z)]),
                ("roll", "{:.6f}".format(math.degrees(bone.roll))),
                ("parent", bone.parent.name if bone.parent else None),
                ("connected", bone.use_connect),
                ("deform", bone.use_deform)
            ])
            bones_data.append(bone_info)

        json_data = json.dumps(bones_data, indent=4)
        json_data = json_data.replace('\n        [', ' [').replace('\n            ', ' ').replace('\n        ]', ' ]')

        # Write the JSON data to the specified file
        try:
            with open(filepath, 'w') as outfile:
                outfile.write(json_data)
        except IOError:
            print("Failed to write to file.")
            return {'CANCELLED'}

        # Restore the original mode
        bpy.ops.object.mode_set(mode=original_mode)

        print("Armature data has been exported")
        return {'FINISHED'}
    else:
        print("No armature selected")
        return {'CANCELLED'}

def create_and_import_armature_data(context, filepath):
    deselect_all_objects()
    armatureName = Path(filepath).stem
    bpy.ops.object.armature_add()
    armature = bpy.context.scene.objects.active
    armature.name = armatureName
    #armature = bpy.data.armatures.new(armatureName)
    #armature_object = bpy.data.objects.new(armatureName, armature)
    #bpy.context.scene.objects.link(armature_object)
    #armature_object = bpy.context.scene.objects.active
    #armature_object.select = True
    return import_armature_data(context, filepath)

# Utility function to import armature data
def import_armature_data(context, filepath):
    armature = context.object
    # Load the JSON data
    bones_data = load_json(filepath)
    # Switch to Edit Mode to create bones
    bpy.context.scene.objects.active = armature
    bpy.ops.object.mode_set(mode='EDIT')
    armature_data = armature.data
    #remove existing bones
    for bone in armature_data.edit_bones:
        armature_data.edit_bones.remove(bone)
    # Dictionary to hold the created bones for easy parent reference
    created_bones = {}
    # Create bones from the JSON data
    for bone_info in bones_data:
        # Ensure all values are floats
        head = [float(bone_info["head"][0]), float(bone_info["head"][1]), float(bone_info["head"][2])]
        tail = [float(bone_info["tail"][0]), float(bone_info["tail"][1]), float(bone_info["tail"][2])]
        roll = float(bone_info["roll"])
        # Add the bone
        bone = armature_data.edit_bones.new(bone_info["name"])
        bone.head = (head[0], head[1], head[2])
        bone.tail = (tail[0], tail[1], tail[2])
        bone.roll = math.radians(roll)
        bone.use_connect = bone_info["connected"]
        bone.use_deform = bone_info["deform"]
        # Store the created bone
        created_bones[bone_info["name"]] = bone
    #
    # Set parent bones after all bones have been created
    for bone_info in bones_data:
        if bone_info["parent"]:
            parent_bone = created_bones.get(bone_info["parent"])
            if parent_bone:
                created_bones[bone_info["name"]].parent = parent_bone
    
    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("Armature has been imported from", filepath)
    return {'FINISHED'}
