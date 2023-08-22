import bpy, mathutils
import re
from collections import OrderedDict
import winsound
import ctypes
from ctypes import wintypes
import os
import time
from .utils import *
from .dictionaries import *
from .dictionary_shapekeys import *
from .dictionary_vertexgroups import *
from .dictionary_materials import *
from .tools_message_box import *
from .helper_material_lists_lookup import *

def blendifyname(bonename) :
    if '_L_' in bonename :
        rem = '_L_'
        ext = '.L'
    elif '_R_' in bonename :
        rem = '_R_'
        ext = '.R'
    else : return bonename
    realname = bonename
    i = realname.index(rem)
    bonename = realname[0:i]+'_'+realname[i+3:] + ext
    return bonename

def get_weights(obj, vgName):
    VG = obj.vertex_groups[vgName]
    for i, v in enumerate(obj.data.vertices):
        for g in v.groups:
            #print (g.group)
            if g.group == VG.index:
                yield (i, g.weight)
                break

def getLastUsageForVertexGroup():
    maxUsage = 0
    for vertexGroup in vertexGroupsArray:
        #name = vertexGroup[0]
        #ob_name = vertexGroup[1]
        #lname_tjoint = vertexGroup[2]
        #lname_vertexdata = vertexGroup[3]
        usage = vertexGroup[4]
        if int(usage)>=maxUsage:
            maxUsage = int(usage)
    return maxUsage

def getLinkedInfoForVertexGroup(name):
    for vertexGroup in vertexGroupsArray: 
        blender_name = vertexGroup[0]
        villa_name = vertexGroup[1]
        lname_tjoint = vertexGroup[2]
        lname_vertexdata = vertexGroup[3]
        usage = vertexGroup[4]
        if name == villa_name:
            return blender_name, villa_name, lname_tjoint, lname_vertexdata
    blendifiedName = blendifyname(name)
    return blendifiedName, name, "custom_"+name, "custom_"+name+"_vd"


def createLinkedInfoForCustomVertexGroup(name, last_usage):
    villafiedName = villafyname(name)
    return name, villafiedName, "custom_"+villafiedName, "custom_"+villafiedName+"_vd", last_usage

def operator_exists(idname):
    from bpy.ops import op_as_string
    try:
        op_as_string(idname)
        return True
    except:
        return False

def deselect_all_objects():
    for ob in bpy.context.selected_objects:
        ob.select = False

