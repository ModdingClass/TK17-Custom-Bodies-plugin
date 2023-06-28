import os
import bpy
import mathutils
from math import radians
from math import degrees
from .dictionaries import *
from .utils import *
from . import globals

def get_fake_mesh_datablocks(mesh_name):
    ob = bpy.data.objects[mesh_name]
    me = ob.data
    m_axis_conversion = mathutils.Matrix(((1,0,0),(0,1,0),(0,0,-1)))
    m_axis_conversion.identity()
    
    vertex_array = []
    normal_array = []
    uv_array = []

    for i in range(len(me.vertices)):
        vertex_array.append(None)
        normal_array.append(None)
        uv_array.append(None)
    
    for vert in me.vertices:
        Vertex = vert.co * m_axis_conversion
        vertex_array[vert.index] = (Vertex.x,Vertex.y,Vertex.z)    
        normal_array[vert.index] = (vert.normal.x,vert.normal.y,vert.normal.z)    

    prim_length_array = []
    index_array = []
    for poly in me.polygons:#[0:10]:
        verts_count_in_poly = len(poly.vertices)
        prim_length_array.append(verts_count_in_poly)
        if (verts_count_in_poly==3):
            index_array.extend([poly.vertices[0],poly.vertices[1],poly.vertices[2]])
        else:
            index_array.extend([poly.vertices[0],poly.vertices[1],poly.vertices[2],poly.vertices[3]])



    uvlayer = me.uv_layers.active
    uvlname = uvlayer.name
    vertexdata0 = []     
    if len(me.uv_layers) == 0:
        pass
    else:
        for face in me.polygons:#[0:100]:
            for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                uvcoords = uvlayer.data[loop_idx].uv
                uvcoords = (uvcoords.x, uvcoords.y)
                vertexdata0.append(uvcoords)
                uv_array[vert_idx] = uvcoords
    return len(me.polygons),vertex_array,normal_array,uv_array,prim_length_array,index_array


def remove_fake_bones():
    _fakes = bpy.data.objects.get("_fakes")
    if _fakes:
        print ("_fakes found in scene")
        objs = bpy.data.objects
        for child in _fakes.children:
            objs.remove(objs[child.name], do_unlink=True)
        objs.remove(objs[_fakes.name], do_unlink=True)
    #
    armature = bpy.context.scene.objects['Armature']
    if armature:
        for pose_bone in armature.pose.bones:
            pose_bone.custom_shape = None
            pose_bone.use_custom_shape_bone_size = False




def getLocalNameForJoint(villaJointName):
    if villaJointName in joint_to_local_dict:
        return joint_to_local_dict[villaJointName]
    return "custom_"+ villaJointName


