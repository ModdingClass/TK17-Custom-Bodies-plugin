import bpy
import json

from .utilz import *


def exportMaterialsToJsonFile(ob, filename):
    ob = bpy.context.object
    assert ob is not None and ob.type == 'MESH', "active object invalid"
    # ensure we got the latest assignments and materials?!? (do we realy need that?!?)
    ob.update_from_editmode()
    #
    mats = ob.material_slots
    materialsExport = {mat.name:[ ] for mat in mats}
    #materialsExport = ob.material_slots.keys()   <-TypeError: list indices must be integers or slices, not str
    for f in ob.data.polygons:
        materialsExport[ob.material_slots[:][f.material_index].name].append(f.index)
    with open(filename, 'w') as outfile:
        outfile.write(prnDict(materialsExport).replace("'", "\""))


def importMaterialsFromJsonFile(ob, filename):
    def checkIfMaterialExistElseCreateIt(ob, material):
        mat = bpy.data.materials.get(material)
        #if it doesnt exist, create it.
        if mat is None:
            # create material
            mat = bpy.data.materials.new(name=material)
            #assign material
        if mat.name not in ob.material_slots.keys():
            ob.data.materials.append(mat)     
        return mat

    #
    ob = bpy.context.object
    assert ob is not None and ob.type == 'MESH', "active object invalid"
    # ensure we got the latest assignments and weights
    ob.update_from_editmode()
    #
    f = open(filename,)
    # returns JSON object as a dictionary
    data = json.load(f)
    f.close()     # Closing file
    #
    #
    for matName,faceIndices in data.items():
        material = checkIfMaterialExistElseCreateIt(ob, matName)
        material_index = bpy.context.object.material_slots.find(material.name)
        for i in faceIndices:
            ob.data.polygons[i].material_index = material_index
    #

def sort_materials_in_object(ob):
    # Check if object has materials
    if not ob or not ob.material_slots:
        return False
    
    ob_mats = [mat.name for mat in ob.material_slots]
    ob_mats.sort()

    for i, mat_name in enumerate(ob_mats):
        # Set active material slot to the last slot
        ob.active_material_index = len(ob.material_slots) - 1
        # Find the material with the matching name
        while ob.active_material.name != mat_name:
            ob.active_material_index -= 1
        # Move the material slot to the correct position
        while ob.active_material_index > i:
            bpy.ops.object.material_slot_move(direction='UP')
    
    return True

