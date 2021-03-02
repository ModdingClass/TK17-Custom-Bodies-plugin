import bpy, math
import sys
import os
from .tools_message_box import *

def export_fake_bones(exportfolderpath, bodyNo, ignoreSomeBones):
	meshes = [ob for ob in bpy.data.objects if ob.type == 'MESH']
	
	text = ""
	
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
		text += "\tSPolygonGeometry.PrimType Primitive.TypeEnum.Triangle;\n"
		text += "\tSPolygonGeometry.PrimCount I32(8);\n"
		text += "\tSPolygonGeometry.PrimLengthArray Array_I32 [ 24 ];\n"
		text += "\tSPolygonGeometry.IndexArray Array_I32 [ 0, 2, 5, 0, 5, 4, 0, 4, 3, 0, 3, 2, 4, 5, 1, 3, 4, 1, 5, 2, 1, 2, 3, 1 ];\n";
		text += "\tSPolygonGeometry.VertexData [ VertexDataVector2f :local_injected_joint_UVMAP000 ];\n"
		text += "\tSPolygonGeometry.VertexArray Array_Vector3f [ (0, 0, 0), (1, 0, 0), (0.18182, 0, 0.12857), (0.18182, -0.12857, 0), (0.18182, 0, -0.03766), (0.18182, 0.12857, 0) ];\n"
		text += "\tSPolygonGeometry.NormalArray Array_Vector3f [ (-0.85886, 0.51222, 0), (0.36892, 0.92946, 0), (0.12046, 0.99272, 0), (0.11821, 0.23388, 0.96505), (0.03421, -0.99941, 0), (0.11821, 0.23388, -0.96505)];\n"
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
	text += "FileObject :fakebone_file_object FileObject.FileName \"PoseEdit/checker_box01\";\n"
	
	#print(text)

	file_path = exportfolderpath+"injected_bone_markers_body"+bodyNo+".bs"
	#file_path = "G:/rv/z/VXB2/Addons/000.Custom.Body.P741.B741.Caroline-injector/Scenes/Shared/Body/injected_bone_markers_body741.bs"
	fileout = open(file_path,"w")
	fileout.write(text)
	fileout.flush()
	fileout.close()
	ShowMessageBox("Fake bones exported to: "+"injected_bone_markers_body"+bodyNo+".bs", "Success", 'INFO')		