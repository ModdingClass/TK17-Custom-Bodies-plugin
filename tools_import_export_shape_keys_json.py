import bpy
import json
from mathutils import Vector
from .tools_message_box import *


def prnDict(aDict, br='\n', html=0, keyAlign='l',   sortKey=0,  keyPrefix='',   keySuffix='',  valuePrefix='', valueSuffix='', leftMargin=0,   indent=1 ):
	#from: https://code.activestate.com/recipes/327142-print-a-dictionary-in-a-structural-way/
	#sortKey require: odict() # an ordered dict, if you want the keys sorted.
    #     Dave Benjamin 
    #     http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/161403
    if aDict:
        #------------------------------ sort key
        if sortKey:
            dic = aDict.copy()
            keys = dic.keys()
            keys.sort()
            aDict = odict()
            for k in keys:
                aDict[k] = dic[k]
        #------------------- wrap keys with ' ' (quotes) if str
        tmp = ['{']
        ks = [type(x)==str and "'%s'"%x or x for x in aDict.keys()]
        #------------------- wrap values with ' ' (quotes) if str
        vs = [type(x)==str and "'%s'"%x or x for x in aDict.values()] 
        maxKeyLen = max([len(str(x)) for x in ks])
        for i in range(len(ks)):
            #-------------------------- Adjust key width
            k = {1            : str(ks[i]).ljust(maxKeyLen),
                 keyAlign=='r': str(ks[i]).rjust(maxKeyLen) }[1]
            v = vs[i]        
            tmp.append(' '* indent+ '%s%s%s:%s%s%s,' %(keyPrefix, k, keySuffix, valuePrefix,v,valueSuffix))
        tmp[-1] = tmp[-1][:-1] # remove the ',' in the last item
        tmp.append('}')
        if leftMargin:
          tmp = [ ' '*leftMargin + x for x in tmp ]
        if html:
            return '<code>%s</code>' %br.join(tmp).replace(' ','&nbsp;')
        else:
            return br.join(tmp)     
    else:
        return '{}'



def exportShapeKeysToJsonFile(ob, filename):
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
            if ( delta.x < epsilon and delta.y < epsilon and delta.z < epsilon ):
                delta = Vector((0,0,0))
            data.append( [delta.x,delta.y,delta.z] )
        skKeysExport[keyName] = data

    with open(filename, 'w') as outfile:
        outfile.write(prnDict(skKeysExport).replace("'", "\""))



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
            key.data[i].co = basis_verts.data[i].co + Vector( tuple(e for e in arr[i])  )


def add_empty_shapekeys_for_vx_body():
    bpy.ops.object.mode_set(mode='OBJECT')
    ob = bpy.context.active_object

    #add fake shapekeys

    verts = ob.data.vertices

    #check to see if we have the Basis Shapekey, otherwise create it
    if ( ob.data.shape_keys == None or len(ob.data.shape_keys.key_blocks)==0 ):
        sk_basis = ob.shape_key_add(name='Basis',from_mix=False)
        sk_basis.interpolation = 'KEY_LINEAR'
        # must set relative to false here
        ob.data.shape_keys.use_relative = False
    #
    #
    shape_keys_dict = [
    'bbb_asian02_morph',
    'bbb_vagfix_morph',
    'bbb_eye_L_morph',
    'bbb_asian01_morph',
    'bbb_atomic01',
    'bbb_hentai01_morph',
    'bbb_eye_R_morph',
    'bbb_african01_morph',
    'bbb_vag_morph',
    'bbb_jenna01_morph',
    'bbb_capelli01_morph',
    'bbb_ear01',
    'bbb_pregnant',
    'bbb_ear02'
    ]

    # Create 10 sequential deformations
    for key in shape_keys_dict: 
        if 	key not in ob.data.shape_keys.key_blocks:
            # Create new shape key
            sk = ob.shape_key_add(key)
            sk.slider_min = -1
            sk.interpolation = 'KEY_LINEAR'
            ob.data.shape_keys.use_relative = True

