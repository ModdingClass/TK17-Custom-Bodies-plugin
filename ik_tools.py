import bpy
import mathutils
import math

from mathutils import Vector
from mathutils import Matrix
from math import radians
from mathutils.geometry import intersect_point_line

from .dictionaries import *
from .correct_final_rolls import *
from .utils import *

def create_foot_IKs(armature_object):
    ob = armature_object
    armature = ob.data    
    #
    #
    joints_list = [["ball_joint.L","ankle_joint.L","ball_target.L"], ["ball_joint.R","ankle_joint.R","ball_target.R"]]
    for joints in joints_list:

        #Must make armature active and in edit mode to create a bone
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        #
        bone_ball_joint = ob.data.edit_bones[joints[0]] # ball_joint.L   
        bone_ankle_joint= ob.data.edit_bones[joints[1]] # ankle_joint.L
        line_a = bone_ankle_joint.head
        line_b = bone_ankle_joint.tail
        plane_co = bone_ball_joint.head
        plane_no = bone_ball_joint.z_axis
        result = mathutils.geometry.intersect_line_plane(line_a, line_b, plane_co, plane_no, False)
        result_world = ob.matrix_world * result
        # target creation
        #difference = result - bone_ball_joint.head
        editBone_target = ob.data.edit_bones.new(joints[2]) #"leg_target.L"
        editBone_target.parent = bone_ankle_joint
        editBone_target.head= result
        editBone_target.tail = result + Vector((0,0.0,0.05))
        #editBone_target.matrix = bone_ball_joint.matrix
        #editBone_target.translate(difference)
        #editBone_target.length *= -1
        bpy.context.scene.update()
        #
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = ob



def create_arms_IKs(armature_object):
    ob = armature_object
    armature = ob.data    
    #
    #
    joints_list = [["wrist_joint.L","elbow_joint.L", "shoulder_joint.L","arm_target.L", "arm_pole.L"], ["wrist_joint.R","elbow_joint.R","shoulder_joint.R","arm_target.R", "arm_pole.R"]]
    for joints in joints_list:
        #Must make armature active and in edit mode to create a bone
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        #
        bone_wrist_joint= ob.data.edit_bones[joints[0]] # wrist_joint.L
        bone_elbow_joint = ob.data.edit_bones[joints[1]] # elbow_joint.L   
        # lets make the fake ikHandle (target) for VX first
        line = (bone_elbow_joint.head, bone_elbow_joint.tail)
        point = bone_wrist_joint.head
        intersect = intersect_point_line(point, line[0], line[1])
        distance = (intersect[0] - bone_elbow_joint.head).length
        result = intersect[0]
        editBone_target = ob.data.edit_bones.new(joints[3].replace("arm_","arm_fake_" )) #"arm_fake_target.L"
        editBone_target.parent = bone_wrist_joint
        editBone_target.head= result
        editBone_target.tail = result + Vector((0,0.1,0))
        editBone_target.use_deform = False
        bpy.context.scene.update()
        editBone_target.parent = None
        # lets make the real target for blender IK
        editBone_target = ob.data.edit_bones.new(joints[3]) #"arm_target.L"
        editBone_target.parent = bone_elbow_joint
        editBone_target.head= bone_elbow_joint.tail
        editBone_target.tail = editBone_target.head + Vector((0,0.1,0))
        editBone_target.use_deform = False
        bpy.context.scene.update()
        editBone_target.parent = None        
        # 
        #pole creation
        bone_shoulder_joint= ob.data.edit_bones[joints[2]]  #"shoulder_joint.L"
        editBone_pole = ob.data.edit_bones.new(joints[4])  #"arm_pole.L"
        editBone_pole.head = Vector([0, 0, 0])
        editBone_pole.tail = Vector([0, 0, bone_shoulder_joint.length])
        editBone_pole.matrix = bone_shoulder_joint.matrix.copy()
        local_translation = Matrix.Translation((0.0, bone_shoulder_joint.length, -0.50))
        editBone_pole.matrix *= local_translation
        editBone_pole.length *= -1
        editBone_pole.tail = editBone_pole.head + Vector([0, 0, 0.1])
        editBone_pole.roll = 0
        editBone_pole.use_deform = False
        #
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='POSE')
        #
        bone = armature.bones[bone_elbow_joint.name]
        #
        ik_constraint = None
        ik_constraints = [ c for c in ob.pose.bones[bone.name].constraints if c.type=='IK']
        if len(ik_constraints)>0:
            print("Constraint exists!")
            ik_constraint = ik_constraints[0]
        else:
            print("Making a new constraint!")
            ik_constraint = ob.pose.bones[bone.name].constraints.new('IK')
        
        
        ik_constraint.target = ob
        ik_constraint.subtarget = joints[3] # arm_target.L
        ik_constraint.pole_target = ob
        ik_constraint.pole_subtarget = joints[4] # arm_pole.L
        ik_constraint.chain_count = 2
        ik_constraint.pole_angle = radians(-90)    

def create_legs_IKs(armature_object):
    ob = armature_object
    armature = ob.data    
    #
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    ik_list_to_remove = ["leg_target.L", "leg_pole.L","leg_target.R", "leg_pole.R","ball_target.L","ball_target.R","arm_target.L","arm_target.R","arm_fake_target.L","arm_fake_target.R","arm_pole.L","arm_pole.R"]
    for ik_bone_name in ik_list_to_remove:
        bone = armature.edit_bones.get(ik_bone_name)
        if bone is not None:
            armature.edit_bones.remove(bone)
    #
    joints_list = [["ankle_joint.L","knee_joint.L", "hip_joint.L","leg_target.L", "leg_pole.L"], ["ankle_joint.R","knee_joint.R","hip_joint.R","leg_target.R", "leg_pole.R"]]
    for joints in joints_list:
        #Must make armature active and in edit mode to create a bone
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        #
        bone_ankle_joint= ob.data.edit_bones[joints[0]] # ankle_joint.L
        bone_knee_joint = ob.data.edit_bones[joints[1]] # knee_joint.L   bone_knee_joint = ob.data.edit_bones[knee_joint.L] 
        line_a = bone_knee_joint.head
        line_b = bone_knee_joint.tail
        plane_co = bone_ankle_joint.head
        plane_no = bone_ankle_joint.z_axis
        result = mathutils.geometry.intersect_line_plane(line_a, line_b, plane_co, plane_no, False)
        result_world = ob.matrix_world * result
        # target creation
        difference = result - bone_ankle_joint.head
        editBone_target = ob.data.edit_bones.new(joints[3]) #"leg_target.L"
        editBone_target.parent = None
        editBone_target.head= result
        editBone_target.tail = result + Vector((0,0.1,0))
        editBone_target.matrix = bone_ankle_joint.matrix
        editBone_target.translate(difference)
        editBone_target.length *= -1
        editBone_target.use_deform = False
        bpy.context.scene.update()
        #difference = editBone_target.head - result
        #print("difference: ")
        #print (difference)
        #editBone_target.head= result
        #editBone_target.tail = result + Vector((0,0.1,0))
        # pole creation
        #
        bone_hip_joint= ob.data.edit_bones[joints[2]]  #"hip_joint.L"
        editBone_pole = ob.data.edit_bones.new(joints[4])  #"leg_pole.L"
        editBone_pole.head = Vector([0, 0, 0])
        editBone_pole.tail = Vector([0, 0, bone_hip_joint.length])
        editBone_pole.matrix = bone_hip_joint.matrix.copy()
        local_translation = Matrix.Translation((0.0, bone_hip_joint.length, -0.50))
        editBone_pole.matrix *= local_translation
        editBone_pole.length *= -1
        editBone_pole.tail = editBone_pole.head + Vector([0, 0, 0.1])
        editBone_pole.roll = 0
        editBone_pole.use_deform = False
        #
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = ob
        bpy.ops.object.mode_set(mode='POSE')
        #
        bone = armature.bones[bone_knee_joint.name]
        #
        ik_constraint = None
        ik_constraints = [ c for c in ob.pose.bones[bone.name].constraints if c.type=='IK']
        if len(ik_constraints)>0:
            print("Constraint exists!")
            ik_constraint = ik_constraints[0]
        else:
            print("Making a new constraint!")
            ik_constraint = ob.pose.bones[bone.name].constraints.new('IK')
        
        
        ik_constraint.target = ob
        ik_constraint.subtarget = joints[3] # leg_target.L
        ik_constraint.pole_target = ob
        ik_constraint.pole_subtarget = joints[4] # leg_pole.L
        ik_constraint.chain_count = 2
        ik_constraint.pole_angle = radians(-90)    

def create_IKs(armature_object):
    create_legs_IKs(armature_object)
    create_arms_IKs(armature_object) 
    create_foot_IKs(armature_object)
    if (True == True):
        return
    center_list = ["spine_joint01","spine_joint02","spine_joint03","spine_joint04","spine_jointEnd","neck_joint01","neck_jointEnd","head_joint01","head_joint02","head_jointEnd"]
    #
    #
    ob = armature_object
    armature = ob.data    
    #
    #
    #Must make armature active and in edit mode to create a bone
    #bpy.context.scene.objects.active = armature_object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #
    armature_matrix_world = ob.matrix_world
    #
    bone_ankle_joint_L = ob.data.edit_bones["ankle_joint.L"]
    bone_knee_joint_L = ob.data.edit_bones["knee_joint.L"]
    line_a = bone_knee_joint_L.head
    line_b = bone_knee_joint_L.tail
    plane_co = bone_ankle_joint_L.head
    plane_no = bone_ankle_joint_L.z_axis
    result = mathutils.geometry.intersect_line_plane(line_a, line_b, plane_co, plane_no, False)
    result_world = ob.matrix_world * result
    editBone = bpy.context.object.data.edit_bones.new("leg_ik.L")
    editBone.head= result
    editBone.tail = result + Vector((0,0.1,0))
    #
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.scene.objects.active = ob
    bpy.ops.object.mode_set(mode='POSE')
    #
    bone = armature.bones["knee_joint.L"]

    ik_constraint = None
    ik_constraints = [ c for c in ob.pose.bones[bone.name].constraints if c.type=='IK']
    if len(ik_constraints)>0:
        print("Constraint exists!")
        ik_constraint = ik_constraints[0]
    else:
        print("Making a new constraint!")
        ik_constraint = ob.pose.bones[bone.name].constraints.new('IK')
    
    
    ik_constraint.target = ob
    ik_constraint.subtarget = "leg_ik.L"
    ik_constraint.pole_target = ob
    ik_constraint.pole_subtarget = "pole.L"
    ik_constraint.chain_count = 2
    ik_constraint.pole_angle = radians(-94.4856)
    if (True == True):
        return
    
    pose_bone_knee_joint_L = ob.pose.bones["knee_joint.L"]
    #set it as active pose bone 
    bpy.context.object.data.bones.active = pose_bone_knee_joint_L.bone
    #bpy.ops.pose.constraint_add(type='IK')
    ik_constraint = None
    pose_bone_knee_joint_L_constraints = [c for c in pose_bone_knee_joint_L.constraints if c.type=='IK']
    if (pose_bone_knee_joint_L_constraints!=None and len(pose_bone_knee_joint_L_constraints)>0):
        ik_constraint = pose_bone_knee_joint_L_constraints[0]
    else:
        ik_constraint = bpy.ops.pose.constraint_add(type='IK')
    ik_constraint.target = armature_object
    ik_constraint.subtarget = "leg_ik.L"
    ik_constraint.pole_target = armature_object
    ik_constraint.pole_subtarget = "pole.L"
    ik_constraint.chain_count = 2
    #result_world
    #bpy.context.scene.cursor_location = result_world

    my_bones = [] 
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
        #print ("bone: " + bone.name)
        ob = bpy.data.objects.new( "_"+villafyname(bone.name), None )
        ob.rotation_mode = 'YZX'
        if bone.name != "root":
            ob.parent = bpy.data.objects[ "_"+villafyname(bone.parent.name)]    
            print (ob.name+ " "+ob.parent.name)
        #if "wrist_joint.L" in bone.name :
        #    bone.length *= -1    
        if bone.get("isFlipped") is not None and bone["isFlipped"] == True :
            bone.length *= -1    
        ob.matrix_world = armature_matrix_world * bone.matrix        
        if bone.get("isFlipped") is not None and bone["isFlipped"] == True :
            bone.length *= -1    
        #if "wrist_joint.L" in bone.name :
        #    bone.length *= -1            
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()
        if villafyname(bone.name) in center_list:
            ob.location.x    = 0
        #ob.show_axis = True        
        bpy.context.scene.objects.link( ob )
    #
    #eb = bpy.data.armatures['Armature'].edit_bones
    bone_ankle_joint_L = ob.data.edit_bones["ankle_joint.L"]
    bone_knee_joint_L = ob.data.edit_bones["knee_joint.L"]
    line_a = bone_knee_joint_L.head
    line_b = bone_knee_joint_L.tail
    plane_co = bone_ankle_joint_L.head
    plane_no = bone_ankle_joint_L.y_axis
    #	
    bone_knee_joint_L_matrix = bone_knee_joint_L.matrix
    bone_knee_joint_L_matrix.translation = bone_knee_joint_L.tail
    bone_knee_joint_L_matrix_world = armature_matrix_world * bone_knee_joint_L_matrix
    ob = bpy.data.objects.new( "_kneetail_L_joint", None )
    ob.parent = bpy.data.objects[ "_hip_L_joint"]    
    ob.matrix_world = bone_knee_joint_L_matrix_world
    ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    ob.matrix_parent_inverse.identity()
    bpy.context.scene.objects.link( ob )
    #line_a (mathutils.Vector) – First point of the first line
    #line_b (mathutils.Vector) – Second point of the first line
    #plane_co (mathutils.Vector) – A point on the plane
    #plane_no (mathutils.Vector) – The direction the plane is facing
    # 
    bone_knee_joint_R = ob.data.edit_bones["knee_joint.R"]
    #
    ob = bpy.data.objects.new( "_mouth_L_fix_group", None )
    ob.rotation_mode = 'YZX'
    ob.parent = bpy.data.objects[ "_head_joint02"]    
    ob.matrix_world =  bpy.data.objects[ "_upper_lip_L_joint02"].matrix_world
    ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    ob.matrix_parent_inverse.identity()
    bpy.context.scene.objects.link( ob )
    #
    ob = bpy.data.objects.new( "_mouth_R_fix_group", None )
    ob.rotation_mode = 'YZX'
    ob.parent = bpy.data.objects[ "_head_joint02"]    
    ob.matrix_world =  bpy.data.objects[ "_upper_lip_R_joint02"].matrix_world
    ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    ob.matrix_parent_inverse.identity()
    bpy.context.scene.objects.link( ob )
    #
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #
    bpy.ops.object.delete() 
    bpy.ops.object.select_all(action='DESELECT')
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    armature_object.select = True



def fixJointsUsedAsEffectors(target_armature):
    print ("fixJointsUsedAsEffectors")
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[target_armature].select = True
    bpy.context.scene.objects.active = bpy.data.objects[target_armature]
    ob = bpy.data.objects[target_armature]
    bpy.ops.object.mode_set(mode='EDIT')
    armature_data = bpy.data.objects[target_armature]
    ebones = armature_data.data.edit_bones
    #
    #first we try to fix the knee bone to make it closer to the ankle
    # knee bones
    startBone = "knee_joint.L"
    endBone = "ankle_joint.L"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones[startBone].length = distance
    #also move the ankles head to the knee tail
    ebones[endBone].head = localCo
    #
    startBone = "knee_joint.R"
    endBone = "ankle_joint.R"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones[startBone].length = distance    
    #also move the ankles head to the knee tail
    ebones[endBone].head = localCo
    #
    #makeBonesCollinearFromBoneHeadToBoneTail(target_armature,["hip_joint.L","knee_joint.L"])
    #makeBonesCollinearFromBoneHeadToBoneTail(target_armature,["hip_joint.R","knee_joint.R"])    
    # hip bones
    #startBone = "hip_joint.L"
    #endBone = "knee_joint.L"
    #localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    #ebones[startBone].length = distance
    #startBone = "hip_joint.R"
    #endBone = "knee_joint.R"
    #localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    #ebones[startBone].length = distance
    # ankle bones
    startBone = "ankle_joint.L"
    endBone = "ball_joint.L"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones[startBone].length = distance
    startBone = "ankle_joint.R"
    endBone = "ball_joint.R"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones[startBone].length = distance
    # ankles tail must match the ball head
    ebones["ankle_joint.L"].tail = ebones["ball_joint.L"].head
    ebones["ankle_joint.R"].tail = ebones["ball_joint.R"].head
    #elbows - forearms
    startBone = "elbow_joint.L"
    endBone = "wrist_joint.L"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones["forearm_joint.L"].tail = localCo
    startBone = "elbow_joint.L"
    endBone = "forearm_joint.L"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones["forearm_joint.L"].head = localCo
    #also fix the wrists ?!?!? why not in the end...
    ebones["wrist_joint.L"].head = ebones["forearm_joint.L"].tail
    #
    startBone = "elbow_joint.R"
    endBone = "wrist_joint.R"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones["forearm_joint.R"].tail = localCo
    startBone = "elbow_joint.R"
    endBone = "forearm_joint.R"
    localCo, worldCo, distance, translationAlongY = getClosestPointFromBoneProjection(target_armature,startBone, endBone)
    ebones["forearm_joint.R"].head = localCo
    #
    #also fix the wrists ?!?!? why not in the end...
    ebones["wrist_joint.R"].head = ebones["forearm_joint.R"].tail
    #make forearm elbow collinear
    makeBonesCollinearFromBoneHeadToBoneTail(target_armature,["elbow_joint.L","forearm_joint.L"])
    makeBonesCollinearFromBoneHeadToBoneTail(target_armature,["elbow_joint.R","forearm_joint.R"])




def getIKValues(armatureName,bone, boneEnd):
	armature_ob = bpy.context.scene.objects[armatureName]
	#armature_data = armature_ob.data
	bpy.ops.object.mode_set(mode='EDIT', toggle=False)
	eb_bone = armature_ob.data.edit_bones[bone]
	eb_boneEnd = armature_ob.data.edit_bones[boneEnd]
	line = (eb_bone.head, eb_bone.tail)
	point = eb_boneEnd.head
	intersect = intersect_point_line(point, line[0], line[1])
	distance = (intersect[0] - eb_bone.head).length
	ikEffector = Vector ((distance,0,0))
	ikHandle = armature_ob.matrix_world * intersect[0]
	bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
	return ikEffector,ikHandle

def getClosestPointFromBoneProjection(armatureName, fromBone, toBone):
    initial_mode = bpy.context.object.mode
    armature_ob = bpy.context.scene.objects[armatureName]
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    armature_ob.select = True
    bpy.context.scene.objects.active = armature_ob
    #
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #
    from_joint= armature_ob.data.edit_bones[fromBone]
    to_joint = armature_ob.data.edit_bones[toBone] 
    #
    line = (from_joint.head, from_joint.tail)
    point = to_joint.head
    intersect = intersect_point_line(point, line[0], line[1])
    localCo = intersect[0]
    worldCo = armature_ob.matrix_world * localCo
    distance = (localCo - from_joint.head).length
    translationAlongY = Vector ((distance,0,0))
    bpy.ops.object.mode_set ( mode = initial_mode )
    return localCo, worldCo, distance, translationAlongY

def makeBonesCollinearFromBoneHeadToBoneTail(armatureName, boneArray):
    initial_mode = bpy.context.object.mode
    armature_ob = bpy.context.scene.objects[armatureName]
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    armature_ob.select = True
    bpy.context.scene.objects.active = armature_ob
    #
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #
    fromBone = armature_ob.data.edit_bones[boneArray[0]]
    toBone = armature_ob.data.edit_bones[boneArray[-1]] 
    line = (fromBone.head, toBone.tail)
    for bone in boneArray:
        if bone == fromBone.name:
            point = armature_ob.data.edit_bones[bone].tail
            intersect = intersect_point_line(point, line[0], line[1])
            localCo = intersect[0]
            armature_ob.data.edit_bones[bone].tail = localCo
        if bone == toBone.name:
            point = armature_ob.data.edit_bones[bone].head
            intersect = intersect_point_line(point, line[0], line[1])
            localCo = intersect[0]
            armature_ob.data.edit_bones[bone].head = localCo            
        else:
            point = armature_ob.data.edit_bones[bone].head
            intersect = intersect_point_line(point, line[0], line[1])
            localCo = intersect[0]
            armature_ob.data.edit_bones[bone].head = localCo            
            #
            point = armature_ob.data.edit_bones[bone].tail
            intersect = intersect_point_line(point, line[0], line[1])
            localCo = intersect[0]
            armature_ob.data.edit_bones[bone].tail = localCo     
    #
    for index, bone in enumerate(boneArray):
        if bone == toBone.name:
            continue
        else:
            armature_ob.data.edit_bones[bone].tail = armature_ob.data.edit_bones[boneArray[index+1]].head       
    #
    #done with making bone collinear

def create_HHPoseIk(armature):
    hh_empties_draw = [
            {"name":"foot_L_target01","draw":"ARROWS","size":0.02},
            {"name":"leg_L_offset_group","draw":"CUBE","size":0.01},
            {"name":"ball_L_group","draw":"SPHERE","size":0.02},
            {"name":"tiptoe_L_rotation_group","draw":"CONE","size":0.01},
            {"name":"knee_L_group_pivot","draw":"ARROWS","size":0.05},
    ]
    #
    oba = bpy.data.objects["Armature"]
    ahhl = oba["HHPoseValuesL"]
    hh_empties = [
        {"name":"foot_L_target01","parent":"","location":ahhl["foot_L_target01"],"rotation":[0, 0, 0]}, #0.113, 0.095 this is how the game inits the leg L value in PoseEdit, is the foot manipulator The values for it are set in **SplineVector3f** :local_54956
        {"name":"foot_L_parent","parent":"foot_L_target01","location":[],"rotation":[0, 0, 0]},
        {"name":"leg_L_group","parent":"foot_L_parent","location":[],"rotation":[0, 0, 0]},
        {"name":"foot_L_rotation_group","parent":"leg_L_group","location":[],"rotation":[0, 0, 0]},
        {"name":"leg_L_offset_group","parent":"foot_L_rotation_group","location":[0.0, 0.0, 0.135],"rotation":[42,0,0]}, # this is important, has values, this is used in HH pose init (SplineVector3f :local_10278 and SplineVector3f :local_10279)
        {"name":"tip_toe_L_group","parent":"leg_L_offset_group","location":[],"rotation":[0, 0, 0]},
        {"name":"ball_L_group","parent":"tip_toe_L_group","location":[],"rotation":[0, 0, 0],"constraint":"tip_toe_L_group_pivot"}, #what about SSimpleTransform.Translation Vector3f( 0.00019925147, 0, 0.000105514795 ) ???
        {"name":"ball_L_group_pivot","parent":"ball_L_group","location":ahhl["ball_L_group_pivot"],"rotation":[0, 0, 0]}, #-0.00016800423, 0.0160358, 0.14387479
        {"name":"leg_L_ikHandle","parent":"ball_L_group","location":[],"rotation":[0, 0, 0]},
        {"name":"leg_L_ikHandle_pivot","parent":"leg_L_ikHandle","location":ahhl["leg_L_ikHandle_pivot"],"rotation":[0, 0, 0]}, #  RotationPivot Vector3f( -0.00016801599, 0.0903118, 0.0416234 );
        {"name":"leg_L_ikHandle_target","parent":"leg_L_ikHandle_pivot","location":[],"rotation":[0, 0, 0]}, #  RotationPivot Vector3f( -0.00016801599, 0.0903118, 0.0416234 );
        {"name":"tip_toe_L_group_pivot","parent":"tip_toe_L_group","location":ahhl["tip_toe_L_group_pivot"],"rotation":[0, 0, 0]}, #from parent STransform.RotationPivot Vector3f( -0.00016799147, 0.0113661, 0.241317 );
        {"name":"tiptoe_L_ikHandle","parent":"tip_toe_L_group","location":[],"rotation":[0, 0, 0],"constraint":"tip_toe_L_group_pivot"},
        {"name":"tiptoe_L_ikHandle_pivot","parent":"tiptoe_L_ikHandle","location":ahhl["tiptoe_L_ikHandle_pivot"],"rotation":[0, 0, 0]},
        {"name":"tiptoe_L_ikHandle_target","parent":"tiptoe_L_ikHandle_pivot","location":[],"rotation":[0, 0, 0]},
        {"name":"tiptoe_L_ikHandle_pole","parent":"tiptoe_L_ikHandle_target","location":ahhl["tiptoe_L_ikHandle_pole"],"rotation":[0, 0, 0]}, # the pole i think are values from the pivot minus the values from the game pole
        {"name":"tiptoe_L_rotation_group","parent":"leg_L_offset_group","location":[0.0, 0, 0],"rotation":[0,0.0,-0.0]}, #rot actual: -40 -> this was moved to the pivot below
        {"name":"tiptoe_L_rotation_group_pivot","parent":"tiptoe_L_rotation_group","location":ahhl["tiptoe_L_rotation_group_pivot"],"rotation":[-40, 0, 0]}, #STransform.RotationPivot Vector3f( -0.00016800406, 0.0160358, 0.14387479 );
        {"name":"tiptoe_L_rotation_ikHandle","parent":"tiptoe_L_rotation_group","location":[],"rotation":[0, 0, 0],"constraint":"tiptoe_L_rotation_group_pivot"},
        {"name":"tiptoe_L_rotation_ikHandle_pivot","parent":"tiptoe_L_rotation_ikHandle","location":ahhl["tiptoe_L_rotation_ikHandle_pivot"],"rotation":[0, 0, 0],"constraint":"tiptoe_L_rotation_group_pivot"},
        {"name":"tiptoe_L_rotation_ikHandle_target","parent":"tiptoe_L_rotation_ikHandle_pivot","location":ahhl["tiptoe_L_rotation_ikHandle_target"],"rotation":[0, 0, 0]}, #values from pivot
        {"name":"tiptoe_L_rotation_ikHandle_pole","parent":"tiptoe_L_rotation_ikHandle_target","location":ahhl["tiptoe_L_rotation_ikHandle_pole"],"rotation":[0, 0, 0]}, #values from sum between pivot above + pole (SIKHandle :local_57070 SIKHandle.PoleVector)
        {"name":"knee_L_group","parent":"leg_L_group","location":[],"rotation":[0, 0, 0]},
        {"name":"knee_L_group_pivot","parent":"knee_L_group","location":ahhl["knee_L_group_pivot"],"rotation":[0, 0, 0]},
        {"name":"knee_L_locator","parent":"knee_L_group_pivot","location":[],"rotation":[0, 0, 0],"constraint":"knee_L_group_pivot"},
    ]


    #0.112832, -0.048875, 0.016036 - cursor location matching the head of ball_joint.L
    #0.113, 0.095

    prefix = "hhe_"
    prefix = ""

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        ob = bpy.data.objects.new( name, None )
        bpy.context.scene.objects.link( ob )

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        parent = prefix + hh_empty["parent"]
        print (parent)
        if parent != prefix:
            print ("adding "+ parent + " as parent for "+name)
            bpy.data.objects[name].parent = bpy.data.objects[parent]

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        location = hh_empty["location"]
        rotation = hh_empty["rotation"]
        if len(location) == 3:
            bpy.data.objects[name].location = Vector ((location[0],location[1],location[2]))
        if len(rotation) == 3:
            bpy.data.objects[name].rotation_euler = Vector ((radians(rotation[0]),radians(rotation[1]),radians(rotation[2])))        

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        bpy.data.objects[name].hide = True
        bpy.data.objects[name].hide_select = True
        bpy.data.objects[name].hide_render = True
        #
        bpy.data.objects[name].lock_location[0] = True
        bpy.data.objects[name].lock_location[1] = True
        bpy.data.objects[name].lock_location[2] = True
        #
        bpy.data.objects[name].lock_rotation[0] = True
        bpy.data.objects[name].lock_rotation[1] = True
        bpy.data.objects[name].lock_rotation[2] = True
        #
        bpy.data.objects[name].lock_scale[0] = True
        bpy.data.objects[name].lock_scale[1] = True
        bpy.data.objects[name].lock_scale[2] = True    

    for hh_empty in ["foot_L_target01","leg_L_offset_group","ball_L_group","tiptoe_L_rotation_group_pivot","knee_L_group_pivot"]:
        name = prefix + hh_empty
        bpy.data.objects[name].hide = False
        bpy.data.objects[name].hide_select = False
        bpy.data.objects[name].hide_select = False
        bpy.data.objects[name].hide_render = True
        bpy.data.objects[name].lock_location[0] = False
        bpy.data.objects[name].lock_location[1] = False
        bpy.data.objects[name].lock_location[2] = False
        #
        bpy.data.objects[name].lock_rotation[0] = False
        bpy.data.objects[name].lock_rotation[1] = False
        bpy.data.objects[name].lock_rotation[2] = False
        #
        bpy.data.objects[name].lock_scale[0] = False
        bpy.data.objects[name].lock_scale[1] = False
        bpy.data.objects[name].lock_scale[2] = False       

    bpy.data.objects["tiptoe_L_rotation_ikHandle_target"].hide = False
    bpy.data.objects["tiptoe_L_rotation_ikHandle_target"].hide_select = False
    bpy.data.objects["tiptoe_L_rotation_ikHandle_pole"].hide = False
    bpy.data.objects["tiptoe_L_rotation_ikHandle_pole"].hide_select = False
    bpy.data.objects["tiptoe_L_rotation_ikHandle_pivot"].hide = False
    bpy.data.objects["tiptoe_L_rotation_ikHandle_pivot"].hide_select = False

    ############################################################################
    ob = bpy.data.objects["tiptoe_L_rotation_ikHandle_pivot"]

    tiptoe_L_rotation_ikHandle_pivot_constraint = None
    tiptoe_L_rotation_ikHandle_pivot_constraints = [ c for c in ob.constraints if c.type=='COPY_TRANSFORMS']

    if len(tiptoe_L_rotation_ikHandle_pivot_constraints)>0:
        print("Constraint exists!")
        tiptoe_L_rotation_ikHandle_pivot_constraint = tiptoe_L_rotation_ikHandle_pivot_constraints[0]
    else:
        print("Making a new constraint!")    
        tiptoe_L_rotation_ikHandle_pivot_constraint = ob.constraints.new('COPY_TRANSFORMS')
        tiptoe_L_rotation_ikHandle_pivot_constraint.target = bpy.data.objects["tiptoe_L_rotation_group_pivot"]

    ob.empty_draw_type = 'CIRCLE'
    ob.empty_draw_size = 0.05

    bpy.context.scene.update()

    #############################################################################

    # for hh_empty in hh_empties:
        # name = prefix + hh_empty["name"]
        # constraint = hh_empty.get("constraint")
        # if constraint != None:
            # constraint = prefix + constraint
            # print (constraint)
            # if constraint != prefix:
                # pivot_constraint = bpy.data.objects[name].constraints.new('PIVOT')
                # print ("adding "+ constraint + " as constraint for "+name)
                # pivot_constraint.target = bpy.data.objects[constraint]
                # pivot_constraint.rotation_range = 'ALWAYS_ACTIVE'
                # pivot_constraint.mute = True

    for hh_empty in hh_empties_draw:
        name = prefix + hh_empty["name"]
        draw = hh_empty.get("draw")
        size = hh_empty.get("size")
        bpy.data.objects[name].empty_draw_type = draw
        bpy.data.objects[name].empty_draw_size = size



    ik_for_bones = [
        {"bone":"knee_joint.L","target":"leg_L_ikHandle_target","pole_target":"knee_L_group_pivot","pole_angle":-90,"chain_length":2},
        {"bone":"ankle_joint.L","target":"tiptoe_L_ikHandle_target","pole_target":"tiptoe_L_ikHandle_pole","pole_angle":-90,"chain_length":1},
        {"bone":"ball_joint.L","target":"tiptoe_L_rotation_ikHandle_target","pole_target":"tiptoe_L_rotation_ikHandle_pole","pole_angle":-90,"chain_length":1},

    ]
    ob = bpy.data.objects["Armature"]
    for ik_bones in ik_for_bones:
        name = ik_bones["bone"]
        target = ik_bones["target"]
        pole_target = ik_bones["pole_target"]
        pole_angle = ik_bones.get("pole_angle")
        chain_length = ik_bones.get("chain_length")
        #
        ik_constraint = None
        ik_constraints = [ c for c in ob.pose.bones[name].constraints if c.type=='IK']
        if len(ik_constraints)>0:
            print("Constraint exists!")
            ik_constraint = ik_constraints[0]
        else:
            print("Making a new constraint!")    
            ik_constraint = ob.pose.bones[name].constraints.new('IK')
        ik_constraint.target = bpy.data.objects[target]
        ik_constraint.pole_target = bpy.data.objects[pole_target]
        ik_constraint.chain_count = chain_length
        ik_constraint.pole_angle = radians(pole_angle)  


    bpy.context.scene.update()




    ob = bpy.data.objects["leg_L_offset_group"]
    ob.location = Vector ( (0,0,0) )
    ob.rotation_euler = Vector ( ( radians(0), radians(0), radians(0)) )

    ob = bpy.data.objects["tiptoe_L_rotation_group_pivot"]
    ob.rotation_euler = Vector ( ( radians(0), radians(0), radians(0)) )

    bpy.context.scene.update()

    hh_empties_draw = [
            {"name":"foot_R_target01","draw":"ARROWS","size":0.02},
            {"name":"leg_R_offset_group","draw":"CUBE","size":0.01},
            {"name":"ball_R_group","draw":"SPHERE","size":0.02},
            {"name":"tiptoe_R_rotation_group","draw":"CONE","size":0.01},
            {"name":"knee_R_group_pivot","draw":"ARROWS","size":0.05},
    ]
    #
    oba = bpy.data.objects["Armature"]
    ahhr = oba["HHPoseValuesR"]
    hh_empties = [
        {"name":"foot_R_target01","parent":"","location":ahhr["foot_R_target01"],"rotation":[0, 0, 0]}, #0.113, 0.095 this is how the game inits the leg L value in PoseEdit, is the foot manipulator The values for it are set in **SplineVector3f** :local_54956
        {"name":"foot_R_parent","parent":"foot_R_target01","location":[],"rotation":[0, 0, 0]},
        {"name":"leg_R_group","parent":"foot_R_parent","location":[],"rotation":[0, 0, 0]},
        {"name":"foot_R_rotation_group","parent":"leg_R_group","location":[],"rotation":[0, 0, 0]},
        {"name":"leg_R_offset_group","parent":"foot_R_rotation_group","location":[0.0, 0.0, 0.135],"rotation":[42,0,0]}, # this is important, has values, this is used in HH pose init (SplineVector3f :local_10278 and SplineVector3f :local_10279)
        {"name":"tip_toe_R_group","parent":"leg_R_offset_group","location":[],"rotation":[0, 0, 0]},
        {"name":"ball_R_group","parent":"tip_toe_R_group","location":[],"rotation":[0, 0, 0],"constraint":"tip_toe_R_group_pivot"}, #what about SSimpleTransform.Translation Vector3f( 0.00019925147, 0, 0.000105514795 ) ???
        {"name":"ball_R_group_pivot","parent":"ball_R_group","location":ahhr["ball_R_group_pivot"],"rotation":[0, 0, 0]}, #-0.00016800423, 0.0160358, 0.14387479
        {"name":"leg_R_ikHandle","parent":"ball_R_group","location":[],"rotation":[0, 0, 0]},
        {"name":"leg_R_ikHandle_pivot","parent":"leg_R_ikHandle","location":ahhr["leg_R_ikHandle_pivot"],"rotation":[0, 0, 0]}, #  RotationPivot Vector3f( -0.00016801599, 0.0903118, 0.0416234 );
        {"name":"leg_R_ikHandle_target","parent":"leg_R_ikHandle_pivot","location":[],"rotation":[0, 0, 0]}, #  RotationPivot Vector3f( -0.00016801599, 0.0903118, 0.0416234 );
        {"name":"tip_toe_R_group_pivot","parent":"tip_toe_R_group","location":ahhr["tip_toe_R_group_pivot"],"rotation":[0, 0, 0]}, #from parent STransform.RotationPivot Vector3f( -0.00016799147, 0.0113661, 0.241317 );
        {"name":"tiptoe_R_ikHandle","parent":"tip_toe_R_group","location":[],"rotation":[0, 0, 0],"constraint":"tip_toe_R_group_pivot"},
        {"name":"tiptoe_R_ikHandle_pivot","parent":"tiptoe_R_ikHandle","location":ahhr["tiptoe_R_ikHandle_pivot"],"rotation":[0, 0, 0]},
        {"name":"tiptoe_R_ikHandle_target","parent":"tiptoe_R_ikHandle_pivot","location":[],"rotation":[0, 0, 0]},
        {"name":"tiptoe_R_ikHandle_pole","parent":"tiptoe_R_ikHandle_target","location":ahhr["tiptoe_R_ikHandle_pole"],"rotation":[0, 0, 0]}, # the pole i think are values from the pivot minus the values from the game pole
        {"name":"tiptoe_R_rotation_group","parent":"leg_R_offset_group","location":[0.0, 0, 0],"rotation":[0,0.0,-0.0]}, #rot actual: -40 -> this was moved to the pivot below
        {"name":"tiptoe_R_rotation_group_pivot","parent":"tiptoe_R_rotation_group","location":ahhr["tiptoe_R_rotation_group_pivot"],"rotation":[-40, 0, 0]}, #STransform.RotationPivot Vector3f( -0.00016800406, 0.0160358, 0.14387479 );
        {"name":"tiptoe_R_rotation_ikHandle","parent":"tiptoe_R_rotation_group","location":[],"rotation":[0, 0, 0],"constraint":"tiptoe_R_rotation_group_pivot"},
        {"name":"tiptoe_R_rotation_ikHandle_pivot","parent":"tiptoe_R_rotation_ikHandle","location":ahhr["tiptoe_R_rotation_ikHandle_pivot"],"rotation":[0, 0, 0],"constraint":"tiptoe_R_rotation_group_pivot"},
        {"name":"tiptoe_R_rotation_ikHandle_target","parent":"tiptoe_R_rotation_ikHandle_pivot","location":ahhr["tiptoe_R_rotation_ikHandle_target"],"rotation":[0, 0, 0]}, #values from pivot
        {"name":"tiptoe_R_rotation_ikHandle_pole","parent":"tiptoe_R_rotation_ikHandle_target","location":ahhr["tiptoe_R_rotation_ikHandle_pole"],"rotation":[0, 0, 0]}, #values from sum between pivot above + pole (SIKHandle :local_57070 SIKHandle.PoleVector)
        {"name":"knee_R_group","parent":"leg_R_group","location":[],"rotation":[0, 0, 0]},
        {"name":"knee_R_group_pivot","parent":"knee_R_group","location":ahhr["knee_R_group_pivot"],"rotation":[0, 0, 0]},
        {"name":"knee_R_locator","parent":"knee_R_group_pivot","location":[],"rotation":[0, 0, 0],"constraint":"knee_R_group_pivot"},
    ]


    #0.112832, -0.048875, 0.016036 - cursor location matching the head of ball_joint.R
    #0.113, 0.095

    prefix = "hhe_"
    prefix = ""

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        ob = bpy.data.objects.new( name, None )
        bpy.context.scene.objects.link( ob )

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        parent = prefix + hh_empty["parent"]
        print (parent)
        if parent != prefix:
            print ("adding "+ parent + " as parent for "+name)
            bpy.data.objects[name].parent = bpy.data.objects[parent]

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        location = hh_empty["location"]
        rotation = hh_empty["rotation"]
        if len(location) == 3:
            bpy.data.objects[name].location = Vector ((location[0],location[1],location[2]))
        if len(rotation) == 3:
            bpy.data.objects[name].rotation_euler = Vector ((radians(rotation[0]),radians(rotation[1]),radians(rotation[2])))        

    for hh_empty in hh_empties:
        name = prefix + hh_empty["name"]
        bpy.data.objects[name].hide = True
        bpy.data.objects[name].hide_select = True
        bpy.data.objects[name].hide_render = True
        #
        bpy.data.objects[name].lock_location[0] = True
        bpy.data.objects[name].lock_location[1] = True
        bpy.data.objects[name].lock_location[2] = True
        #
        bpy.data.objects[name].lock_rotation[0] = True
        bpy.data.objects[name].lock_rotation[1] = True
        bpy.data.objects[name].lock_rotation[2] = True
        #
        bpy.data.objects[name].lock_scale[0] = True
        bpy.data.objects[name].lock_scale[1] = True
        bpy.data.objects[name].lock_scale[2] = True    

    for hh_empty in ["foot_R_target01","leg_R_offset_group","ball_R_group","tiptoe_R_rotation_group_pivot","knee_R_group_pivot"]:
        name = prefix + hh_empty
        bpy.data.objects[name].hide = False
        bpy.data.objects[name].hide_select = False
        bpy.data.objects[name].hide_select = False
        bpy.data.objects[name].hide_render = True
        bpy.data.objects[name].lock_location[0] = False
        bpy.data.objects[name].lock_location[1] = False
        bpy.data.objects[name].lock_location[2] = False
        #
        bpy.data.objects[name].lock_rotation[0] = False
        bpy.data.objects[name].lock_rotation[1] = False
        bpy.data.objects[name].lock_rotation[2] = False
        #
        bpy.data.objects[name].lock_scale[0] = False
        bpy.data.objects[name].lock_scale[1] = False
        bpy.data.objects[name].lock_scale[2] = False       

    bpy.data.objects["tiptoe_R_rotation_ikHandle_target"].hide = False
    bpy.data.objects["tiptoe_R_rotation_ikHandle_target"].hide_select = False
    bpy.data.objects["tiptoe_R_rotation_ikHandle_pole"].hide = False
    bpy.data.objects["tiptoe_R_rotation_ikHandle_pole"].hide_select = False
    bpy.data.objects["tiptoe_R_rotation_ikHandle_pivot"].hide = False
    bpy.data.objects["tiptoe_R_rotation_ikHandle_pivot"].hide_select = False

    ############################################################################
    ob = bpy.data.objects["tiptoe_R_rotation_ikHandle_pivot"]

    tiptoe_R_rotation_ikHandle_pivot_constraint = None
    tiptoe_R_rotation_ikHandle_pivot_constraints = [ c for c in ob.constraints if c.type=='COPY_TRANSFORMS']

    if len(tiptoe_R_rotation_ikHandle_pivot_constraints)>0:
        print("Constraint exists!")
        tiptoe_R_rotation_ikHandle_pivot_constraint = tiptoe_R_rotation_ikHandle_pivot_constraints[0]
    else:
        print("Making a new constraint!")    
        tiptoe_R_rotation_ikHandle_pivot_constraint = ob.constraints.new('COPY_TRANSFORMS')
        tiptoe_R_rotation_ikHandle_pivot_constraint.target = bpy.data.objects["tiptoe_R_rotation_group_pivot"]

    ob.empty_draw_type = 'CIRCLE'
    ob.empty_draw_size = 0.05

    bpy.context.scene.update()

    #############################################################################

    # for hh_empty in hh_empties:
        # name = prefix + hh_empty["name"]
        # constraint = hh_empty.get("constraint")
        # if constraint != None:
            # constraint = prefix + constraint
            # print (constraint)
            # if constraint != prefix:
                # pivot_constraint = bpy.data.objects[name].constraints.new('PIVOT')
                # print ("adding "+ constraint + " as constraint for "+name)
                # pivot_constraint.target = bpy.data.objects[constraint]
                # pivot_constraint.rotation_range = 'ALWAYS_ACTIVE'
                # pivot_constraint.mute = True

    for hh_empty in hh_empties_draw:
        name = prefix + hh_empty["name"]
        draw = hh_empty.get("draw")
        size = hh_empty.get("size")
        bpy.data.objects[name].empty_draw_type = draw
        bpy.data.objects[name].empty_draw_size = size



    ik_for_bones = [
        {"bone":"knee_joint.R","target":"leg_R_ikHandle_target","pole_target":"knee_R_group_pivot","pole_angle":-90,"chain_length":2},
        {"bone":"ankle_joint.R","target":"tiptoe_R_ikHandle_target","pole_target":"tiptoe_R_ikHandle_pole","pole_angle":-90,"chain_length":1},
        {"bone":"ball_joint.R","target":"tiptoe_R_rotation_ikHandle_target","pole_target":"tiptoe_R_rotation_ikHandle_pole","pole_angle":-90,"chain_length":1},

    ]
    ob = bpy.data.objects["Armature"]
    for ik_bones in ik_for_bones:
        name = ik_bones["bone"]
        target = ik_bones["target"]
        pole_target = ik_bones["pole_target"]
        pole_angle = ik_bones.get("pole_angle")
        chain_length = ik_bones.get("chain_length")
        #
        ik_constraint = None
        ik_constraints = [ c for c in ob.pose.bones[name].constraints if c.type=='IK']
        if len(ik_constraints)>0:
            print("Constraint exists!")
            ik_constraint = ik_constraints[0]
        else:
            print("Making a new constraint!")    
            ik_constraint = ob.pose.bones[name].constraints.new('IK')
        ik_constraint.target = bpy.data.objects[target]
        ik_constraint.pole_target = bpy.data.objects[pole_target]
        ik_constraint.chain_count = chain_length
        ik_constraint.pole_angle = radians(pole_angle)  


    bpy.context.scene.update()




    ob = bpy.data.objects["leg_R_offset_group"]
    ob.location = Vector ( (0,0,0) )
    ob.rotation_euler = Vector ( ( radians(0), radians(0), radians(0)) )

    ob = bpy.data.objects["tiptoe_R_rotation_group_pivot"]
    ob.rotation_euler = Vector ( ( radians(0), radians(0), radians(0)) )

    bpy.context.scene.update()