def add_fake_bones(obj_name):
    if bpy.data.objects.get("Armature") is None:
        ShowMessageBox("Can't find object: Armature", "Error", 'ERROR')
        return None
    #
    armature_object = bpy.data.objects.get("Armature")
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    boneSizeDict = {}  
    boneFlippedDict = {} 

    #we need to save edit bone length in boneSizeDict
    for editBone in bpy.data.armatures['Armature'].edit_bones:
        boneName = editBone.name
        #
        if ( ("_IK" in boneName) or ("_pole" in boneName) or ("_target" in boneName) or ("Empty" in boneName) or ("_fakes" == boneName) or ("_fake_target" in boneName) or ("axe" == boneName)):
            continue        
        if (villafyname(boneName) in animSkeletonValues):
            pass
        else :
            pass
            """
            if editBone.use_deform == True :
                villaname = villafyname(editBone.name)
                villaparentname = villafyname(editBone.parent.name)
                extraBones[villaname] = "custom_"+ villaname
            """
        #
        boneSizeDict[boneName] = editBone.length
        if editBone.get("isFlipped") is not None and editBone["isFlipped"] == True :
            boneFlippedDict[boneName] = True
        else:
            boneFlippedDict[boneName] = False
        print( boneName )
        #
    #
    #bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #print(bpy.context.space_data.text.filepath)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    print(directory)
    path_to_file = os.path.join(directory, obj_name+".obj")
    bpy.ops.import_scene.obj(filepath = path_to_file,split_mode='OFF')
    imported = bpy.context.selected_objects[0]
    print(imported.name)
    fake_mesh_datablocks={}
    prim_count,vertex_array,normal_array,uvdata,prim_length_array,index_array = get_fake_mesh_datablocks (imported.name)
    fake_mesh_datablocks["prim_count"] = prim_count
    fake_mesh_datablocks["vertex_array"] = vertex_array
    fake_mesh_datablocks["normal_array"] = normal_array
    fake_mesh_datablocks["uvdata"] = uvdata
    print("adding:")
    print(prim_length_array)
    print(index_array)
    fake_mesh_datablocks["prim_length_array"] = prim_length_array
    fake_mesh_datablocks["index_array"]    = index_array
    imported["fake_mesh_datablocks"] = fake_mesh_datablocks
    scn = bpy.context.scene
    parent = bpy.data.objects.new( "_fakes", None )
    scn.objects.link(parent)
    print("--------------------------")
    print("--------------------------")
    print("--------------------------")
    for key in sorted(boneSizeDict.keys()):
        if ( ("_IK" in key) or ("_pole" in key) or ("_target" in key) or ("Empty" in key) or ("_fakes" == key) or ("_fake_target" in key) or ("axe" == key)):
            continue
        if (key in 'tail_joint'):
            print("key: "+key)
        print (key, boneSizeDict[key])
        src_obj = bpy.data.objects[imported.name]
        new_obj = src_obj.copy()
        new_obj.data = src_obj.data.copy()
        new_obj.name = "cone_"+key
        new_obj.data.name = "cone_"+key
        new_obj.scale = new_obj.scale * boneSizeDict[key]
        new_obj["scale"] = new_obj.scale
        print("key {0}".format(key))
        print("key {0}".format(villafyname(key)))
        localTJoint = getLocalNameForJoint(villafyname(key))
        #print("key {0}".format(joint_to_local_dict[villafyname(key)]))
        #new_obj["localTJoint"] = joint_to_local_dict[villafyname(key)]
        print("key {0}".format(localTJoint))
        new_obj["localTJoint"] = localTJoint        
        new_obj.parent = parent
        scn.objects.link(new_obj)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = new_obj
        new_obj.select = True    
        new_obj.rotation_euler.z= radians(90)
        bpy.ops.object.transform_apply(rotation = True)        
        if boneFlippedDict[key] == True :
            new_obj.rotation_euler.y= radians(180)
            bpy.ops.object.transform_apply(rotation = True)
            new_obj["isFlipped"] = True 
        bpy.ops.object.transform_apply(scale = True)
        #
        #new_obj["fake_mesh_datablocks"] = fake_mesh_datablocks
    #
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')
    imported.select = True    # Blender 2.7x
    bpy.ops.object.delete() 
    #bpy.data.objects["Armature"].pose.bones["hip_joint.L"].custom_shape
    armature = bpy.context.scene.objects['Armature']
    for pose_bone in armature.pose.bones:
        if ("_IK" in pose_bone.name or "_pole" in pose_bone.name or "_target" in pose_bone.name or "Empty" in pose_bone.name or ("_fakes" == pose_bone.name)  or "_fake_target" in pose_bone.name or "axe" == pose_bone.name):
            continue        
        pose_bone.custom_shape = bpy.data.objects["cone_"+pose_bone.name]
        pose_bone.use_custom_shape_bone_size = False

    return fake_mesh_datablocks    



def merge_fake_bones_into_single_mesh_object(ignoreSomeBones, ignoreMaleBones): 
    if bpy.data.objects.get("_fakes") is None:
        ShowMessageBox("Can't find object: _fakes", "Error", 'ERROR')
        return None
    if bpy.data.objects.get("Armature") is None:
        ShowMessageBox("Can't find object: Armature", "Error", 'ERROR')
        return None
    #
    armature_object = bpy.data.objects.get("Armature")
    armature_object.select = True
    bpy.context.scene.objects.active = armature_object
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #
    armature_object = bpy.data.objects["Armature"]
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    #
    armature_matrix_world = armature_object.matrix_world
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

    shapes=[]
    parentBone = armature_object.data.edit_bones["root"]
    print_heir(parentBone)
    #
    for bone in my_bones:
        if ("_IK" in bone.name or "_pole" in bone.name or "_target" in bone.name or "Empty" in bone.name or "axe" in bone.name):
            continue
        if ignoreSomeBones == True:
            if ("_jointEnd" in bone.name and not bone.name in ["vagina_jointEnd.L","vagina_jointEnd.R", "spine_jointEnd", "neck_jointEnd", "lower_jaw_jointEnd", "forehead_jointEnd", "head_jointEnd"]):
                continue
            if ("toe_joint" in bone.name):
                continue
            if ("testicles" in bone.name):
                continue                
            if ("penis" in bone.name):
                continue 
            if ("finger" in bone.name and "_jointEnd." in bone.name):
                continue 
        if ignoreMaleBones == True:
            if  "penis_joint" in bone.name or "testicles_joint" in bone.name:
                continue                                   
        pb = armature_object.pose.bones.get(bone.name)
        shape = bpy.data.objects["cone_"+bone.name]
        shape.parent =bpy.data.objects["Armature"]
        shape.parent_type = 'BONE'
        shape.parent_bone = bone.name
        mpi = shape.matrix_parent_inverse
        ti = mathutils.Matrix.Translation([0, bone.length, 0]).inverted()
        shape.matrix_parent_inverse = mpi * ti
        shapes.append(shape.name) 

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.object.select_all(action='DESELECT')
    for obname in shapes:
        ob = bpy.data.objects[obname]
        ob.select = True
    bpy.context.scene.objects.active = bpy.data.objects[shapes[0]]
    bpy.ops.object.join()
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.transform_apply( location=True, rotation=True, scale=True )
    ob = bpy.context.scene.objects.active
    ob.name = "body_fakes"
    ob.data.name = "body_fakes"










