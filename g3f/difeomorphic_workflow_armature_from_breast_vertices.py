import bpy
from mathutils import Matrix
from ..g3f.difeomorphic_workflow_init_custom_vertex_indices import *
from ..g3f.difeomorphic_workflow_armature_utils import *

def getArmatureBonesDictFromBreastVertices(bones_dict):
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
    
    #right
    breast_joint_R_head = getCenter (breast_base_R, obj)
    breast_joint_R_tail = getCenter (breast_top_R, obj)

    nipple_joint01_R_head = getCenter (nipple_base_R, obj)
    nipple_joint01_R_tail = getCenter (nipple_top_R, obj)

    breast_scale_joint_R_head = breast_joint_R_tail
    breast_scale_joint_R_tail = nipple_joint01_R_head

    breast_deform01_joint01_R_head = breast_joint_R_tail
    breast_deform02_joint01_R_head = breast_joint_R_tail
    breast_deform02_joint01_R_head = breast_joint_R_tail

    breast_deform01_joint01_R_tail = getCenter (breast_deform01_R, obj)
    breast_deform02_joint01_R_tail = getCenter (breast_deform02_R, obj)
    breast_deform03_joint01_R_tail = getCenter (breast_deform03_R, obj)

    #left
    breast_joint_L_head = getCenter (breast_base_L, obj)
    breast_joint_L_tail = getCenter (breast_top_L, obj)

    nipple_joint01_L_head = getCenter (nipple_base_L, obj)
    nipple_joint01_L_tail = getCenter (nipple_top_L, obj)

    breast_scale_joint_L_head = breast_joint_L_tail
    breast_scale_joint_L_tail = nipple_joint01_L_head

    breast_deform01_joint01_L_head = breast_joint_L_tail
    breast_deform02_joint01_L_head = breast_joint_L_tail
    breast_deform02_joint01_L_head = breast_joint_L_tail

    breast_deform01_joint01_L_tail = getCenter (breast_deform01_L, obj)
    breast_deform02_joint01_L_tail = getCenter (breast_deform02_L, obj)
    breast_deform03_joint01_L_tail = getCenter (breast_deform03_L, obj)

    extra = Vector((0,-0.01,0))
    #right
    bones_dict["breast_joint.R"]= {"head" : amwi * breast_joint_R_head, "tail" : amwi * breast_joint_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_scale_joint.R"]= {"head" : amwi * breast_scale_joint_R_head, "tail" : amwi * breast_scale_joint_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }

    bones_dict["nipple_joint01.R"]= {"head" : amwi * nipple_joint01_R_head, "tail" : amwi * nipple_joint01_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["nipple_jointEnd.R"]= {"head" : amwi * nipple_joint01_R_tail, "tail" : amwi * nipple_joint01_R_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }


    bones_dict["breast_deform01_joint01.R"]= {"head" : amwi * breast_joint_R_tail, "tail" : amwi * breast_deform01_joint01_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_deform01_jointEnd.R"]= {"head" : amwi * breast_deform01_joint01_R_tail, "tail" : amwi * breast_deform01_joint01_R_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }

    bones_dict["breast_deform02_joint01.R"]= {"head" : amwi * breast_joint_R_tail, "tail" : amwi * breast_deform02_joint01_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_deform02_jointEnd.R"]= {"head" : amwi * breast_deform02_joint01_R_tail, "tail" : amwi * breast_deform02_joint01_R_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }

    bones_dict["breast_deform03_joint01.R"]= {"head" : amwi * breast_joint_R_tail, "tail" : amwi * breast_deform03_joint01_R_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_deform03_jointEnd.R"]= {"head" : amwi * breast_deform03_joint01_R_tail, "tail" : amwi * breast_deform03_joint01_R_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }


    #left
    bones_dict["breast_joint.L"]= {"head" : amwi * breast_joint_L_head, "tail" : amwi * breast_joint_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_scale_joint.L"]= {"head" : amwi * breast_scale_joint_L_head, "tail" : amwi * breast_scale_joint_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }

    bones_dict["nipple_joint01.L"]= {"head" : amwi * nipple_joint01_L_head, "tail" : amwi * nipple_joint01_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["nipple_jointEnd.L"]= {"head" : amwi * nipple_joint01_L_tail, "tail" : amwi * nipple_joint01_L_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }


    bones_dict["breast_deform01_joint01.L"]= {"head" : amwi * breast_joint_L_tail, "tail" : amwi * breast_deform01_joint01_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_deform01_jointEnd.L"]= {"head" : amwi * breast_deform01_joint01_L_tail, "tail" : amwi * breast_deform01_joint01_L_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }

    bones_dict["breast_deform02_joint01.L"]= {"head" : amwi * breast_joint_L_tail, "tail" : amwi * breast_deform02_joint01_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_deform02_jointEnd.L"]= {"head" : amwi * breast_deform02_joint01_L_tail, "tail" : amwi * breast_deform02_joint01_L_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }

    bones_dict["breast_deform03_joint01.L"]= {"head" : amwi * breast_joint_L_tail, "tail" : amwi * breast_deform03_joint01_L_tail, "roll" : 0, "rollOffset" : 0, "connected" : False }
    bones_dict["breast_deform03_jointEnd.L"]= {"head" : amwi * breast_deform03_joint01_L_tail, "tail" : amwi * breast_deform03_joint01_L_tail + extra, "roll" : 0, "rollOffset" : 0, "connected" : False }



