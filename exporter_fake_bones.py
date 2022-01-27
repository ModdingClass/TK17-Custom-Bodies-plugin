import bpy, math, mathutils
import sys
import os
from .tools_message_box import *


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
    #
    return len(me.polygons),vertex_array,normal_array,uv_array,prim_length_array,index_array


def export_fake_bones(exportfolderpath, bodyNo, ignoreSomeBones):
    meshes = [ob for ob in bpy.data.objects if ob.type == 'MESH']
    
    text = ""
    uvdata = []
    #prim_count,vertex_array,normal_array,uvdata,prim_length_array,index_array = get_fake_mesh_datablocks (mesh.name)
    count = 3000
    for mesh in meshes:
        if mesh.parent == None or not "cone_" in mesh.name:
            continue
        if ignoreSomeBones == True:
            if ("_jointEnd" in mesh.name and not mesh.name in ["spine_jointEnd", "neck_jointEnd", "lower_jaw_jointEnd", "forehead_jointEnd", "head_jointEnd"]):
                continue
            if ("toe_joint" in mesh.name):
                continue
            if ("testicles" in mesh.name):
                continue                
            if ("penis" in mesh.name):
                continue                                
        acceptedName = mesh.name.replace(".","_")
        localmat = mesh.matrix_local
        decomposed = localmat.decompose()
        scaleval = mesh.scale
        scaleval.x = mesh["scale"][0]
        scaleval.y = mesh["scale"][1]
        scaleval.z = mesh["scale"][2]
        diameter = scaleval.x * 0.1
        radius = diameter * 0.5
        rot = decomposed[1].to_euler()
        rx = math.degrees(rot.x)
        ry = math.degrees(rot.y)
        rz = math.degrees(rot.z)
        rx = 0
        ry = 0
        if mesh.get("isFlipped") is not None and mesh["isFlipped"] == True :
            ry = -180
        rz = 0
        #
        if mesh.get("fake_mesh_datablocks") is not None:
            fake_mesh_datablocks = mesh.get("fake_mesh_datablocks")
            prim_count = fake_mesh_datablocks["prim_count"]
            vertex_array = fake_mesh_datablocks["vertex_array"]
            normal_array = fake_mesh_datablocks["normal_array"]
            uvdata = fake_mesh_datablocks["uvdata"]
            prim_length_array = fake_mesh_datablocks["prim_length_array"].to_list()
            print(prim_length_array)
            index_array = fake_mesh_datablocks["index_array"].to_list()
            print (index_array)
        else:
            prim_count,vertex_array,normal_array,uvdata,prim_length_array,index_array = get_fake_mesh_datablocks (mesh.name)
        #
        #prim_count = 8
        text += "TPolygonGeometry :local_"+acceptedName+"_MESH"+" . {\n"
        count += 1
        text += "\tTGeometry.Shader RenderShader :local_fakebone_render_shader;\n"
        text += "\tTNode.SNode SPolygonGeometry :local_S"+acceptedName+"_MESH"+";\n"
        parentname = "_".join(mesh.parent.name.split("_")[-2:])
        text += "\tTNode.Parent TTransform :local_"+acceptedName+";\n"
        text += "\tTNode.BoundingSphere Spheref( 0, 0, 0, "+'{:.10f}'.format(diameter)+" );\n"
        text += "\tObject.Name \""+acceptedName+"_mesh"+"\";\n";
        text += "};\n"
        text += "SPolygonGeometry :local_S"+acceptedName+"_MESH"+" . {\n"
        text += "\tSPolygonGeometry.PrimType Primitive.TypeEnum.Polygon;\n"
        text += "\tSPolygonGeometry.PrimCount I32(" + str(prim_count) + ");\n"
        text += "\tSPolygonGeometry.PrimLengthArray Array_I32 " + str(prim_length_array) + ";\n"
        text += "\tSPolygonGeometry.IndexArray Array_I32 " + str(index_array) + ";\n";
        text += "\tSPolygonGeometry.VertexData [ VertexDataVector2f :local_injected_joint_UVMAP000 ];\n"
        text += "\tSPolygonGeometry.VertexArray Array_Vector3f [ "+', '.join(["( "+', '.join(["{:0.8f}".format(vertex_array[i][j]) for j in range(len(vertex_array[i]))])+")" for i in range(len(vertex_array))]) + " ];\n"   #+ str(vertex_array)
        #text += "\tSPolygonGeometry.NormalArray Array_Vector3f [ (-0.85886, 0.51222, 0), (0.36892, 0.92946, 0), (0.12046, 0.99272, 0), (0.11821, 0.23388, 0.96505), (0.03421, -0.99941, 0), (0.11821, 0.23388, -0.96505)];\n"
        text += "\tSPolygonGeometry.NormalArray Array_Vector3f [ "+', '.join(["( "+', '.join(["{:0.8f}".format(normal_array[i][j]) for j in range(len(normal_array[i]))])+")" for i in range(len(normal_array))]) + " ];\n" #(-0.85886, 0.51222, 0), (0.36892, 0.92946, 0), (0.12046, 0.99272, 0), (0.11821, 0.23388, 0.96505), (0.03421, -0.99941, 0), (0.11821, 0.23388, -0.96505)
        text += "\tObject.Name \"S"+acceptedName+"_mesh"+"\";\n";
        text += "};\n"
        count += 2
        text += "TTransform :local_"+acceptedName+" . {\n"
        text += "\tTNode.SNode STransform :local_S"+acceptedName+";\n"
        text += "\tTNode.Parent TJoint :"+mesh["localTJoint"]+";\n"
        text += "\tObject.Name \""+acceptedName+"\";\n"
        text += "};\n"
        text += "STransform :local_S"+acceptedName+" . {\n"
        text += "\tSSimpleTransform.Rotation Vector3f( "+'{:.10f}'.format(rx)+", "+'{:.10f}'.format(ry)+", "+'{:.10f}'.format(rz)+");\n"
        text += "\tSSimpleTransform.Scaling Vector3f( "+'{:.10f}'.format(scaleval.x)+", "+'{:.10f}'.format(scaleval.y)+", "+'{:.10f}'.format(scaleval.z)+");\n"
        text += "\tObject.Name \"S"+acceptedName+"\";\n"
        text += "};\n"
        count += 2
    
    text += "\n"
    text += "VertexDataVector2f :local_injected_joint_UVMAP000 . {\n"
    text += "\tVertexDataVector2f.DataArray Array_Vector2f "+"[ "+', '.join(["( "+', '.join(["{:0.8f}".format(uvdata[i][j]) for j in range(len(uvdata[i]))])+")" for i in range(len(uvdata))])+" ];\n"            #+str(uvdata)
    text += "\tVertexData.Usage U32(65536);\n"
    text += "};\n"
    text += "\n"
    text += "RenderShader :local_fakebone_render_shader . {\n"
    text += "\tRenderShader.Surface ShaderPhong :local_fakebone_shader_phong;\n"
    text += "\tObject.Name \"fakebone_render_shader\";\n"
    text += "};\n"
    text += "ShaderPhong :local_fakebone_shader_phong . {\n"
    text += "\tShaderPhong.Color ShaderTexture :local_fakebone_shader_texture;\n"
    text += "\tShaderPhong.Material RenderMaterial :local_fakebone_render_material;\n"
    text += "};\n"
    text += "RenderMaterial :local_fakebone_render_material . {\n"
    text += "\tRenderMaterial.SpecularColor Vector3f( 0.150000006, 0.150000006, 0.150000006 );\n"
    text += "\tRenderMaterial.Shininess F32(10);\n"
    text += "};\n"
    text += "ShaderTexture :local_fakebone_shader_texture . {\n"
    text += "\tShaderTexture.Texture Texture2D :local_fakebone_texture;\n"
    text += "\tObject.Name \"fakebone_shader_texture\";\n"
    text += "};\n"
    text += "Texture2D :local_fakebone_texture . {\n"
    text += "\tTexture.FileObject FileObject :fakebone_file_object;\n"
    text += "\tTexture.DefaultColor Vector4f( 0.8500000238, 0.6516667008, 0.5525000095, 1 );\n"
    text += "\tObject.Name \"fakebone_texture\";\n"
    text += "};\n"
    #text += "FileObject :fakebone_file_object FileObject.FileName \"PoseEdit/checker_box01\";\n" # Shared/Body/new_axis_bone
    text += "FileObject :fakebone_file_object FileObject.FileName \"Shared/Body/new_axis_bone\";\n" # 
    #print(text)

    file_path = exportfolderpath+"injected_bone_markers_body"+bodyNo+".bs"
    #file_path = "G:/rv/z/VXB2/Addons/000.Custom.Body.P741.B741.Caroline-injector/Scenes/Shared/Body/injected_bone_markers_body741.bs"
    fileout = open(file_path,"w")
    fileout.write(text)
    fileout.flush()
    fileout.close()
    ShowMessageBox("Fake bones exported to: "+"injected_bone_markers_body"+bodyNo+".bs", "Success", 'INFO')        