def export_body(exportfolderpath, bodyNo, includeGeograftsOnExport) :
    # a ton of boilerplate checks comes next
    if bpy.data.objects.get("body_subdiv_cage") is None:
        ShowMessageBox("Can't find object: body_subdiv_cage", "Error", 'ERROR')
        return None

    if bpy.data.objects["body_subdiv_cage"].hide :
        ShowMessageBox("'body_subdiv_cage' object is not visible!", "Error", 'ERROR')
        return None

    exportfolderpath = os.path.join(exportfolderpath,"")    
    if not os.path.exists(exportfolderpath+"bsBlocks"):
        os.makedirs(exportfolderpath+"bsBlocks")

    hiddenStatusGeografts = {}
    mergeGeografts = []
    anatomies = []
    ob = bpy.data.objects["body_subdiv_cage"]
    ob.select = True
    bpy.context.scene.objects.active = ob
    
    if not includeGeograftsOnExport:
        pass
    else:
        if ( operator_exists("daz.merge_geografts_fast") or operator_exists("daz.merge_geografts") ):
            pass
        else:
            ShowMessageBox("'Include Geografts' is checked, but can't find `modded` Difeomorphic addon for Blender", "Error", 'ERROR')
            return None
        if ob.data.get("mergeGeografts") is None:
                ShowMessageBox("'Include Geografts' is checked, but you are missing 'mergeGeografts' property in data block Custom Properties", "Error", 'ERROR')
                return None
        if len(ob.data["mergeGeografts"].strip()) == 0 :
                ShowMessageBox("'Include Geografts' is checked, but empty 'mergeGeografts' in data block Custom Properties", "Error", 'ERROR')
                return None
        mergeGeografts = ob.data["mergeGeografts"].split(",")
        if len(mergeGeografts)==0:
            ShowMessageBox("'Include Geografts' is checked, but empty 'mergeGeografts' in data block Custom Properties", "Error", 'ERROR')
            return None
        else:
            for geo in mergeGeografts:
                ob = bpy.data.objects.get(geo)
                if ob is None:
                    ShowMessageBox("'Include Geografts' is checked, but the object with name: "+geo+" is missing", "Error", 'ERROR')    
                    return None
                if ob.type != 'MESH':
                    ShowMessageBox("'Include Geografts' is checked, but the object with name: "+geo+" is not a Mesh type", "Error", 'ERROR')    
                    return None       
                hiddenStatusGeografts[ob.name] = ob.hide      
                if ob.hide :
                    ob.hide = False # we need to show it
                    #ShowMessageBox("Geograft object '"+ ob.name +"' is not visible!", "Error", 'ERROR')
                    #return None                

    if includeGeograftsOnExport:
        deselect_all_objects()       
        ob = bpy.data.objects["body_subdiv_cage"]
        ob.select = True
        bpy.context.scene.objects.active = ob
        bpy.ops.object.duplicate(linked=False)
        bodyClone = bpy.context.scene.objects.active
        bodyClone.name = "body_subdiv_cage_delete_me_after_export"
        #
        for geo in mergeGeografts:
            deselect_all_objects()
            ob = bpy.data.objects[geo]
            ob.select = True
            bpy.context.scene.objects.active = ob
            bpy.ops.object.duplicate(linked=False)
            geoClone = bpy.context.scene.objects.active
            geoClone.parent = bodyClone
            anatomies.append(geoClone)
            bpy.data.objects[geo].hide = hiddenStatusGeografts[ob.name] # we need to restore the hidden status
        #
        deselect_all_objects()
        #
        for geo in anatomies:
            geo.select = True
            bpy.context.scene.objects.active = geo        
        bodyClone.select=True
        bpy.context.scene.objects.active = bodyClone
        bodyClone.select=True
        if ( operator_exists("daz.merge_geografts_fast") ):
            bpy.ops.daz.merge_geografts_fast()
        else: 
            bpy.ops.daz.merge_geografts()
    
    
    ob = bpy.context.scene.objects.active

    #if True==True:
    #    return None
    me = ob.data
    if len(me.uv_layers) == 0:
        ShowMessageBox("Object: body_subdiv_cage has no UV Map", "Error", 'ERROR')
        return None
    uvlayer = me.uv_layers.active
    uvlname = uvlayer.name
    if uvlname not in ["UVMap","UVLayer_local_635_65536"]:
        ShowMessageBox("UV Map not named UVMap or UVLayer_local_635_6553", "Error", 'ERROR')
        return None    
    uvlname = uvlname.split("_")
    uvllocal = "local_635"#uvlname[-3]+"_"+uvlname[-2]
    uvlusage = "65536"#uvlname[-1]


    edgepointarray = []
    vertarray = []
    faceedgearray = []
    edgepointkeys = []
    faceshaderarray = []
    facelengtharray = []
    faceattrarray = []
    vertexdata0 = [] 
    tic = time.perf_counter()

    for i in range(len(me.vertices)):
        vertarray.append(None)
        
    m_axis_conversion = mathutils.Matrix(((1,0,0),(0,0,-1),(0,1,0)))
    for vert in me.vertices:
        Vertex = vert.co * m_axis_conversion
        vertarray[vert.index] = (Vertex.x,Vertex.y,Vertex.z)

    toc = time.perf_counter()
    print("*********************************** finished vertarray in "+ "{:0.4f}".format(toc - tic)+" seconds")

    tic = time.perf_counter()
    for edge in me.edges:
        edgepoints = [vert for vert in edge.vertices]
        for edgepoint in edgepoints:
            edgepointarray.append(edgepoint)
        edgepointkeys.append(edge.key)
        
    edgepointkeys_dictionary={}
    for idx,edgepointkey in enumerate(edgepointkeys):
        edgepointkeys_dictionary[edgepointkey] = idx
        
    toc = time.perf_counter()
    print("*********************************** finished edgepointarray in "+ "{:0.4f}".format(toc - tic)+" seconds")
    #no longer relevant: materials are kinda hardcoded, so make sure the material list blender is only shuffled, but don't exced the number of materials unless the hardcoded part is also changed
    #blender_mat_dict = { i: mat.name        for i, mat in enumerate(ob.data.materials)}
    #tk17_mat_dict = { mat[0]: i        for i, mat in enumerate(stock_materials)}
    
    tic = time.perf_counter()
    #new calling build_materials_list_looup will send data in global arrray lookup_materials defined in helper_material_lists_lookup.py
    lookup_materials, output_materials, indexed_output_materials = build_materials_list_lookup() # lookup_materials[] and output_materials dict is now populated
    #
    pyblock_MeshData_ShaderArray = []
    for mat in output_materials:
        pyblock_MeshData_ShaderArray.append("RenderShader :"+output_materials[mat]['localname'])
    

    for poly in me.polygons:
        edgekeys = poly.edge_keys
        #faceshaderarray.append(poly.material_index)
        #faceshaderarray.append(tk17_mat_dict[blender_mat_dict[poly.material_index]])
        faceshaderarray.append(lookup_materials[poly.material_index])
        facelengtharray.append(len(poly.vertices))
    toc = time.perf_counter()
    print("*********************************** finished materials in "+ "{:0.4f}".format(toc - tic)+" seconds")
    
    tic = time.perf_counter()
    polyind = 0
    for poly in me.polygons:#[0:100]:
        edgekeys = poly.edge_keys
        face = []
        for i in range(len(poly.vertices)): #
            loop = poly.loop_indices[i]
            uvcoords = uvlayer.data[loop].uv
            uvcoords = (uvcoords.x, uvcoords.y)
            vertexdata0.append(uvcoords)
    
    toc = time.perf_counter()
    print("*********************************** finished UVs in "+ "{:0.4f}".format(toc - tic)+" seconds")
    
    #print ('#####')
    #print (i)
    #print (vertindex)
    #print (poly.vertices[i])
    
    tic = time.perf_counter()
    polyind = 0
    for poly in me.polygons:#[0:10]:
        edgekeys = poly.edge_keys
        face = []
        for i in range(len(poly.vertices)): #
            vertindex = poly.vertices[i]
            edgekey = edgekeys[i]
            #index = edgepointkeys.index(edgekey) # this was fucking slow!!!!
            index = -1
            try:
                index = edgepointkeys_dictionary[edgekey]
                if vertindex == edgepointarray[index * 2]:
                    faceedgearray.append(index*2)
                else:
                    faceedgearray.append(index*2+1)                
            except:
                print(vertindex, edgekey)
            #
            faceattrarray.append(polyind)
            polyind += 1

    toc = time.perf_counter()
    print("*********************************** finished looping polygons in "+ "{:0.4f}".format(toc - tic)+" seconds")
    
    tic = time.perf_counter()
    vg_dict =OrderedDict()
    #vertexGroupsArray = ['root_local_70_local_636_524288', 'spine_joint01_local_71_local_637_524289', 'spine_joint02_local_72_local_638_524290', 'spine_joint03_local_73_local_639_524291', 'spine_joint04_local_74_local_640_524292', 'spine_jointEnd_local_75_local_641_524293', 'neck_joint01_local_76_local_642_524294', 'neck_jointEnd_local_77_local_643_524295', 'head_joint01_local_78_local_644_524296', 'head_joint02_local_79_local_645_524297', 'lower_jaw_joint01_local_80_local_646_524298', 'lower_jaw_jointEnd_local_81_local_647_524299', 'chin_joint01_local_82_local_648_524300', 'chin_jointEnd_local_83_local_649_524301', 'lower_lip_R_joint01_local_84_local_650_524302', 'lower_lip_R_joint02_local_85_local_651_524303', 'lower_lip_R_joint03_local_86_local_652_524304', 'lower_lip_R_jointEnd_local_87_local_653_524305', 'lower_lip_L_joint01_local_88_local_654_524306', 'lower_lip_L_joint02_local_89_local_655_524307', 'lower_lip_L_joint03_local_90_local_656_524308', 'lower_lip_L_jointEnd_local_91_local_657_524309', 'upper_lip_L_joint01_local_92_local_658_524310', 'upper_lip_L_joint02_local_93_local_659_524311', 'upper_lip_L_joint03_local_94_local_660_524312', 'upper_lip_L_jointEnd_local_95_local_661_524313', 'upper_lip_R_joint01_local_96_local_662_524314', 'upper_lip_R_joint02_local_97_local_663_524315', 'upper_lip_R_joint03_local_98_local_664_524316', 'upper_lip_R_jointEnd_local_99_local_665_524317', 'eye_socket_L_joint_local_100_local_666_524318', 'eye_L_joint_local_101_local_667_524319', 'eye_brow_L_joint01_local_102_local_668_524320', 'eye_brow_L_joint02_local_103_local_669_524321', 'eye_brow_L_jointEnd_local_104_local_670_524322', 'eye_socket_R_joint_local_105_local_671_524323', 'eye_R_joint_local_106_local_672_524324', 'eye_brow_R_joint01_local_107_local_673_524325', 'eye_brow_R_joint02_local_108_local_674_524326', 'eye_brow_R_jointEnd_local_109_local_675_524327', 'nose_joint01_local_110_local_676_524328', 'nose_joint02_local_111_local_677_524329', 'nose_jointEnd_local_112_local_678_524330', 'forehead_joint01_local_113_local_679_524331', 'forehead_jointEnd_local_114_local_680_524332', 'cheek_L_joint01_local_115_local_681_524333', 'cheek_L_jointEnd_local_116_local_682_524334', 'cheek_R_joint01_local_117_local_683_524335', 'cheek_R_jointEnd_local_118_local_684_524336', 'ear_L_joint01_local_119_local_685_524337', 'ear_L_jointEnd_local_120_local_686_524338', 'ear_R_joint01_local_121_local_687_524339', 'ear_R_jointEnd_local_122_local_688_524340', 'head_jointEnd_local_123_local_689_524341', 'clavicle_L_joint_local_124_local_690_524342', 'shoulder_L_joint_local_125_local_691_524343', 'elbow_L_joint_local_126_local_692_524344', 'forearm_L_joint_local_127_local_693_524345', 'wrist_L_joint_local_128_local_694_524346', 'finger01_L_joint01_local_129_local_695_524347', 'finger01_L_joint02_local_130_local_696_524348', 'finger01_L_joint03_local_131_local_697_524349', 'finger01_L_jointEnd_local_132_local_698_524350', 'finger02_L_joint01_local_133_local_699_524351', 'finger02_L_joint02_local_134_local_700_524352', 'finger02_L_joint03_local_135_local_701_524353', 'finger02_L_joint04_local_136_local_702_524354', 'finger02_L_jointEnd_local_137_local_703_524355', 'finger03_L_joint01_local_138_local_704_524356', 'finger03_L_joint02_local_139_local_705_524357', 'finger03_L_joint03_local_140_local_706_524358', 'finger03_L_joint04_local_141_local_707_524359', 'finger03_L_jointEnd_local_142_local_708_524360', 'finger04_L_joint01_local_143_local_709_524361', 'finger04_L_joint02_local_144_local_710_524362', 'finger04_L_joint03_local_145_local_711_524363', 'finger04_L_joint04_local_146_local_712_524364', 'finger04_L_jointEnd_local_147_local_713_524365', 'finger05_L_joint01_local_148_local_714_524366', 'finger05_L_joint02_local_149_local_715_524367', 'finger05_L_joint03_local_150_local_716_524368', 'finger05_L_joint04_local_151_local_717_524369', 'finger05_L_jointEnd_local_152_local_718_524370', 'clavicle_R_joint_local_153_local_719_524371', 'shoulder_R_joint_local_154_local_720_524372', 'elbow_R_joint_local_155_local_721_524373', 'forearm_R_joint_local_156_local_722_524374', 'wrist_R_joint_local_157_local_723_524375', 'finger01_R_joint01_local_158_local_724_524376', 'finger01_R_joint02_local_159_local_725_524377', 'finger01_R_joint03_local_160_local_726_524378', 'finger01_R_jointEnd_local_161_local_727_524379', 'finger02_R_joint01_local_162_local_728_524380', 'finger02_R_joint02_local_163_local_729_524381', 'finger02_R_joint03_local_164_local_730_524382', 'finger02_R_joint04_local_165_local_731_524383', 'finger02_R_jointEnd_local_166_local_732_524384', 'finger03_R_joint01_local_167_local_733_524385', 'finger03_R_joint02_local_168_local_734_524386', 'finger03_R_joint03_local_169_local_735_524387', 'finger03_R_joint04_local_170_local_736_524388', 'finger03_R_jointEnd_local_171_local_737_524389', 'finger04_R_joint01_local_172_local_738_524390', 'finger04_R_joint02_local_173_local_739_524391', 'finger04_R_joint03_local_174_local_740_524392', 'finger04_R_joint04_local_175_local_741_524393', 'finger04_R_jointEnd_local_176_local_742_524394', 'finger05_R_joint01_local_177_local_743_524395', 'finger05_R_joint02_local_178_local_744_524396', 'finger05_R_joint03_local_179_local_745_524397', 'finger05_R_joint04_local_180_local_746_524398', 'finger05_R_jointEnd_local_181_local_747_524399', 'breast_L_joint_local_182_local_748_524400', 'breast_scale_L_joint_local_183_local_749_524401', 'nipple_L_joint01_local_184_local_750_524402', 'nipple_L_jointEnd_local_185_local_751_524403', 'breast_deform01_L_joint01_local_186_local_752_524404', 'breast_deform01_L_jointEnd_local_187_local_753_524405', 'breast_deform02_L_joint01_local_188_local_754_524406', 'breast_deform02_L_jointEnd_local_189_local_755_524407', 'breast_deform03_L_joint01_local_190_local_756_524408', 'breast_deform03_L_jointEnd_local_191_local_757_524409', 'breast_R_joint_local_192_local_758_524410', 'breast_scale_R_joint_local_193_local_759_524411', 'nipple_R_joint01_local_194_local_760_524412', 'nipple_R_jointEnd_local_195_local_761_524413', 'breast_deform01_R_joint01_local_196_local_762_524414', 'breast_deform01_R_jointEnd_local_197_local_763_524415', 'breast_deform02_R_joint01_local_198_local_764_524416', 'breast_deform02_R_jointEnd_local_199_local_765_524417', 'breast_deform03_R_joint01_local_200_local_766_524418', 'breast_deform03_R_jointEnd_local_201_local_767_524419', 'rib_L_joint01_local_202_local_768_524420', 'rib_L_jointEnd_local_203_local_769_524421', 'rib_R_joint01_local_204_local_770_524422', 'rib_R_jointEnd_local_205_local_771_524423', 'stomach_joint01_local_206_local_772_524424', 'stomach_jointEnd_local_207_local_773_524425', 'hip_L_joint_local_208_local_774_524426','hipp_L_joint_local_hipp_local_hippvd_524460', 'knee_L_joint_local_209_local_775_524427', 'ankle_L_joint_local_210_local_776_524428', 'ball_L_joint_local_211_local_777_524429', 'toe_L_joint_local_212_local_778_524430', 'toe_deform01_L_joint01_local_213_local_779_524431', 'toe_deform01_L_jointEnd_local_214_local_780_524432', 'toe_deform02_L_joint01_local_215_local_781_524433', 'toe_deform02_L_jointEnd_local_216_local_782_524434', 'hip_R_joint_local_217_local_783_524435', 'knee_R_joint_local_218_local_784_524436', 'ankle_R_joint_local_219_local_785_524437', 'ball_R_joint_local_220_local_786_524438', 'toe_R_joint_local_221_local_787_524439', 'toe_deform01_R_joint01_local_222_local_788_524440', 'toe_deform01_R_jointEnd_local_223_local_789_524441', 'toe_deform02_R_joint01_local_224_local_790_524442', 'toe_deform02_R_jointEnd_local_225_local_791_524443', 'penis_joint01_local_226_local_792_524444', 'penis_joint02_local_227_local_793_524445', 'penis_joint03_local_228_local_794_524446', 'penis_jointEnd_local_229_local_795_524447', 'testicles_joint01_local_230_local_796_524448', 'testicles_joint02_local_231_local_797_524449', 'testicles_jointEnd_local_232_local_798_524450', 'vagina_L_joint01_local_233_local_799_524451', 'vagina_R_joint01_local_235_local_801_524453', 'vagina_L_jointEnd_local_234_local_800_524452', 'vagina_R_jointEnd_local_236_local_802_524454', 'butt_L_joint01_local_237_local_803_524455', 'butt_L_jointEnd_local_238_local_804_524456', 'butt_R_joint01_local_239_local_805_524457', 'butt_R_jointEnd_local_240_local_806_524458', 'anus_joint_local_241_local_807_524459']

    orderedJoints=[]
    usage = 524288
    if me.get("orderedJoints") is not None:
        orderedJoints = me["orderedJoints"].split(",")
    for joint in orderedJoints:
        #
        if joint == 'shin_L_joint':
            aaaaaa=1
            aaaaaa=aaaaaa+2        
        blender_name, villa_name, lname_tjoint, lname_vertexdata = getLinkedInfoForVertexGroup(joint)
        #
        vg_dict[blender_name]={'tk_name':villa_name, 'tjoint':lname_tjoint, 'vertexdata':lname_vertexdata ,'usage':usage  }
        usage += 1 
        print (">>  reordered:"+blender_name)    
        #
    if True == False :
        # first lets store all stock VGs names 
        originalVGNamesOnlyArray = [ item[0] for item in vertexGroupsArray ]
        #originalVGNamesOnlyArray = [ villafyname(item) for item in animSkeletonValues ]



        #we get all vertex groups that contains _joint and root
        objectVGArray = [ vgroup.name for vgroup in ob.vertex_groups if ('_joint' in vgroup.name or 'root'==vgroup.name)]

        
        # but to keep a bit of order, lets keep the list as original bodies, with root coming first, then the rest of original VGs, then at the end we add new custom VGs
        vgExtraArray = [e for e in objectVGArray if e not in originalVGNamesOnlyArray]

        for vertexGroup in vertexGroupsArray: 
            blender_name = vertexGroup[0]
            villa_name = vertexGroup[1]
            lname_tjoint = vertexGroup[2]
            lname_vertexdata = vertexGroup[3]
            usage = vertexGroup[4]

            vg_dict[blender_name]={'tk_name':villa_name, 'tjoint':lname_tjoint, 'vertexdata':lname_vertexdata ,'usage':usage  }
            print (">>original:"+blender_name)
            #
        lastUsage = getLastUsageForVertexGroup()
        for vgExtra in vgExtraArray:        
            """
            for empty in bpy.data.objects:
                if  empty.type != 'EMPTY':
                    continue
                if  empty.get("exportAsVillaJoint") is None or empty["exportAsVillaJoint"] == False :
                    continue
                if  empty.get("isCustomVillaJoint") is None or empty["isCustomVillaJoint"] == False :
                    continue        
            """
            blender_name = vgExtra    
            lastUsage +=1
            blender_name, villa_name, lname_tjoint, lname_vertexdata, usage =  createLinkedInfoForCustomVertexGroup(blender_name,lastUsage)
            vg_dict[blender_name]={'tk_name':villa_name, 'tjoint':lname_tjoint, 'vertexdata':lname_vertexdata ,'usage':usage  }        
            print (">>  custom:"+blender_name)    
    toc = time.perf_counter()
    print("*********************************** finished vertexgroups1 in "+ "{:0.4f}".format(toc - tic)+" seconds")

    tic = time.perf_counter()
    #lets init the blocks first
    pyBlock_MeshDataVG_VertexData = []    

    VGroups = OrderedDict()            
    #VertGroups = ob.vertex_groups
    # create vertex group lookup dictionary for names
    vgroup_names = [ vgroup.name for vgroup in ob.vertex_groups]
    for idx,keyName in enumerate(vg_dict):
        vgblock = vg_dict[keyName]
        usage = vgblock['usage']
        #print ("usage: "+usage)
        VGroups[usage] = OrderedDict() 
        VGroups[usage]["localname"] = vgblock['vertexdata'] #lname_vertexdata;
        VGroups[usage]["tjoint"] = vgblock['tjoint'] #lname_tjoint
        VGroups[usage]["name"] = vgblock['tk_name'] #name
        VGroups[usage]["weights"] = [0.0] * len(me.vertices)
        #VG = ob.vertex_groups[keyName]
        if keyName in vgroup_names:
            for i, w in get_weights(ob, keyName):
                VGroups[usage]["weights"][i] = w        
        pyBlock_MeshDataVG_VertexData.append("VertexDataF32 :" + VGroups[usage]["localname"])
        #pyBlock_MeshDataJointsArray.append("TJoint :"+VGroups[usage]["tjoint"])
    """             
    for VG in VertGroups:
        #print ("processing: "+VG.name)
        if VG.name in vg_dict:
            vgblock = vg_dict[VG.name]
            usage = vgblock['usage']
            #print ("usage: "+usage)
            VGroups[usage] = {}
            VGroups[usage]["localname"] = vgblock['vertexdata'] #lname_vertexdata;
            VGroups[usage]["bclocal"] = vgblock['tjoint'] #lname_tjoint
            VGroups[usage]["name"] = vgblock['tk_name'] #name
            VGroups[usage]["weights"] = [0.0] * len(me.vertices)
            for i, w in get_weights(ob, VG):
                VGroups[usage]["weights"][i] = w
            #
            pyBlock_MeshDataVG_VertexData.append("VertexDataF32 :" + VGroups[usage]["localname"]) 
    """
    """ 
            #vg_idx = 0
            #o = bpy.context.object
            #vs = [ v for v in o.data.vertices if vg_idx in [ vg.group for vg in v.groups ] ]
            #print(lname_vertexdata, lname_tjoint, ob_name, usage)
            # for i in range(len(me.vertices)):
                # index = me.vertices[i].index
                # try:
                    # weight = VG.weight(index)
                # except:
                    # weight = 0.0
                # VGroups[usage]["weights"].append(weight)
    """ 
    ###########################################    
    toc = time.perf_counter()
    print("*********************************** finished vertexgroups2 in "+ "{:0.4f}".format(toc - tic)+" seconds")

    tic = time.perf_counter()
    tk_conversion_matrix = mathutils.Matrix(((1,0,0),(0,0,-1),(0,1,0)))

    #for stock_key in stock_shapekeys:
    #    SKName = stock_key[0]
    #    print (SKName)

    #lets init the blocks first
    pyBlock_MeshDataSK_VertexData = []
    pyBlock_MeshDataSK_BlendControl = []
    SKGroups = OrderedDict()

    #we need an ordered dictionary to keep track of the shapekeys added to the file. First default shapekeys will be written and marked as processed
    #then we will loop again and work with the keys not marked in the first run (which are new added custom shapekeys)
    processed_SK = OrderedDict() # important to make this an ordered dictionary to keep shapekeys in order they are defined

    ob = bpy.data.objects["body_subdiv_cage"]
    me = ob.data
    basis_verts = ob.data.shape_keys.key_blocks[0]
    #copy all shapekeys name in the processed_SK dictionary (lookup table)
    for key in ob.data.shape_keys.key_blocks[1:]:
        SKName = key.name
        processed_SK[SKName] = False
        #print (SKName)

    #stock_shapekeys is defined dictionary_shapekeys.py and is actually an array
    # first lets populate the blocks for pyBlock_MeshData_VertexData, pyBlock_MeshData_BlendControl and SKGroups[usage]["data"] for the stock shapekeys
    # if a stock shapekey is not found in the current mesh shapekeys list, then is added as zeroed
    for stock_key in stock_shapekeys:
        stock_key_name = stock_key[0]
        stock_key_shortname = stock_key[1]
        blendControl_local = "local_"+stock_key[2]
        vertexDataVector3f_local = "local_"+stock_key[3]
        usage = stock_key[4]    
        SKGroups[usage] = {}
        SKGroups[usage]["localname"] = vertexDataVector3f_local;
        print ("Processing stock key: " +stock_key_name+"usage: "+usage)
        current_key = ""
        isDefined = False
        for processed_key in processed_SK.keys():
            #print ("testing for:  "+processed_key)
            if stock_key_name in processed_key or stock_key_shortname in processed_key:
                current_key = processed_key
                isDefined = True
                break
        #
        pyBlock_MeshDataSK_VertexData.append("VertexDataVector3f :" + vertexDataVector3f_local)
        pyBlock_MeshDataSK_BlendControl.insert(0,"BlendControl :" + blendControl_local)
        #    
        data = []
        epsilon = 0.000001
        #
        if isDefined:
            print ("Found key: " + current_key+ " exported as stock object: "+stock_key_name)
            processed_SK[current_key] = True
            key = ob.data.shape_keys.key_blocks[current_key]
            for i in range(len(me.vertices)):
                delta = (key.data[i].co - basis_verts.data[i].co) 
                if ( abs(delta.x) < epsilon and abs(delta.y) < epsilon and abs(delta.z) < epsilon ) : 
                    data.append("(0, 0, 0)")
                else:
                    delta = delta * tk_conversion_matrix
                    data.append("( "+"{:0.10f}".format(delta.x)+", "+"{:0.10f}".format(delta.y)+", "+"{:0.10f}".format(delta.z)+")")
        else:
            print ("Missing key: " + stock_key_shortname + " exported as zeroed object: "+stock_key_name)
            for i in range(len(me.vertices)):
                data.append("(0, 0, 0)")
        #
        SKGroups[usage]["data"] = ",".join(data)        
        #
        #
        #BlendControl :local_843 Object.Name "body_blends_body_vagina_morph";
        #VertexDataVector3f :local_808 . {
        #    VertexDataVector3f.DataArray Array_Vector3f [ (0, 0, 0), (0, 0, 0), ... ];
        #    VertexData.Usage U32(655373);
        #};

    #stock shapekeys stops at 655373, so we are going to add all custom shapekeys with usage from 655373+1 and up
    usage = 655373 # last usage consumed by stock morphs
    for processed_key in processed_SK.keys():
        if processed_SK[processed_key] == False:
            usage = usage + 1 #increment usage
            SKGroups[usage] = {}
            processed_key_pretty = re.sub(r'\W+', '_', processed_key) #replacing any non alfanumeric character in shapekey with "_" character
            print ("Found custom key: " + processed_key+ " exported as custom object: "+processed_key_pretty)
            processed_SK[processed_key] = True
            pyBlock_MeshDataSK_VertexData.append("VertexDataVector3f :vert_"+processed_key_pretty)
            pyBlock_MeshDataSK_BlendControl.append("BlendControl :bc_"+processed_key_pretty)
            SKGroups[usage]["localname"] = "vert_"+processed_key_pretty;
            SKGroups[usage]["blendname"] = "bc_"+processed_key_pretty;
            SKGroups[usage]["realname"] = processed_key_pretty;
            data = []
            epsilon = 0.000001
            key = ob.data.shape_keys.key_blocks[processed_key]
            for i in range(len(me.vertices)):
                delta = (key.data[i].co - basis_verts.data[i].co) 
                if ( abs(delta.x) < epsilon and abs(delta.y) < epsilon and abs(delta.z) < epsilon ) : 
                    data.append("(0, 0, 0)")
                else:
                    delta = delta * tk_conversion_matrix
                    data.append("( "+"{:0.10f}".format(delta.x)+", "+"{:0.10f}".format(delta.y)+", "+"{:0.10f}".format(delta.z)+")")
            SKGroups[usage]["data"] = ",".join(data)        


        
    toc = time.perf_counter()
    print("*********************************** finished shapekeys in "+ "{:0.4f}".format(toc - tic)+" seconds")

    tic = time.perf_counter()
    # from here we start to print to files    

    fileout = open(exportfolderpath+'bsBlocks/part0.bs_block', 'w')
    fileout.write("//BSB6\n\n")
    fileout.write("TTransform :local_1 . {\n")
    fileout.write("\tTNode.SNode STransform :local_2;\n")
    fileout.write("\tObject.Name \"Shared/Body/body"+bodyNo+".ma\";\n")
    fileout.write("};\n")
    fileout.flush()
    fileout.close()

    
    # here the outputfile goes in        
    fileout = open(exportfolderpath+'bsBlocks/URQqAAA_bs.block', 'w')
    fileout.write("\tMeshStructure.NumPoints I32("+str(len(me.vertices))+");\n")
    fileout.write("\tMeshStructure.EdgePointArray Array_I32 "+str(edgepointarray)+";\n")
    fileout.flush()
    fileout.close()
    
    fileout = open(exportfolderpath+'bsBlocks/URQqBBB_bs.block', 'w')
    fileout.write("\tMeshStructure.FaceLengthArray Array_I32 "+str(facelengtharray)+";\n")
    fileout.flush()
    fileout.close()
    
    fileout = open(exportfolderpath+'bsBlocks/URQqCCC_bs.block', 'w')
    fileout.write("\tMeshStructure.FaceEdgeArray Array_I32 "+str(faceedgearray)+";\n")
    fileout.flush()
    fileout.close()
    
    fileout = open(exportfolderpath+'bsBlocks/URQqDDD_bs.block', 'w')
    fileout.write("\tMeshStructure.FaceAttrArray Array_I32 "+str(faceattrarray)+";\n\n")
    fileout.flush()
    fileout.close()
    
    fileout = open(exportfolderpath+'bsBlocks/URQqEEE_bs.block', 'w')
    fileout.write("\tMeshData.VertexArray Array_Vector3f "+"[ "+', '.join(["( "+', '.join(["{:0.10f}".format(vertarray[i][j]) for j in range(len(vertarray[i]))])+")" for i in range(len(vertarray))]) +"];\n")
    fileout.flush()
    fileout.close()
    
    fileout = open(exportfolderpath+'bsBlocks/URQqFFF_bs.block', 'w')
    fileout.write("\tMeshData.SimilarArray Array_I32 "+str(faceattrarray)+";\n")
    fileout.flush()
    fileout.close()
    
    
    #***********************************************
    #***********************************************
    #***********************************************
    #***********************************************
    
    fileout = open(exportfolderpath+'bsBlocks/part3.1_1_content_MeshDataShaderArray.bs_block', 'w')
    fileout.write( " , ".join(pyblock_MeshData_ShaderArray) )
    fileout.flush()
    fileout.close()

    
    
    fileout = open(exportfolderpath+'bsBlocks/URQqGGG_bs.block', 'w')
    fileout.write("\tMeshData.FaceShaderArray Array_I32 "+str(faceshaderarray)+";\n")
    fileout.flush()
    fileout.close()
    
    fileout = open(exportfolderpath+'bsBlocks/URQqHHH_bs.block', 'w')
    fileout.write("VertexDataVector2f :"+uvllocal+" . {\n")
    fileout.write("\tVertexDataVector2f.DataArray Array_Vector2f "+"[ "+', '.join(["( "+', '.join(["{:0.10f}".format(vertexdata0[i][j]) for j in range(len(vertexdata0[i]))])+")" for i in range(len(vertexdata0))]) +"];\n")
    fileout.write("\tVertexData.Usage U32("+uvlusage+");\n")
    fileout.write("};\n")

    fileout = open(exportfolderpath+'bsBlocks/URQqIII_bs.block', 'w')
    for key in VGroups:
        #print("sending output: "+key)
        VGroup = VGroups[key]
        fileout.write("VertexDataF32 :"+VGroup["localname"]+" . {\n")
        weights_data_out = ', '.join(["{:0.10f}".format(VGroup["weights"][i]) for i in range(len(VGroup["weights"]))])
        weights_data_out = weights_data_out.replace("-0.0000000000","0").replace("0.0000000000","0")        #replace long zeros
        fileout.write("\tVertexDataF32.DataArray Array_F32 [ "+ weights_data_out +"];\n")
        fileout.write("\tVertexData.Usage U32("+str(key)+");\n")
        fileout.write("};\n")
    fileout.flush()
    fileout.close()






    #pyBlock_MeshDataVG_VertexData.reverse()
    fileout = open(exportfolderpath+'bsBlocks/part3.0_1_content_MeshDataVertexData_1_weights.bs_block', 'w')
    fileout.write( " , ".join(pyBlock_MeshDataVG_VertexData) )
    fileout.write( " , ") # lets add one more comma, because there is more data coming after this
    fileout.flush()
    fileout.close()

    """
    fileout = open(exportfolderpath+'bsBlocks/part3.2_1_content_MeshDataJointArray.bs_block', 'w')
    fileout.write( " , ".join(pyBlock_MeshDataJointsArray) )
    fileout.flush()
    fileout.close()
    """


    fileout = open(exportfolderpath+'bsBlocks/URQqJJJ_bs.block', 'w')
    for usage in SKGroups.keys():
        localname =SKGroups[usage]["localname"]
        SKGroup = SKGroups[usage]
        #SKGroup = SKGroups["655360"] 
        #print(usage, localname)    
        fileout.write("VertexDataVector3f :"+localname + " . {\n")
        fileout.write("\tVertexDataVector3f.DataArray Array_Vector3f [ "+SKGroup["data"]+"];\n")
        fileout.write("\tVertexData.Usage U32("+str(usage)+");\n")
        fileout.write("};\n")
    fileout.flush()
    fileout.close()

    fileout = open(exportfolderpath+'bsBlocks/part3.0_1_content_MeshDataVertexData_2_morphs.bs_block', 'w')
    fileout.write( " , ".join(pyBlock_MeshDataSK_VertexData) )
    fileout.flush()
    fileout.close()

    fileout = open(exportfolderpath+'bsBlocks/part4_4_content_MeshDataBlendControl.bs_block', 'w')
    fileout.write( " , ".join(pyBlock_MeshDataSK_BlendControl) )
    fileout.flush()
    fileout.close()


    #BlendControl :local_840 Object.Name "body_blends_body_eye_L_morph";
    fileout = open(exportfolderpath+'bsBlocks/part5_2_extraBlendControls.bs_block', 'w')
    for usage in SKGroups.keys():
        if int(usage) > 655373:
            blendname = SKGroups[usage]["blendname"]
            realname = SKGroups[usage]["realname"]
            SKGroup = SKGroups[usage]
            #SKGroup = SKGroups["655360"] 
            print(usage, localname)
            #if realname.startswith('jcm_'):
            if realname.startswith('aa_'):
                fileout.write("BlendControl :"+blendname +" . {\n");
                fileout.write("\tBlendControl.Weight F32(1);\n");
                fileout.write("\tBlendControl.StaticBlend I32(2);\n");
                fileout.write("\tObject.Name \""+realname+"\";\n};\n");
            else:
                fileout.write("BlendControl :"+blendname + " Object.Name \""+realname+"\";\n")
    fileout.flush()
    fileout.close()


    fileout = open(exportfolderpath+'bsBlocks/part6.bs_block', 'w')
    fileout.write("STransform :local_2 Object.Name \"SShared/Body/body"+bodyNo+".ma\";\n")
    fileout.flush()
    fileout.close()
    toc = time.perf_counter()
    print("*********************************** finished writing files in "+ "{:0.4f}".format(toc - tic)+" seconds")

    if includeGeograftsOnExport:
        bpy.ops.object.delete()
    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


    ctypes.windll.user32.FlashWindow(ctypes.windll.user32.GetActiveWindow(), True )



