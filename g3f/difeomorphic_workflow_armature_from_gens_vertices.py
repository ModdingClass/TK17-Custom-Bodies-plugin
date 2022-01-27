import bpy
from mathutils import Matrix
from ..g3f.difeomorphic_workflow_init_custom_vertex_indices import *
from ..g3f.difeomorphic_workflow_armature_utils import *

def getArmatureBonesDictFromGensVertices(bones_dict):
    print("getArmatureBonesFromBreastVertices()...")
    armature_data = bpy.data.objects['Armature']
    amw = armature_data.matrix_world
    amwi = amw.inverted()
    amwi = Matrix.Identity(4)
    difeomorphic_body = "Genesis 3 Female Mesh"
    
    #
    """                 bpy.ops.object.mode_set(mode='OBJECT')
                #
                bpy.ops.object.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.data.objects[difeomorphic_body].select = True
                bpy.context.scene.objects.active = bpy.data.objects[difeomorphic_body] """
    obj = bpy.data.objects[difeomorphic_body]
    
    vagina_location = getCenter (vagina_center, obj )
    
    vagina_joint01_R_tail = getCenter (vagina_R, obj )
    vagina_joint01_R_head = getCenter (vagina_center, obj )
    vagina_joint01_R_head.x = vagina_joint01_R_tail.x
    
    vagina_jointEnd_R_head = vagina_joint01_R_tail.copy()
    vagina_jointEnd_R_tail = vagina_joint01_R_tail.copy()
    vagina_jointEnd_R_tail.x -= 0.02
    
    vagina_joint01_L_tail = getCenter (vagina_L, obj )
    vagina_joint01_L_head = getCenter (vagina_center, obj )
    vagina_joint01_L_head.x = vagina_joint01_L_tail.x
    
    vagina_jointEnd_L_head = vagina_joint01_L_tail.copy()
    vagina_jointEnd_L_tail = vagina_joint01_L_tail.copy()
    vagina_jointEnd_L_tail.x += 0.02
    
    
    
    anus_head = getCenter (anus_center, obj )
    anus_tail = anus_head.copy()
    anus_tail.x += 0.02
    
    
    
    bones_dict["vagina_joint01.R"]= {"head" : amwi * vagina_joint01_R_head, "tail" : amwi * vagina_joint01_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["vagina_joint01.L"]= {"head" : amwi * vagina_joint01_L_head, "tail" : amwi * vagina_joint01_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    
    bones_dict["vagina_jointEnd.R"]= {"head" : amwi * vagina_jointEnd_R_head, "tail" : amwi * vagina_jointEnd_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["vagina_jointEnd.L"]= {"head" : amwi * vagina_jointEnd_L_head, "tail" : amwi * vagina_jointEnd_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    
    
    bones_dict["anus_joint"]= {"head" : amwi * anus_head, "tail" : amwi * anus_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
