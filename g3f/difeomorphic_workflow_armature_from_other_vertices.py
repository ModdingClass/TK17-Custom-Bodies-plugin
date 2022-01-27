import bpy
from mathutils import Matrix
from ..g3f.difeomorphic_workflow_init_custom_vertex_indices import *
from ..g3f.difeomorphic_workflow_armature_utils import *

def getArmatureBonesDictFromOtherVertices(bones_dict):
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
    
    stomach_joint01_head = getCenter (stomach_base, obj)
    stomach_joint01_tail = getCenter (stomach_top, obj)
    stomach_joint01_head.z = stomach_joint01_tail.z
    #
    stomach_jointEnd_head = stomach_joint01_tail.copy()
    stomach_jointEnd_tail = stomach_joint01_tail.copy()
    stomach_jointEnd_tail.x += 0.02
    
    #calculate locations from vertices
    rib_joint01_R_head = getCenter (rib_base_R, obj)
    rib_joint01_R_tail = getCenter (rib_top_R, obj)
    rib_jointEnd_R_head = rib_joint01_R_tail.copy()
    rib_jointEnd_R_tail = rib_jointEnd_R_head.copy()
    rib_jointEnd_R_tail.x += -0.02
    
    rib_joint01_L_head = getCenter (rib_base_L, obj)
    rib_joint01_L_tail = getCenter (rib_top_L, obj)
    rib_jointEnd_L_head = rib_joint01_L_tail.copy()
    rib_jointEnd_L_tail = rib_jointEnd_L_head.copy()
    rib_jointEnd_L_tail.x += 0.02
    
    butt_joint01_R_head = getCenter (butt_base_R, obj)
    butt_joint01_R_tail = getCenter (butt_top_R, obj)
    butt_joint01_R_head.z = butt_joint01_R_tail.z
    butt_jointEnd_R_head = butt_joint01_R_tail
    butt_jointEnd_R_tail = butt_jointEnd_R_head.copy()
    butt_jointEnd_R_tail.x += -0.02
    
    butt_joint01_L_head = getCenter (butt_base_L, obj)
    butt_joint01_L_tail = getCenter (butt_top_L, obj)
    butt_joint01_L_head.z = butt_joint01_L_tail.z
    butt_jointEnd_L_head = butt_joint01_L_tail
    butt_jointEnd_L_tail = butt_jointEnd_L_head.copy()
    butt_jointEnd_L_tail.x += 0.02
    
    bones_dict["stomach_joint01"]= {"head" : amwi * stomach_joint01_head, "tail" : amwi * stomach_joint01_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["stomach_jointEnd"]= {"head" : amwi * stomach_jointEnd_head, "tail" : amwi * stomach_jointEnd_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    
    bones_dict["rib_joint01.R"]= {"head" : amwi * rib_joint01_R_head, "tail" : amwi * rib_joint01_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["rib_jointEnd.R"]= {"head" : amwi * rib_jointEnd_R_head, "tail" : amwi * rib_jointEnd_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    
    bones_dict["butt_joint01.R"]= {"head" : amwi * butt_joint01_R_head, "tail" : amwi * butt_joint01_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["butt_jointEnd.R"]= {"head" : amwi * butt_jointEnd_R_head, "tail" : amwi * butt_jointEnd_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    
    bones_dict["rib_joint01.L"]= {"head" : amwi * rib_joint01_L_head, "tail" : amwi * rib_joint01_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["rib_jointEnd.L"]= {"head" : amwi * rib_jointEnd_L_head, "tail" : amwi * rib_jointEnd_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    
    bones_dict["butt_joint01.L"]= {"head" : amwi * butt_joint01_L_head, "tail" : amwi * butt_joint01_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["butt_jointEnd.L"]= {"head" : amwi * butt_jointEnd_L_head, "tail" : amwi * butt_jointEnd_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }


