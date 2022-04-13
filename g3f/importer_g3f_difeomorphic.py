import bpy

from ..g3f.difeomorphic_workflow_convert_body import *
from ..tools_message_box import *
from ..utils_bpy import *


def import_g3f_difeomorphic() :
    isMyArmature = checkIfActiveObjectIs("ARMATURE","Genesis 3 Female")
    if (isMyArmature):
        pass
    else:
        ShowMessageBox("Genesis 3 Female Armature is not the active object","Error",icon="ERROR")
        return
    #
    activeObject = bpy.context.scene.objects.active
    bodyMesh = checkIfActiveObjectHasChild("MESH","Genesis 3 Female Mesh")
    gensMesh = checkIfActiveObjectHasChild("MESH","Genesis 3 Female Genitalia")
    if (bodyMesh != None):
        pass
    else:
        ShowMessageBox("Genesis 3 Female Mesh is not a child of the active object","Error",icon="ERROR")
        return
    #
    if (gensMesh != None):
        setActiveObject(gensMesh)
        activateObject(gensMesh)
        active_object = bpy.context.scene.objects.active
        bpy.ops.object.duplicate(linked=False)
        gensMeshCloned = bpy.context.scene.objects.active
        gensMeshCloned.parent = None
    #    
    if (bodyMesh != None):
        setActiveObject(bodyMesh)
        activateObject(bodyMesh)
        active_object = bpy.context.scene.objects.active
        bpy.ops.object.duplicate(linked=False)
        bodyMeshCloned = bpy.context.scene.objects.active
        bodyMeshCloned.parent = None
    #
    
    
    # no, we are not going to merge yet... we need to do that later
    #activateObject(gensMeshCloned) # activate this to maybe deselect all in scene first?
    #gensMeshCloned.select = True
    #bodyMeshCloned.select = True
    #setActiveObject(bodyMeshCloned)
    #if (True == False):
    #    return  
    #bpy.ops.daz.merge_geografts()
    activateObject(bodyMeshCloned)
    setActiveObject(bodyMeshCloned)
    """     #
    #setActiveObject(gensMesh)
    setActiveObject(bodyMesh)
    activateObject(bodyMesh)
    active_object = bpy.context.scene.objects.active
    bpy.ops.object.duplicate(linked=False)
    cloned_object = bpy.context.scene.objects.active
    setActiveObject(cloned_object)
    activateObject(cloned_object) 
    cloned_object.parent = None """
    #
    #activateObject(gensMesh)
    #if (1==1):
    #    return
    scene = bpy.context.scene
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    #
    # we need to make clones of the materials, otherwise we will overwrite on the stock materials assigned to difeomorphic body
    materials_list = bpy.context.object.material_slots.keys()
    for mat_name in materials_list:
        mat_index = bpy.context.object.material_slots.find(mat_name)
        bpy.context.object.active_material_index = mat_index
        active_material = bodyMeshCloned.active_material
        bodyMeshCloned.active_material = active_material.copy()
    #
    #reload the materials list
    materials_list = bpy.context.object.material_slots.keys()
    bpy.ops.object.editmode_toggle()  # we need to go in edit mode so we can select vertices from materials
    #
    #g3f body has too many vertices that we don't need, so we are going to select them based on materials and remove them
    for mat in materials_list:
        if ("Irises" in mat) or ("Cornea" in mat) or ("EyeMoisture" in mat) or ("Pupils" in mat) or ("Sclera" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()


    # this is the part where we should delete the selected vertices based on unwanted materials, but not going to do that because we are going to scale to zero and hide those unwanted vertices for now
    if (True == False):
        bpy.ops.object.mode_set(mode='EDIT')
        #
        #
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.mesh.select_all(action='DESELECT')
        #
        bpy.ops.object.editmode_toggle()  #back in object mode
    #
    #instead, lets try and scale them
    if (True == True):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.transform.resize(value=(0.0, 0.0, 0.0))
        bpy.ops.object.editmode_toggle()  #back in object mode
    #
    #
    #delete unused materials
    bpy.ops.object.mode_set(mode='OBJECT')
    ob = bpy.context.active_object
    mat_slots = {}
    for p in ob.data.polygons:
        mat_slots[p.material_index] = 1

    mat_slots = mat_slots.keys()

    for i in reversed(range(len(ob.material_slots))):
        if i not in mat_slots:
            bpy.context.scene.objects.active = ob
            ob.active_material_index = i
            bpy.ops.object.material_slot_remove()

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_mode(type="FACE")


    #making the head material
    materials_list = bpy.context.object.material_slots.keys()
    for mat in materials_list:
        if ("EyeSocket" in mat) or ("Ears" in mat) or ("Lips" in mat) or ("Face" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()

    #assign all faces to the body_head01 material
    bpy.ops.object.material_slot_assign()
    bpy.context.object.active_material.name = "body_head01"
    bpy.ops.mesh.select_all(action='DESELECT')

    #making the mouth material
    materials_list = bpy.context.object.material_slots.keys()
    for mat in materials_list:
        if ("Mouth" in mat) or ("Teeth" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()

    #assign all faces to the body_teeth01 material
    bpy.ops.object.material_slot_assign()
    bpy.context.object.active_material.name = "body_teeth01"
    bpy.ops.mesh.select_all(action='DESELECT')

    materials_list = bpy.context.object.material_slots.keys()
    for mat in materials_list:
        if ("Arms" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()        

    bpy.context.object.active_material.name = "body_hand01_L"
    bpy.ops.mesh.select_all(action='DESELECT')


    materials_list = bpy.context.object.material_slots.keys()
    for mat in materials_list:
        if ("Torso" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()    

    bpy.context.object.active_material.name = "body_main_upper"
    bpy.ops.mesh.select_all(action='DESELECT')

    materials_list = bpy.context.object.material_slots.keys()
    for mat in materials_list:
        if ("Toenails" in mat) or ("Legs" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()    

    bpy.context.object.active_material.name = "body_foot_L"
    bpy.ops.object.material_slot_assign()
    bpy.ops.mesh.select_all(action='DESELECT')

    materials_list = bpy.context.object.material_slots.keys()
    for mat in materials_list:
        if ("Genitalia" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()    

    bpy.context.object.active_material.name = "body_genital01"
    bpy.ops.mesh.select_all(action='DESELECT')

    for mat in materials_list:
        if ("Eyelashes" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()    

    bpy.context.object.active_material.name = "body_eyelash01"
    bpy.ops.mesh.select_all(action='DESELECT')

    for mat in materials_list:
        if ("Fingernails" in mat):
            mat_index = bpy.context.object.material_slots.find(mat)
            bpy.context.object.active_material_index = mat_index
            bpy.ops.object.material_slot_select()    

    #assign all faces to the Fingernails material
    bpy.ops.object.material_slot_assign()
    bpy.context.object.active_material.name = "body_fingernails_L.001" #.001 because body_fingernails_L would be otherwise be locked
    bpy.ops.mesh.select_all(action='DESELECT')


    bpy.ops.object.mode_set(mode='OBJECT')

    #delete unused materials
    ob = bpy.context.active_object
    mat_slots = {}
    for p in ob.data.polygons:
        mat_slots[p.material_index] = 1

    mat_slots = mat_slots.keys()
     
    for i in reversed(range(len(ob.material_slots))):
        if i not in mat_slots:
            bpy.context.scene.objects.active = ob
            ob.active_material_index = i
            bpy.ops.object.material_slot_remove()




    game_material_names = [
    'body_teeth01',
    'body_leg_lower_R',
    'body_leg_lower_L',
    'body_main_lower',
    'body_arm_lower_R',
    'body_arm_lower_L',
    'body_fingernails_R',
    'body_arm_upper_R',
    'body_arm_upper_L',
    'body_leg_upper_R',
    'body_leg_upper_L',
    'body_foot_L',
    'body_hand01_L',
    'body_genital01',
    'body_head01',
    'body_main_upper',
    'body_hand01_R',
    'body_foot_R',
    'body_fingernails_L',
    'body_eyelash01']

    if (True == False):
        return
    #refresh the materials_list array
    current_materials_list = bpy.context.object.material_slots.keys()
    print ("size of current_materials_list:{0}".format(len(current_materials_list)))
    #
    for i,game_mat_name in enumerate(game_material_names): 
        print ("current index {0} and size of current_materials_list:{1}".format(i,len(current_materials_list)))
        mat = None
        for existing_mat in current_materials_list:
            if (game_mat_name in existing_mat):
                # Get material
                print("Found material: {0} in current_materials_list as {1}".format(game_mat_name,existing_mat))
                mat = bpy.data.materials.get(existing_mat)
        #if it doesnt exist, create it.
        if mat is None:
            # create material
            print("Material: {0} not found, lets create it".format(game_mat_name))
            mat = bpy.data.materials.new(name=game_mat_name)
            print("\t Material added as : {0}".format(mat.name))
            #assign material
            ob.data.materials.append(mat)    
        #
        #             
        if (mat.name != game_mat_name):
            print("\t Material should be renamed as : {0}".format(game_mat_name))
            mat.name = game_mat_name
            print("\t Material new name is : {0}".format(mat.name))
        #otherwise
    """         else:
            #mat.name = target_mat_name
            #get material
            #mat = bpy.data.materials.get(target_mat_name)
            found = False
            for idx, m in enumerate(ob.material_slots):
                if (m.name == game_mat_name):
                    bpy.context.object.active_material_index = idx
                    bpy.ops.object.material_slot_select()
                    found = True
                    break
            if (found == False):
                ob.data.materials.append(mat) """
    #
    if (True == False):
        return






    ob = bpy.context.active_object
    for j in range (len(ob.material_slots)):
        for i in range (len(ob.material_slots)-1):
            ob.active_material_index = i
            tempStr = ob.active_material.name
            ob.active_material_index = i+1
            if ob.active_material.name.split("_")[-1] < tempStr.split("_")[-1]:
                bpy.ops.object.material_slot_move(direction='UP')




    ob.active_material_index = 0
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')
    bpy.ops.object.material_slot_move(direction='DOWN')

    bpy.data.materials["body_teeth01"]["localname"]="local_custommouth_RS"
    bpy.data.materials["body_teeth01"]["objectname"]="body_teeth01_SG"




    body_subdiv_cage_object = bpy.context.scene.objects.get("body_subdiv_cage")

    if body_subdiv_cage_object:
        print ("\"body_subdiv_cage\" object found in scene, using original name")
    else:
        ob.name= "body_subdiv_cage"
        ob.data.name = "M_body_subdiv_cage"

    
    #lets flip eyelashes normals
    eyelashes_faces_that_needs_to_have_flipped_normals = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197]
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.object.mode_set(mode='OBJECT')
    for i in eyelashes_faces_that_needs_to_have_flipped_normals:
        ob.data.polygons[i].select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.flip_normals() 
    bpy.ops.object.mode_set(mode='OBJECT')

    ob.data.uv_layers[0].name = "UVMap"
    #lets add this property
    ob.data["json_sk_exporter"] = "bbb_eye_L_morph,bbb_eye_R_morph,bbb_vagfix_morph"



