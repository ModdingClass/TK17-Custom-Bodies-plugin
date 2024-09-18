import bpy
import json
import mathutils
from mathutils import Vector
from decimal import Decimal
import re

from .utilz import *

def exportShapeKeysToJsonFile(ob, filename):
    
    def round_floats(o):
        if isinstance(o, float): return "~{:.8f}~".format(o)
        if isinstance(o, dict): return {k: round_floats(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)): return [round_floats(x) for x in o]
        return o    
    #
    ob = bpy.context.object
    assert ob is not None and ob.type == 'MESH', "active object invalid"
    # ensure we got the latest assignments and weights
    ob.update_from_editmode()
    #
    me = ob.data
    basis_verts = ob.data.shape_keys.key_blocks[0]

    json_sk_exporter = "" #in properties it could be defined as  bbb_eye_L_morph,bbb_eye_R_morph,bbb_vagfix_morph

    if ob.data.get("json_sk_exporter") is not None:
        json_sk_exporter = ob.data.get("json_sk_exporter")

    skKeys = []
    for key in ob.data.shape_keys.key_blocks[1:]:
        SKName = key.name
        if json_sk_exporter == "":
            skKeys.append(SKName)
        else:    
            if SKName in json_sk_exporter:
                skKeys.append(SKName)

    skKeysExport = {keyName:[ ] for keyName in skKeys}

    epsilon = 0.000001
    for keyName in skKeys:
        key = ob.data.shape_keys.key_blocks[keyName]
        data = []
        for i in range(len(me.vertices)):
            delta = (key.data[i].co - basis_verts.data[i].co)
            if ( abs(delta.x) < epsilon and abs(delta.y) < epsilon and abs(delta.z) < epsilon ):
                delta = Vector((0,0,0))
            data.append( [ delta.x,  delta.y,  delta.z ] )
        skKeysExport[keyName] = data

   
    
    outStr= json.dumps(round_floats(skKeysExport))
    outStr = outStr.replace("{", "{\n\t").replace("}","\n}" )               #split arrays on rows 
    outStr = outStr.replace("]], ","] ],\n\t").replace("[[","[ [")          #add a space between main brackets
    outStr = outStr.replace("\"~","").replace("~\"","")                     # convert from strings with prefix/suffix back to readable floats
    outStr = outStr.replace("-0.00000000","0").replace("0.00000000","0")        #replace long zeros
    with open(filename, 'w') as outfile:
        outfile.write( outStr )
    
    #with open(filename, 'w') as outfile:
    #    outfile.write(prnDict(skKeysExport).replace("'", "\""))        



def importShapeKeysFromJsonFile(ob, filename):
    def checkIfShapekeyExistAndRecreateIt(ob, shapekey):
        if shapekey in [key.name for key in ob.data.shape_keys.key_blocks[1:]]:
            # setting the active shapekey
            iIndex = ob.data.shape_keys.key_blocks.keys().index(shapekey)
            ob.active_shape_key_index = iIndex
            # delete it
            bpy.ops.object.shape_key_remove()
        ob.shape_key_add(shapekey)
        iIndex = ob.data.shape_keys.key_blocks.keys().index(shapekey)
        ob.active_shape_key_index = iIndex
        ob.data.shape_keys.use_relative = True          
    #
    ob = bpy.context.object
    assert ob is not None and ob.type == 'MESH', "active object invalid"
    # ensure we got the latest assignments and weights
    ob.update_from_editmode()
    me = ob.data
    #
    f = open(filename,)
    # returns JSON object as a dictionary
    data = json.load(f)
    f.close()     # Closing file
    if len( data.items() ) == 0 :
        ShowMessageBox("No data in input json file!", "Error", 'ERROR')
        return
    #
    #check to see if json file has same number of vertices
    for skName,arr in data.items():
        if len(arr) == len(me.vertices):
            #all good, we can continue
            break
        else:
            ShowMessageBox("Vertex count not matching!", "Error", 'ERROR')
            return 
    #
    #check to see if we have the Basis Shapekey, otherwise create it
    if ( ob.data.shape_keys == None or len(ob.data.shape_keys.key_blocks)==0 ):
        sk_basis = ob.shape_key_add(name='Basis',from_mix=False)
        sk_basis.interpolation = 'KEY_LINEAR'
        # must set relative to false here
        ob.data.shape_keys.use_relative = False
    #
    basis_verts = ob.data.shape_keys.key_blocks[0]
    #
    for skName,arr in data.items():
        checkIfShapekeyExistAndRecreateIt(ob,skName)
        key = ob.data.shape_keys.key_blocks[skName]
        for i in range(len(me.vertices)):
            #here we should check if arr is already (0,0,0)
            key.data[i].co = basis_verts.data[i].co + Vector( tuple(e for e in arr[i])  )




def split_shape_key_by_axis(obj, shape_key_index):
    """
    Splits the selected shape key into three separate keys affecting only X, Y, and Z axes.
    """
    if obj.type != 'MESH':
        return
    
    mesh = obj.data
    shape_keys = mesh.shape_keys
    key_blocks = shape_keys.key_blocks
    
    if not shape_keys or shape_key_index < 0 or shape_key_index >= len(key_blocks):
        return
    
    base_key = key_blocks[0]
    selected_key = key_blocks[shape_key_index]
    
    # Create new shape keys for each axis
    key_x = obj.shape_key_add(name="{}_X".format(selected_key.name), from_mix=False)
    key_y = obj.shape_key_add(name="{}_Y".format(selected_key.name), from_mix=False)
    key_z = obj.shape_key_add(name="{}_Z".format(selected_key.name), from_mix=False)
    
    # Set the new shape keys to affect only their respective axis
    for v_index in range(len(base_key.data)):
        base_coord = base_key.data[v_index].co
        selected_coord = selected_key.data[v_index].co
        delta = selected_coord - base_coord
        
        # Explicitly create vectors with only one axis set
        delta_x = mathutils.Vector((delta.x, 0, 0))
        delta_y = mathutils.Vector((0, delta.y, 0))
        delta_z = mathutils.Vector((0, 0, delta.z))
        
        key_x.data[v_index].co = base_coord + delta_x
        key_y.data[v_index].co = base_coord + delta_y
        key_z.data[v_index].co = base_coord + delta_z


