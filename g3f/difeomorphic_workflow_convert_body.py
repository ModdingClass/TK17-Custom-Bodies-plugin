import bpy
from ..utils_bpy import *

def checkIfActiveObjectIs(typeOfObject, name): #'ARMATURE', "MESH"
    activeObject = bpy.context.scene.objects.active
    if (activeObject.type == typeOfObject and name in activeObject.name):
        return True
    else:
        return False


    
#meshes = [ob for ob in bpy.data.objects if ob.type == 'MESH']

def checkIfActiveObjectHasChild(typeOfObject,name): #'ARMATURE', "MESH"
    #init
    foundIt = None
    activeObject = bpy.context.scene.objects.active
    children = []
    getChildrenRecursive(activeObject, children, 0, levels = 10)
    for c in children: 
        if (c.type == typeOfObject and name in c.name):
            foundIt = c
            break
    #
    return foundIt    

def notYetWorking():
    bpy.context.scene.objects.active = armature_object
    bpy.ops.object.duplicate(linked=False)
    clone = bpy.context.scene.objects.active
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #
    bpy.ops.object.delete() 
    bpy.ops.object.select_all(action='DESELECT')
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    armature_object.select = True


