#logic behind is:
#right hand is good, left leg is good, etc... (everything which is not flipped)
#but we can't symmetrize the armature because it has a -90 z rotation
#so first apply rotation, then symmetrize in groups (because we want to set right hand values to left hand and left leg to right leg : not flipped to flipped) then only then!!! check x-axis mirror 
#adjust armature to body
#remove check x-axis mirror option
#select all edit bones and rotate 90
#in object mode set rotation back to 90
#corect rolls for flipped bones (180 + value of non flipped
#now can finally export

import bpy
import mathutils
import math

from mathutils import Vector
from mathutils import Matrix
from math import radians

from .dictionaries import *
from .correct_final_rolls import *
from .ik_tools import *


def regenerate_empties(armature_object):
    center_list = ["spine_joint01","spine_joint02","spine_joint03","spine_joint04","spine_jointEnd","neck_joint01","neck_jointEnd","head_joint01","head_joint02","head_jointEnd"]
    #
    #
    bpy.context.scene.objects.active = armature_object
    bpy.ops.object.duplicate(linked=False)
    clone = bpy.context.scene.objects.active
    fix_rolls(clone)
    #
    #
    #Must make armature active and in edit mode to create a bone
    #bpy.context.scene.objects.active = armature_object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #
    armature_matrix_world = clone.matrix_world
    #
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
    parentBone = clone.data.edit_bones["root"]
    print_heir(parentBone)
    #
    for bone in my_bones:
        #print ("bone: " + bone.name)
        if "_target" in bone.name or "_pole" in bone.name or "axe" == bone.name:
            continue
        ob = bpy.data.objects.new( "_"+ctkToVillaDict[bone.name], None )
        ob.rotation_mode = 'YZX'
        if bone.name != "root":
            ob.parent = bpy.data.objects[ "_"+ctkToVillaDict[bone.parent.name]]    
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
        #if (bone.name == "root"):
        #    ob.location.x    = 0    
        #if ctkToVillaDict[bone.name] in center_list:
        #    ob.location.x    = 0
        #ob.show_axis = True        
        bpy.context.scene.objects.link( ob )
    #  
    #localCo, worldCo, distance = getClosestPointFromBoneProjection("Armature", "elbow_joint.R", "wrist_joint.R")
	#eb = bpy.data.armatures['Armature'].edit_bones
    bone_ankle_joint_L = clone.data.edit_bones["ankle_joint.L"]
    bone_knee_joint_L = clone.data.edit_bones["knee_joint.L"]
    line_a = bone_knee_joint_L.head
    line_b = bone_knee_joint_L.tail
    plane_co = bone_ankle_joint_L.head
    plane_no = bone_ankle_joint_L.y_axis
	#	
    #bone_knee_joint_L_matrix = bone_knee_joint_L.matrix
    #bone_knee_joint_L_matrix.translation = bone_knee_joint_L.tail
    #bone_knee_joint_L_matrix_world = armature_matrix_world * bone_knee_joint_L_matrix
    #ob = bpy.data.objects.new( "_kneetail_L_joint", None )
    #ob.parent = bpy.data.objects[ "_hip_L_joint"]    
    #ob.matrix_world = bone_knee_joint_L_matrix_world
    #ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    #ob.matrix_parent_inverse.identity()
    #bpy.context.scene.objects.link( ob )
    #line_a (mathutils.Vector) – First point of the first line
    #line_b (mathutils.Vector) – Second point of the first line
    #plane_co (mathutils.Vector) – A point on the plane
    #plane_no (mathutils.Vector) – The direction the plane is facing
    # 
    #bone_knee_joint_R = clone.data.edit_bones["knee_joint.R"]
    #leg_target_L
    if True == True and "leg_target.L" in clone.data.edit_bones.keys() :
        bone = clone.data.edit_bones["leg_target.L"] #
        ob = bpy.data.objects.new( "_leg_target_L", None )
        ob.rotation_mode = 'YZX'
        ob.parent = bpy.data.objects[ "_knee_L_joint"]  
        ob.matrix_world = armature_matrix_world * bone.matrix
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()    
        bpy.context.scene.objects.link( ob )
    #
    #leg_target_R
    if True == True and "leg_target.R" in clone.data.edit_bones.keys() :
        bone = clone.data.edit_bones["leg_target.R"] #
        ob = bpy.data.objects.new( "_leg_target_R", None )
        ob.rotation_mode = 'YZX'
        ob.parent = bpy.data.objects[ "_knee_R_joint"]  
        ob.matrix_world = armature_matrix_world * bone.matrix
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()    
        bpy.context.scene.objects.link( ob )
    #    
    #leg_pole_L
    #
    if True == True and "leg_pole.L" in clone.data.edit_bones.keys() :
        bone = clone.data.edit_bones["leg_pole.L"] #
        ob = bpy.data.objects.new( "_leg_pole_L", None )
        ob.rotation_mode = 'YZX'
        ob.parent = bpy.data.objects[ "_leg_target_L"]  
        ob.matrix_world = armature_matrix_world * bone.matrix
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()    
        bpy.context.scene.objects.link( ob )       
    #
    #leg_pole_R    
    if True == True and "leg_pole.R" in clone.data.edit_bones.keys() :
        bone = clone.data.edit_bones["leg_pole.R"] #
        ob = bpy.data.objects.new( "_leg_pole_R", None )
        ob.rotation_mode = 'YZX'
        ob.parent = bpy.data.objects[ "_leg_target_R"]  
        ob.matrix_world = armature_matrix_world * bone.matrix
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()    
        bpy.context.scene.objects.link( ob )       
    #    
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
    if True == True:
        # setting up _ball_L_ikEffector
        ankle_L_joint = bpy.data.objects[ "_ankle_L_joint"]
        ankle_R_joint = bpy.data.objects[ "_ankle_R_joint"]
        ikEffector,ikHandle = getIKValues(clone.name,"ankle_joint.L","ball_joint.L")
        #
        ob = bpy.data.objects.new( "_ball_L_ikEffector", None )
        ob.rotation_mode = 'YZX'
        ob.parent = ankle_L_joint
        ob.matrix_world =  ankle_L_joint.matrix_world
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()       
        # Define the translation we want to perform in local space (after rotation) # we actually move down the local Y axis of the ankle joint
        trans_local = Vector((0, ikEffector.x, 0))
        # Convert the local translation to global with the 3x3 rotation matrix of our object
        trans_world = ob.matrix_world.to_3x3() * trans_local
        # Apply the translation
        ob.matrix_world.translation += trans_world
        bpy.context.scene.objects.link( ob )
        #
        #setting up PoleVector
        if True == True :
            ikEffector,ikHandle = getIKValues(clone.name,"ankle_joint.L","ball_joint.L")
            ob = bpy.data.objects.new( "_tiptoe_L_ikHandle_pole", None )
            ob.rotation_mode = 'YZX'
            ob.parent = ankle_L_joint
            ob.matrix_world =  ankle_L_joint.matrix_world
            ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
            ob.matrix_parent_inverse.identity()
            # Define the translation we want to perform in local space (after rotation) we actually move down the local Y axis of the ankle joint and down a bit
            trans_local = Vector((0, ikEffector.x, -0.1))
            # Convert the local translation to global with the 3x3 rotation matrix of our object
            trans_world = ob.matrix_world.to_3x3() * trans_local
            # Apply the translation
            ob.matrix_world.translation += trans_world
            bpy.context.scene.objects.link( ob )
            #
            # 
            ikEffector,ikHandle = getIKValues(clone.name,"ankle_joint.R","ball_joint.R")
            ob = bpy.data.objects.new( "_tiptoe_R_ikHandle_pole", None )
            ob.rotation_mode = 'YZX'
            ob.parent = ankle_R_joint
            ob.matrix_world =  ankle_R_joint.matrix_world
            ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
            ob.matrix_parent_inverse.identity()
            # Define the translation we want to perform in local space (after rotation) we actually move down the local Y axis of the ankle joint and down a bit
            #this is tricky because of the flipped bone that is transffered into the empty
            # maybe this should be calculated directly from the edit bone, not from the empty 
            trans_local = Vector((0, -1 * ikEffector.x, 0.1))
            # Convert the local translation to global with the 3x3 rotation matrix of our object
            trans_world = ob.matrix_world.to_3x3() * trans_local
            # Apply the translation
            ob.matrix_world.translation += trans_world
            bpy.context.scene.objects.link( ob )            
        #
        #setting up _toe_L_ikEffector
        ball_L_joint = bpy.data.objects[ "_ball_L_joint"]
        ikEffector,ikHandle = getIKValues(clone.name,"ball_joint.L","toe_joint.L")
        #
        ob = bpy.data.objects.new( "_toe_L_ikEffector", None )
        ob.rotation_mode = 'YZX'
        ob.parent = ball_L_joint
        ob.matrix_world =  ball_L_joint.matrix_world
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()       
        # Define the translation we want to perform in local space (after rotation) # we actually move down the local Y axis of the ankle joint
        trans_local = Vector((0, ikEffector.x, 0))
        # Convert the local translation to global with the 3x3 rotation matrix of our object
        trans_world = ob.matrix_world.to_3x3() * trans_local
        # Apply the translation
        ob.matrix_world.translation += trans_world
        bpy.context.scene.objects.link( ob )
        #
        #setting up _toe_R_ikEffector
        ball_R_joint = bpy.data.objects[ "_ball_R_joint"]
        ikEffector,ikHandle = getIKValues(clone.name,"ball_joint.R","toe_joint.R")
        #
        ob = bpy.data.objects.new( "_toe_R_ikEffector", None )
        ob.rotation_mode = 'YZX'
        ob.parent = ball_R_joint
        ob.matrix_world =  ball_R_joint.matrix_world
        ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
        ob.matrix_parent_inverse.identity()       
        # Define the translation we want to perform in local space (after rotation) # we actually move down the local Y axis of the ankle joint
        #the bone is flipped, the empty is backwards, so we need to multiply with -1 
        trans_local = Vector((0, -1 * ikEffector.x, 0))
        # Convert the local translation to global with the 3x3 rotation matrix of our object
        trans_world = ob.matrix_world.to_3x3() * trans_local
        # Apply the translation
        ob.matrix_world.translation += trans_world
        bpy.context.scene.objects.link( ob )        
    #
    #    
    #
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.delete() 
    bpy.ops.object.select_all(action='DESELECT')
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    armature_object.select = True





def regenerate_empties_hands(armature_object):
    bpy.context.scene.objects.active = armature_object
    clone = bpy.context.scene.objects.active
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #
    armature_matrix_world = clone.matrix_world
    #
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
    parentBone = clone.data.edit_bones["root"]
    print_heir(parentBone)
    #
    editBone = bpy.context.object.data.edit_bones.new("wrist_fake_parent.R")
    editBone.head = Vector( (0,0,0) )
    editBone.tail = Vector( (-1,0,0) )
    editBone.roll = radians(-180)
    editBone.use_deform = False
    bpy.context.scene.update()
    #
    ob = bpy.data.objects.new( "_wrist_fake_parent_R", None)
    ob.rotation_mode = 'YZX'
    ob.parent = bpy.data.objects["_root"]
    ob.matrix_world = armature_matrix_world * editBone.matrix       
    ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    ob.matrix_parent_inverse.identity()
    bpy.context.scene.objects.link( ob )
    clone.data.edit_bones.remove(editBone)
    #
    bone = clone.data.edit_bones["wrist_joint.R"]
    ob = bpy.data.objects.new( "_wrist_fake_joint_R", None)
    ob.rotation_mode = 'YZX'
    ob.parent = bpy.data.objects["_wrist_fake_parent_R"]
    ob.matrix_world = armature_matrix_world * bone.matrix       
    ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    ob.matrix_parent_inverse.identity()
    bpy.context.scene.objects.link( ob )
    #
    editBone = bpy.context.object.data.edit_bones.new("wrist_fake_parent.L")
    editBone.head = Vector( (0,0,0) )
    editBone.tail = Vector( (1,0,0) )
    editBone.roll = radians(+180)
    editBone.use_deform = False
    bpy.context.scene.update()
    #
    ob = bpy.data.objects.new( "_wrist_fake_parent_L", None)
    ob.rotation_mode = 'YZX'
    ob.parent = bpy.data.objects["_root"]
    ob.matrix_world = armature_matrix_world * editBone.matrix       
    ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    ob.matrix_parent_inverse.identity()
    bpy.context.scene.objects.link( ob )
    clone.data.edit_bones.remove(editBone)
    #
    bone = clone.data.edit_bones["wrist_joint.L"]
    ob = bpy.data.objects.new( "_wrist_fake_joint_L", None)
    ob.rotation_mode = 'YZX'
    ob.parent = bpy.data.objects["_wrist_fake_parent_L"]
    ob.matrix_world = armature_matrix_world * bone.matrix       
    ob.matrix_basis = ob.matrix_parent_inverse * ob.matrix_basis
    ob.matrix_parent_inverse.identity()
    bpy.context.scene.objects.link( ob )


    




def regenerate_empties_ik(armature_object):
    bpy.context.scene.objects.active = armature_object
    clone = bpy.context.scene.objects.active
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #
    armature_matrix_world = clone.matrix_world
    #
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
    parentBone = clone.data.edit_bones["root"]
    print_heir(parentBone)
    #
    #arm_pole.L
    pole_z_distance = -0.3
    bone_shoulder_joint = clone.data.edit_bones["shoulder_joint.L"] #""
    bone_matrix = bone_shoulder_joint.matrix.copy()
    local_translation = Matrix.Translation((0.0, bone_shoulder_joint.length, pole_z_distance))
    bone_matrix *= local_translation  
    world_coords = clone.matrix_world * bone_matrix.translation
    #bpy.context.scene.cursor_location = world_coords
    ob = bpy.data.objects.new( "_arm_pole_L", None )
    ob.rotation_mode = 'YZX'
    ob.location = world_coords
    ob.parent = bpy.data.objects[ "_root"]  
    ob.matrix_parent_inverse = ob.parent.matrix_world.inverted()
    bpy.context.scene.objects.link( ob ) 
    #arm_pole.R
    bone_shoulder_joint = clone.data.edit_bones["shoulder_joint.R"] #""
    bone_matrix = bone_shoulder_joint.matrix.copy()
    local_translation = Matrix.Translation((0.0, bone_shoulder_joint.length, pole_z_distance))
    bone_matrix *= local_translation  
    world_coords = clone.matrix_world * bone_matrix.translation
    #bpy.context.scene.cursor_location = world_coords
    ob = bpy.data.objects.new( "_arm_pole_R", None )
    ob.rotation_mode = 'YZX'
    ob.location = world_coords
    #mw = ob.matrix_world.copy()
    ob.parent = bpy.data.objects[ "_root"]  
    ob.matrix_parent_inverse = ob.parent.matrix_world.inverted()
    bpy.context.scene.objects.link( ob )     
    #
    #knee_pole.L
    pole_z_distance = -0.5
    bone_hip_joint = clone.data.edit_bones["hip_joint.L"] #""
    bone_matrix = bone_hip_joint.matrix.copy()
    local_translation = Matrix.Translation((0.0, bone_hip_joint.length, pole_z_distance))
    bone_matrix *= local_translation  
    world_coords = clone.matrix_world * bone_matrix.translation
    #bpy.context.scene.cursor_location = world_coords
    ob = bpy.data.objects.new( "_knee_pole_L", None )
    ob.rotation_mode = 'YZX'
    ob.location = world_coords
    ob.parent = bpy.data.objects[ "_root"]  
    ob.matrix_parent_inverse = ob.parent.matrix_world.inverted()
    bpy.context.scene.objects.link( ob )    
    #
    #knee_pole.R
    bone_hip_joint = clone.data.edit_bones["hip_joint.R"] #""
    bone_matrix = bone_hip_joint.matrix.copy()
    local_translation = Matrix.Translation((0.0, bone_hip_joint.length, pole_z_distance))
    bone_matrix *= local_translation  
    world_coords = clone.matrix_world * bone_matrix.translation
    #bpy.context.scene.cursor_location = world_coords
    ob = bpy.data.objects.new( "_knee_pole_R", None )
    ob.rotation_mode = 'YZX'
    ob.location = world_coords
    ob.parent = bpy.data.objects[ "_root"]  
    ob.matrix_parent_inverse = ob.parent.matrix_world.inverted()
    bpy.context.scene.objects.link( ob )      
    #
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.select_all(action='DESELECT')
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    armature_object.select = True

