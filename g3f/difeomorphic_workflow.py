import bpy
import mathutils
import math
from math import radians
import json
from mathutils import Vector

from ..tools_message_box import *

from ..ik_tools import *

from ..g3f.difeomorphic_workflow_dictionaries_bones import *
from ..g3f.difeomorphic_workflow_dictionaries_vertex_groups import *
from ..g3f.difeomorphic_workflow_init_custom_vertex_indices import *

from ..g3f.difeomorphic_workflow_armature_utils import *

from ..g3f.difeomorphic_workflow_armature_from_gens_vertices import *
from ..g3f.difeomorphic_workflow_armature_from_other_vertices import *
from ..g3f.difeomorphic_workflow_armature_from_head_vertices import *
from ..g3f.difeomorphic_workflow_armature_from_breast_vertices import *

#if "bpy" in locals():
#    import imp
#    imp.reload(....g3f.difeomorphic_workflow_dictionaries_bones)
#else:
#    from ..g3f import difeomorphic_workflow_dictionaries_bones


def alignArmatureToDifeomorphic():
    bones_dict = {}
    activeObject = bpy.context.scene.objects.active
    if (activeObject.type == 'ARMATURE'):
        pass
    else:
        print ("Difeomorphic Armature must be selected")
        ShowMessageBox("Difeomorphic Armature must be selected", "Warning", 'INFO')
        return {'FINISHED'}
    if ("Genesis 3 Female" in activeObject.name):
            children = getChildren(activeObject) 
            extractSpecificBonesFromG3FArmatureFastVersion(activeObject.name, bones_dict)
            #setupSpecificBonesFromG3FArmature(activeObject.name, "Armature")
            for c in children: 
                #print (c.name)
                if ("Genesis 3 Female Mesh" in c.name):
                    print("bla")
                    getArmatureBonesDictFromBreastVertices(bones_dict)
                    getArmatureBonesDictFromOtherVertices(bones_dict)
                    getArmatureBonesDictFromHeadVertices(bones_dict)
                    getArmatureBonesDictFromGensVertices(bones_dict)
                    #setupSpecificBonesRollFromG3FBodyMesh()
                #if ("Genesis 3 Female Genitalia" in c.name):
                #    setupBonesFromGenitalGeoGraftMesh()
                print (bones_dict)
    #
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects["Armature"].select = True
    bpy.context.scene.objects.active = bpy.data.objects["Armature"]
    bpy.ops.object.editmode_toggle()

    armature_data = bpy.data.objects['Armature']
    # amw is armature matrix world, amwi is the inverse
    amw = armature_data.matrix_world
    amwi = amw.inverted()
    ebones = armature_data.data.edit_bones
    for key,value in bones_dict.items():
        print(key)
        print(value)
        ebones[key].head = amwi * value['head']
        ebones[key].tail = amwi * value['tail']
        ebones[key].roll = radians(value['roll']+value['rollOffset'])
    #
    bpy.ops.object.mode_set(mode='OBJECT')



