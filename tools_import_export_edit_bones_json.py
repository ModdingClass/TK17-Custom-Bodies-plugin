import bpy
import json
import math
from collections import OrderedDict

from .tools_message_box import *

from mathutils import Vector
from mathutils import Matrix
from math import radians

        
class MyCustomEditBone:
    def __init__(self, name, parent, head, tail , roll, isDeform):
        self.__dict__ = OrderedDict()
        self.__dict__['name'] = name
        self.__dict__['parent'] = parent
        self.__dict__['head'] = [head.x, head.y, head.z]
        self.__dict__['tail'] = [tail.x, tail.y, tail.z]  
        self.__dict__['roll'] = math.degrees(roll)
        self.__dict__['isDeform'] = isDeform
        # self.name = name
        # self.parent = parent
        # self.head = [head.x, head.y, head.z]
        # self.tail = [tail.x, tail.y, tail.z]
        # self.roll = roll
        # self.isDeform = isDeform


def exportEditBonesToJsonFile(ob, filename):
    ob = bpy.context.object
    assert ob is not None and ob.type == 'ARMATURE', "active object invalid - not an armature"
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    my_bones = []
    exportableArray = [] 
    def print_heir(ob, levels=50):
        def recurse(ob, parent, depth):
            if depth > levels: 
                return
            #print("  " * depth, ob.name)
            my_bones.append(ob)
            for child in ob.children:
                recurse(child, ob,  depth + 1)
        recurse(ob, ob.parent, 0)
    #
    parentBone = ob.data.edit_bones["root"]
    print_heir(parentBone)
    #
    for bone in my_bones:
        parentName = None if bone.parent is None else bone.parent.name
        myCustomBone = MyCustomEditBone(bone.name, parentName , bone.head, bone.tail, bone.roll, bone.use_deform)
        exportableArray.append( myCustomBone)
    #convert to JSON string
    jsonStr = ""
    #convert to JSON string
    for item in exportableArray:
        jsonStr = jsonStr + json.dumps(item.__dict__) +",\n"
        #    
        #print json string
        #print(jsonStr)
    jsonStr = "[\n" + jsonStr[:-2] + "]"
    with open(filename, 'w') as outfile:
        outfile.write( jsonStr )
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def importEditBonesFromJsonFile(ob, filename):
    f = open(filename,)
    # returns JSON object as a dictionary
    data = json.load(f)
    f.close()     # Closing file
    if len( data ) == 0 :
        #print ("no data")
        ShowMessageBox("No data in input json file!", "Error", 'ERROR')
        return
    #

    ob = bpy.context.object
    assert ob is not None and ob.type == 'ARMATURE', "active object invalid - not an armature"
    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    #check to see if json file has same number of vertices
    for item in data:
        bone = ob.data.edit_bones[item["name"]]
        bone.parent = None if item["parent"] is None else ob.data.edit_bones[item["parent"]]
        bone.head = Vector (( item["head"][0],item["head"][1],item["head"][2] ))
        bone.tail = Vector (( item["tail"][0],item["tail"][1],item["tail"][2] ))
        bone.use_deform = item["isDeform"]
        bone.roll = math.radians(item["roll"])