def fixBreastJointEndsDifeomorphic(target_armature):
    print ("fixBreastJointEndsDifeomorphic")
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[target_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[target_armature]
    ob = bpy.data.objects[target_armature]
    bpy.ops.object.editmode_toggle()
    armature_data = bpy.data.objects[target_armature]
    ebones = armature_data.data.edit_bones
    breast_scale_joint_R = ebones["breast_scale_joint.R"]
    nipple_joint01_R = ebones["nipple_joint01.R"]
    nipple_jointEnd_R = ebones["nipple_jointEnd.R"]
    matrix = breast_scale_joint_R.matrix.copy()
    nipple_joint01_R_head = nipple_joint01_R.head.copy()
    nipple_joint01_R_tail = nipple_joint01_R.tail.copy()
    nipple_jointEnd_R_head = nipple_jointEnd_R.head.copy()
    nipple_jointEnd_R_tail = nipple_jointEnd_R.tail.copy()
    #
    nipple_joint01_R.matrix = matrix
    nipple_joint01_R.head = nipple_joint01_R_head
    nipple_joint01_R.tail = nipple_joint01_R_tail
    nipple_jointEnd_R.matrix = nipple_joint01_R.matrix.copy()
    nipple_jointEnd_R.head = nipple_joint01_R.tail
    nipple_jointEnd_R.tail = nipple_joint01_R.head
    nipple_jointEnd_R.length *= -1
    #
    breast_deform02_joint01_R = ebones["breast_deform02_joint01.R"]
    breast_deform02_jointEnd_R = ebones["breast_deform02_jointEnd.R"]
    matrix = breast_deform02_joint01_R.matrix.copy()
    breast_deform02_jointEnd_R_head = breast_deform02_joint01_R.tail.copy()
    breast_deform02_jointEnd_R_tail = breast_deform02_jointEnd_R.tail.copy()
    length = breast_deform02_joint01_R.length
    breast_deform02_joint01_R.length *= 1.05 
    breast_deform02_jointEnd_R.matrix = matrix
    breast_deform02_jointEnd_R.head = breast_deform02_jointEnd_R_head
    breast_deform02_jointEnd_R.tail = breast_deform02_joint01_R.tail.copy()
    breast_deform02_joint01_R.length = length
    #
    breast_deform03_joint01_R = ebones["breast_deform03_joint01.R"]
    breast_deform03_jointEnd_R = ebones["breast_deform03_jointEnd.R"]
    matrix = breast_deform03_joint01_R.matrix.copy()
    breast_deform03_jointEnd_R_head = breast_deform03_joint01_R.tail.copy()
    breast_deform03_jointEnd_R_tail = breast_deform03_jointEnd_R.tail.copy()
    length = breast_deform03_joint01_R.length
    breast_deform03_joint01_R.length *= 1.05 
    breast_deform03_jointEnd_R.matrix = matrix
    breast_deform03_jointEnd_R.head = breast_deform03_jointEnd_R_head
    breast_deform03_jointEnd_R.tail = breast_deform03_joint01_R.tail.copy()
    breast_deform03_joint01_R.length = length
    #
    breast_deform03_joint01_R = ebones["breast_deform03_joint01.R"]
    breast_deform03_jointEnd_R = ebones["breast_deform03_jointEnd.R"]
    matrix = breast_deform03_joint01_R.matrix.copy()
    breast_deform03_jointEnd_R_head = breast_deform03_joint01_R.tail.copy()
    breast_deform03_jointEnd_R_tail = breast_deform03_jointEnd_R.tail.copy()
    length = breast_deform03_joint01_R.length
    breast_deform03_joint01_R.length *= 1.05 
    breast_deform03_jointEnd_R.matrix = matrix
    breast_deform03_jointEnd_R.head = breast_deform03_jointEnd_R_head
    breast_deform03_jointEnd_R.tail = breast_deform03_joint01_R.tail.copy()
    breast_deform03_joint01_R.length = length
    #
    breast_deform01_joint01_R = ebones["breast_deform01_joint01.R"]
    breast_deform01_jointEnd_R = ebones["breast_deform01_jointEnd.R"]
    matrix = breast_deform01_joint01_R.matrix.copy()
    breast_deform01_jointEnd_R_head = breast_deform01_joint01_R.tail.copy()
    breast_deform01_jointEnd_R_tail = breast_deform01_jointEnd_R.tail.copy()
    length = breast_deform01_joint01_R.length
    breast_deform01_joint01_R.length *= 1.05 
    breast_deform01_jointEnd_R.matrix = matrix
    breast_deform01_jointEnd_R.head = breast_deform01_jointEnd_R_head
    breast_deform01_jointEnd_R.tail = breast_deform01_joint01_R.tail.copy()
    breast_deform01_joint01_R.length = length
    breast_scale_joint_L = ebones["breast_scale_joint.L"]
    nipple_joint01_L = ebones["nipple_joint01.L"]
    nipple_jointEnd_L = ebones["nipple_jointEnd.L"]
    matrix = breast_scale_joint_L.matrix.copy()
    nipple_joint01_L_head = nipple_joint01_L.head.copy()
    nipple_joint01_L_tail = nipple_joint01_L.tail.copy()
    nipple_jointEnd_L_head = nipple_jointEnd_L.head.copy()
    nipple_jointEnd_L_tail = nipple_jointEnd_L.tail.copy()
    nipple_joint01_L.matrix = matrix
    nipple_joint01_L.head = nipple_joint01_L_head
    nipple_joint01_L.tail = nipple_joint01_L_tail
    nipple_jointEnd_L.matrix = nipple_joint01_L.matrix.copy()
    nipple_jointEnd_L.head = nipple_joint01_L.tail
    nipple_jointEnd_L.tail = nipple_joint01_L.head
    nipple_jointEnd_L.length *= -1
    #
    breast_deform02_joint01_L = ebones["breast_deform02_joint01.L"]
    breast_deform02_jointEnd_L = ebones["breast_deform02_jointEnd.L"]
    matrix = breast_deform02_joint01_L.matrix.copy()
    breast_deform02_jointEnd_L_head = breast_deform02_joint01_L.tail.copy()
    breast_deform02_jointEnd_L_tail = breast_deform02_jointEnd_L.tail.copy()
    length = breast_deform02_joint01_L.length
    breast_deform02_joint01_L.length *= 1.05 
    breast_deform02_jointEnd_L.matrix = matrix
    breast_deform02_jointEnd_L.head = breast_deform02_jointEnd_L_head
    breast_deform02_jointEnd_L.tail = breast_deform02_joint01_L.tail.copy()
    breast_deform02_joint01_L.length = length
    #
    breast_deform03_joint01_L = ebones["breast_deform03_joint01.L"]
    breast_deform03_jointEnd_L = ebones["breast_deform03_jointEnd.L"]
    matrix = breast_deform03_joint01_L.matrix.copy()
    breast_deform03_jointEnd_L_head = breast_deform03_joint01_L.tail.copy()
    breast_deform03_jointEnd_L_tail = breast_deform03_jointEnd_L.tail.copy()
    length = breast_deform03_joint01_L.length
    breast_deform03_joint01_L.length *= 1.05 
    breast_deform03_jointEnd_L.matrix = matrix
    breast_deform03_jointEnd_L.head = breast_deform03_jointEnd_L_head
    breast_deform03_jointEnd_L.tail = breast_deform03_joint01_L.tail.copy()
    breast_deform03_joint01_L.length = length
    #
    breast_deform03_joint01_L = ebones["breast_deform03_joint01.L"]
    breast_deform03_jointEnd_L = ebones["breast_deform03_jointEnd.L"]
    matrix = breast_deform03_joint01_L.matrix.copy()
    breast_deform03_jointEnd_L_head = breast_deform03_joint01_L.tail.copy()
    breast_deform03_jointEnd_L_tail = breast_deform03_jointEnd_L.tail.copy()
    length = breast_deform03_joint01_L.length
    breast_deform03_joint01_L.length *= 1.05 
    breast_deform03_jointEnd_L.matrix = matrix
    breast_deform03_jointEnd_L.head = breast_deform03_jointEnd_L_head
    breast_deform03_jointEnd_L.tail = breast_deform03_joint01_L.tail.copy()
    breast_deform03_joint01_L.length = length
    #
    breast_deform01_joint01_L = ebones["breast_deform01_joint01.L"]
    breast_deform01_jointEnd_L = ebones["breast_deform01_jointEnd.L"]
    matrix = breast_deform01_joint01_L.matrix.copy()
    breast_deform01_jointEnd_L_head = breast_deform01_joint01_L.tail.copy()
    breast_deform01_jointEnd_L_tail = breast_deform01_jointEnd_L.tail.copy()
    length = breast_deform01_joint01_L.length
    breast_deform01_joint01_L.length *= 1.05 
    breast_deform01_jointEnd_L.matrix = matrix
    breast_deform01_jointEnd_L.head = breast_deform01_jointEnd_L_head
    breast_deform01_jointEnd_L.tail = breast_deform01_joint01_L.tail.copy()
    breast_deform01_joint01_L.length = length


def fixHeadJointsDifeomorphic(target_armature):
    print ("fixHeadJointsDifeomorphic")
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[target_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[target_armature]
    ob = bpy.data.objects[target_armature]
    bpy.ops.object.editmode_toggle()
    armature_data = bpy.data.objects[target_armature]
    ebones = armature_data.data.edit_bones
    #
    ebones["head_joint02"].tail.y = ebones["head_joint02"].head.y
    ebones["head_joint01"].tail.y = ebones["head_joint02"].head.y
    ebones["head_joint01"].head.y = ebones["head_joint02"].head.y
    ebones["head_joint01"].head.z = ebones["head_joint02"].head.z


def fixSpineJointsDifeomorphic(target_armature):
    print ("fixSpineJointsDifeomorphic")
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[target_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[target_armature]
    ob = bpy.data.objects[target_armature]
    bpy.ops.object.editmode_toggle()
    armature_data = bpy.data.objects[target_armature]
    ebones = armature_data.data.edit_bones
    #
    ebones["spine_jointEnd"].tail = ebones["neck_joint01"].head
    boneArray = ["spine_joint01","spine_joint02","spine_joint03","spine_joint04","spine_jointEnd"]
    makeBonesCollinearFromBoneHeadToBoneTail("Armature", boneArray)


def fixFingersJointEndsDifeomorphic(target_armature):
    print ("fixFingersJointEndsDifeomorphic")
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[target_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[target_armature]
    ob = bpy.data.objects[target_armature]
    bpy.ops.object.editmode_toggle()
    armature_data = bpy.data.objects[target_armature]
    ebones = armature_data.data.edit_bones
    for index, row in enumerate(finger_jointend_bones_parents):
        ebones[row[0]].head = ebones[row[1]].tail
        ebones[row[0]].tail = ebones[row[0]].head + Vector ((0,0,0.005))
        print(row[0])


def fixToesJointEndsDifeomorphic(target_armature):
    print ("fixToesJointEndsDifeomorphic")
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[target_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[target_armature]
    ob = bpy.data.objects[target_armature]
    bpy.ops.object.editmode_toggle()
    armature_data = bpy.data.objects[target_armature]
    ebones = armature_data.data.edit_bones
    for index, row in enumerate(toe_jointend_bones_parents):
        ebones[row[0]].head = ebones[row[1]].tail
        ebones[row[0]].tail = ebones[row[0]].head + Vector ((0.01,0,0))
        print(row[0])



def extractSpecificBonesFromG3FArmatureFastVersion(difeomorphic_armature, bones_dict):
    print("extractSpecificBonesFromG3FArmatureFastVersion()...")
    #
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[difeomorphic_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[difeomorphic_armature]
    ob = bpy.data.objects[difeomorphic_armature]
    bpy.ops.object.editmode_toggle()
    #
    difeomorphic_armature_data = bpy.data.objects[difeomorphic_armature]
    #
    difeomorphic_ebones = difeomorphic_armature_data.data.edit_bones
    # amw is armature matrix world, amwi is the inverse
    difeomorphic_amw = difeomorphic_armature_data.matrix_world
    difeomorphic_amwi = difeomorphic_amw.inverted()
    #
    for index, row in enumerate(leg_bones_matching + hand_bones_matching + spine_bones_matching):
        if (row[0] == row[1]):
            eb = difeomorphic_ebones[row[0]]
            difeomorphic_eb_matrix_world = difeomorphic_amw * eb.matrix
            difeomorphic_eb_head_world = eb.head + difeomorphic_armature_data.location 
            difeomorphic_eb_tail_world =  eb.tail + difeomorphic_armature_data.location    
        else:
            # first head
            eb = difeomorphic_ebones[row[0]]
            difeomorphic_eb_head_world =  eb.head + difeomorphic_armature_data.location      
            # then tail
            eb = difeomorphic_ebones[row[1]]
            difeomorphic_eb_tail_world =  eb.tail + difeomorphic_armature_data.location             
        #
        bones_dict[row[2]]= {"head":difeomorphic_eb_head_world, "tail":difeomorphic_eb_tail_world, "roll":0, "rollOffset":0, "connected":False }
    #
    # lets get the roll if defined
    for index, row in enumerate(leg_bones_matching + hand_bones_matching + spine_bones_matching):
        eb = difeomorphic_ebones[row[0]]
        bones_dict[row[2]]['roll']= math.degrees(eb.roll)
        rollOffset  = row[3] if 3 < len(row) else 0          # check if it exists defined, otherwise is 0
        print("RollOffset for bone {0} is {1}".format(row[2],rollOffset))
        bones_dict[row[2]]['rollOffset']= rollOffset
    #    
    bpy.ops.object.mode_set(mode='OBJECT')
    return bones_dict

def extractSpecificBonesFromG3FBodyMesh(difeomorphic_body, bones_dict):
    print("setupSpecificBonesFromG3FGensGeograftMesh()...")
    #
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[difeomorphic_body].select = True
    bpy.context.scene.objects.active = bpy.data.objects[difeomorphic_body]
    ob = bpy.data.objects[difeomorphic_body]
    vagina_center = getCenterFromVertices (vagina_center, obj )

    #
    #bones_dict[]= {"head":difeomorphic_eb_head_world, "tail":difeomorphic_eb_tail_world, "roll":0, "rollOffset":0, "connected":False }
    return bones_dict

def extractSpecificBonesFromG3FGensGeograftMesh(difeomorphic_gens, bones_dict):
    print("setupSpecificBonesFromG3FGensGeograftMesh()...")
    #
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[difeomorphic_gens].select = True
    bpy.context.scene.objects.active = bpy.data.objects[difeomorphic_gens]
    ob = bpy.data.objects[difeomorphic_gens]
    bpy.ops.object.editmode_toggle()
    #
    #bones_dict[]= {"head":difeomorphic_eb_head_world, "tail":difeomorphic_eb_tail_world, "roll":0, "rollOffset":0, "connected":False }
    return bones_dict


def findGensMesh():
    meshes = [ob for ob in bpy.data.objects if (ob.type == 'MESH' and 'Genesis 3 Female Genitalia' in ob.name )]
    if len(meshes)>0:
        return meshes[0]
    return None


def setupSpecificBonesFromG3FArmature(difeomorphic_armature, vx_armature ):
    print("setupSpecificBonesFromG3FArmature()...")
    for index, row in enumerate(leg_bones_matching):
        align_bones(difeomorphic_armature,row[0],row[1], vx_armature, row[2])
        print(row[2])
    for index, row in enumerate(hand_bones_matching):
        align_bones(difeomorphic_armature, row[0],row[1], vx_armature, row[2])
        print(row[2])
    for index, row in enumerate(spine_bones_matching):
        align_bones(difeomorphic_armature, row[0],row[1], vx_armature, row[2])
        print(row[2])        

def setupSpecificBonesRollFromG3FBodyMesh():
    print("setupSpecificBonesRollFromG3FBodyMesh()...")

def setupBonesFromGenitalGeoGraftMesh():
    print("setupBonesFromGenitalGeoGraftMesh()...")



def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 
 
 





def align_bones(difeomorphic_armature, difeomorphic_bone_for_head, difeomorphic_bone_for_tail, vx_armature, vx_bone):
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[difeomorphic_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[difeomorphic_armature]
    ob = bpy.data.objects[difeomorphic_armature]
    bpy.ops.object.editmode_toggle()
    #
    difeomorphic_armature_data = bpy.data.objects[difeomorphic_armature]
    #
    difeomorphic_ebones = difeomorphic_armature_data.data.edit_bones
    # amw is armature matrix world, amwi is the inverse
    difeomorphic_amw = difeomorphic_armature_data.matrix_world
    difeomorphic_amwi = difeomorphic_amw.inverted()
    #
    eb = difeomorphic_ebones[difeomorphic_bone_for_head]
    difeomorphic_eb_matrix_world = difeomorphic_amw * eb.matrix
    difeomorphic_eb_head_world = eb.head + difeomorphic_armature_data.location
    #
    eb = difeomorphic_ebones[difeomorphic_bone_for_tail]
    difeomorphic_eb_matrix_world = difeomorphic_amw * eb.matrix
    difeomorphic_eb_tail_world = eb.tail + difeomorphic_armature_data.location
    #
    #
    #
    bpy.ops.object.editmode_toggle()
    #
    #
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[vx_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[vx_armature]
    ob = bpy.data.objects[vx_armature]
    bpy.ops.object.editmode_toggle()
    #
    armature_data = bpy.data.objects[vx_armature]
    ebones = armature_data.data.edit_bones
    #
    amw = armature_data.matrix_world
    amwi = amw.inverted()
    #
    eb = ebones[vx_bone]
    #eb_matrix_world = difeomorphic_amw * difeomorphic_eb.matrix    
    #
    #eb.matrix = amwi * difeomorphic_eb_matrix_world    
    eb.head = amwi * difeomorphic_eb_head_world
    eb.tail = amwi * difeomorphic_eb_tail_world




def mainGoOverBonesAndAlignThem():
    for index, row in enumerate(leg_bones_matching):
        align_bones(row[0],row[1], row[2])
        print(row[2])
    for index, row in enumerate(hand_bones_matching):
        align_bones(row[0],row[1], row[2])
        print(row[2])
    for index, row in enumerate(spine_bones_matching):
        align_bones(row[0],row[1], row[2])
        print(row[2])            


#mainGoOverBonesAndAlignThem()


def getAlignVectorFromTwoVertices(source_mesh, v1, v2):
    #get align vector in world space from two vertices indexes
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    #fa is the face array indices
    obj = bpy.data.objects[source_mesh]
    vector_from_verts = obj.data.vertices[v1].co - obj.data.vertices[v2].co
    vector_from_verts.normalize()
    alignVector = obj.matrix_world * vector_from_verts
    alignVector.normalize()
    alignVector
    return alignVector


def getAlignVectorFromVertexNormals(source_mesh, va):
    #get align vector in world space from vertex array normals (vertices defined by their indices)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    #fa is the face array indices
    obj = bpy.data.objects[source_mesh]
    averageNormal = mathutils.Vector()
    for v_index in va:
        vertex = obj.data.vertices[f_index]
        # set vertex normal to average of face normals
        averageNormal += vertex.normal
    averageNormal /= len(va)
    alignVector = obj.matrix_world * averageNormal
    alignVector.normalize()
    alignVector
    return alignVector


def getAlignVectorFromFacesArray(source_mesh, fa):
    #get align vector in world space from faces normal averaged
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    #fa is the face array indices
    obj = bpy.data.objects[source_mesh]
    averageNormal = mathutils.Vector()
    for f_index in fa:
        face = obj.data.polygons[f_index]
        # set vertex normal to average of face normals
        averageNormal += face.normal
    averageNormal /= len(fa)
    alignVector = obj.matrix_world * averageNormal
    alignVector.normalize()
    alignVector
    return alignVector


def alignRollWithVector(vector, target_armature, target_bone, offset):
    #set the target_bone roll value to match the vector
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.objects[target_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[target_armature]
    ob = bpy.data.objects[target_armature]
    bpy.ops.object.editmode_toggle()
    #
    #
    armature_data = bpy.data.objects[target_armature]
    ebones = armature_data.data.edit_bones
    eb = ebones[target_bone]
    #
    eb.align_roll(vector)
    eb.roll += radians(offset)


genesis3Toes = {
    "lFoot" : ["lMetatarsals"],
    "rFoot" : ["rMetatarsals"],
    "lToe" : ["lBigToe", "lSmallToe1", "lSmallToe2", "lSmallToe3", "lSmallToe4", "lBigToe_2", "lSmallToe1_2", "lSmallToe2_2", "lSmallToe3_2", "lSmallToe4_2"],
    "rToe" : ["rBigToe", "rSmallToe1", "rSmallToe2", "rSmallToe3", "rSmallToe4", "rBigToe_2", "rSmallToe1_2", "rSmallToe2_2", "rSmallToe3_2", "rSmallToe4_2"]
}

def checkIfVertexGroupExistAndRecreateIt(ob, group):
    if group in ob.vertex_groups.keys():
        vgrp = ob.vertex_groups[group]
        ob.vertex_groups.remove(vgrp)
        vgrp = ob.vertex_groups.new(name=group)
    else:
        vgrp = ob.vertex_groups.new(name=group)
    return vgrp

def renameVertexGroup(ob, oldGroupName, newGroupName):
    if oldGroupName in ob.vertex_groups.keys():
        vgrp = ob.vertex_groups[oldGroupName]
        vgrp.name = newGroupName


def deleteVertexGroup(ob, group):
    if group in ob.vertex_groups.keys():
        vgrp = ob.vertex_groups[group]
        ob.vertex_groups.remove(vgrp)



def mergeSubgroupsIntoGroup(ob, mergers):
    vg_dict = {}
    for group,subGroups in mergers.items():
        #
        vgrp = checkIfVertexGroupExistAndRecreateIt(ob,group)
        #
        subgrps = []
        for subGroup in subGroups:
            if subGroup in ob.vertex_groups.keys():
                subgrps.append(ob.vertex_groups[subGroup])
        idxs = [vg.index for vg in subgrps]
        idxs.append(vgrp.index)
        weights = dict([(vn,0) for vn in range(len(ob.data.vertices))])
        for v in ob.data.vertices:
            for g in v.groups:
                if g.group in idxs:
                    weights[v.index] += g.weight
        #for subgrp in subgrps:
        #    ob.vertex_groups.remove(subgrp)
        #result_string = json.dumps(weights)
        #print (result_string)
        #
        vg_dict[vgrp.name] = weights 
        #       
        for vn,w in weights.items():
            if w > 1e-3:
                #vgrp.add([vn], 0, 'REPLACE')
                vgrp.add([vn], w, 'REPLACE')
        #
        #with open("C:\\Users\\Neon\\Desktop\\dump\dump.txt", 'w') as outfile:
        #    json.dump(vg_dict, outfile, indent=4)


def getCenterFromVertices(vertex_index_list, obj):
	print (obj.name)
	vertex_list = [obj.data.vertices[i] for i in vertex_index_list]
	count = float(len(vertex_list))
	x, y, z = [ sum( [v.co[i] for v in vertex_list] ) for i in range(3)]
	center = (Vector( (x, y, z ) ) / count ) 
	return center



def check_vertices_count_of_the_body(mesh_name, number_of_vertices_the_object_should_have):
    ob = bpy.data.objects[mesh_name] #Genesis 3 Female Mesh
    me = ob.data
    return (len(me.vertices) == number_of_vertices_the_object_should_have)
    
 
#https://blender.stackexchange.com/questions/46584/how-to-align-an-object-so-one-of-its-faces-are-axis-aligned-make-an-object-upr

# obj = bpy.data.objects['Plane']
# face = obj.data.polygons[5951]
# alignVector = obj.matrix_world * face.normal
# alignVector.normalize()
# alignVector

# bpy.ops.object.select_all(action='DESELECT')
# bpy.ops.object.mode_set(mode='OBJECT')
# bpy.data.objects["Armature"].select = True
# bpy.context.scene.objects.active = bpy.data.objects["Armature"]
# ob = bpy.data.objects["Armature"]
# bpy.ops.object.editmode_toggle()


# armature_data = bpy.data.objects['Armature']
# ebones = armature_data.data.edit_bones
# eb = ebones["finger02_joint03.L"]


# eb.align_roll(alignVector)





# import bpy
# import bmesh

# obj = bpy.context.edit_object
# me = obj.data
# bm = bmesh.from_edit_mesh(me)

# for f in bm.faces:
    # if f.select:
        # print(f.index)



#knee_centerX_L=[3410, 4675]
#knee_centerX_R=[10293, 11533]

def armature_make_friendly_ik_joints(ob):
    assert ob is not None and ob.type == 'ARMATURE', "active object invalid"
    #Must make armature active and in edit mode to create a bone
    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    amw = ob.matrix_world
    amwi = amw.inverted()

    armature = bpy.data.armatures[ob.name]
    
    center=dict()
    k = 1
    list_of_bones = ["hip_joint","knee_joint","ankle_joint","ball_joint"]

    
    difeomorphic_body = "Genesis 3 Female Mesh"
    if difeomorphic_body in bpy.data.objects:
        obj = bpy.data.objects[difeomorphic_body]
        center["centerX.L"]= getCenter (knee_centerX_L, obj )[0]
        center["centerX.R"]= getCenter (knee_centerX_R, obj )[0]
    else:
        center["centerX.L"]= armature.edit_bones["knee_joint.L"].head.x
        center["centerX.R"]= armature.edit_bones["knee_joint.R"].head.x
        #for suffix in [".L",".R"]:
        #    for bonename in list_of_bones:
        #        ebone = armature.edit_bones[bonename+suffix]
    
    for suffix in [".L",".R"]:
        if suffix == ".R":
            k = -1
        for bonename in list_of_bones:
            ebone = armature.edit_bones[bonename+suffix]
            ebone.head.x = center["centerX"+suffix]
            ebone.tail.x = center["centerX"+suffix]


        armature.edit_bones["hip_joint"+suffix].tail = armature.edit_bones["knee_joint"+suffix].head
        armature.edit_bones["knee_joint"+suffix].tail = armature.edit_bones["ankle_joint"+suffix].head
        armature.edit_bones["ankle_joint"+suffix].tail = armature.edit_bones["ball_joint"+suffix].head
        armature.edit_bones["toe_joint"+suffix].head =  armature.edit_bones["ball_joint"+suffix].tail

        armature.edit_bones["hip_joint"+suffix].roll = radians(0)
        armature.edit_bones["knee_joint"+suffix].roll = radians(0)
        armature.edit_bones["ankle_joint"+suffix].roll = radians(180) * k
        armature.edit_bones["ball_joint"+suffix].roll = radians(180) * k


        armature.edit_bones["toe_joint"+suffix].length =  0.025
        armature.edit_bones["toe_joint"+suffix].roll = radians(0) 


