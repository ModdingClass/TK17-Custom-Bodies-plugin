import struct
import bmesh
import bpy
import os
#from stl.types import *
from mathutils import Matrix, Vector, Euler

class H5MReader(object):

	def __init__(self, file, object_name):
		self.file = file
		self.object_name = object_name
		self.offset = 0

	def read_bytes(self, byte_count):
		bytes = self.file.read(byte_count)
		if len(bytes) < byte_count:
			raise FormatError(
				"Unexpected end of file at offset %i" % (
					self.offset + len(bytes),
				)
			)
		self.offset += byte_count
		return bytes

	def read_uint32(self):
		bytes = self.read_bytes(4)
		return struct.unpack('<I', bytes)[0]

	def read_uint16(self):
		bytes = self.read_bytes(2)
		return struct.unpack('<H', bytes)[0]

	def read_float(self):
		bytes = self.read_bytes(4)
		return struct.unpack('<f', bytes)[0]

	def read_vector3d(self):
		x = self.read_float()
		y = self.read_float()
		z = self.read_float()
		return Vector3d(x, y, z)

	def read_header(self):
		bytes = self.read_bytes(3)
		#print(bytes)
		#return struct.unpack('3c', bytes)[0]
		#.strip('\0')
		
	# read unsigned byte from file
	def read_whole_file(self):
		file_object = self.file
		object_name = self.object_name
		#print("size of fmt:")
		fmt = '3s'
		#print(struct.calcsize(fmt))
		data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))[0]
		header = "".join(map(chr, data))
		print('header is %s'%header)
		
		fmt = 'I'
		#print('fmt size%s'%struct.calcsize(fmt))
		data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
		print('type is %i'%data)
		
		if data[0] == 11:
			print('type is again %i'%data)
			fmt = '3f'
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			x = data[0]
			y = data[1]
			z = data[2]
			print('got the bound min:')		
			print('x%f'%x)
			print('y%f'%y)
			print('z%f'%z)
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			x = data[0]
			y = data[1]
			z = data[2]
			print('got the bound max:')		
			print('x%f'%x)
			print('y%f'%y)
			print('z%f'%z)
			
		fmt = 'I'
		#print('fmt size%s'%struct.calcsize(fmt))
		data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
		vcount = data[0]
		print('VCOUNT : vertex count: %i'%data)
	
		fmt = 'I'
		#print('fmt size%s'%struct.calcsize(fmt))
		data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
		print('VSIZE : size of vertex struct: %i'%data)
		
		fmt = 'I'
		#print('fmt size%s'%struct.calcsize(fmt))
		data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
		icount = data[0]
		print('ICOUNT : count of indices in index array: %i'%data)		
		
		fmt = 'I'
		#print('fmt size%s'%struct.calcsize(fmt))
		data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
		scount = data[0]
		print('SCOUNT : count of subsets: %i'%data)	

		vertices = []
		indices = []
		faces = []
		uvs = []
		for i in range(vcount):
			fmt = '3f'
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			#print('p: %i'%data)				
			x = data[0]
			y = data[1]
			z = data[2]
			#print('got the vertex')		
			#print('x%f'%x)
			#print('y%f'%y)
			#print('z%f'%z)
			#vertex = Vector[(x, y, z)]
			vertices.append([x, -z, y])
			#print (', '.join(vertex))
			fmt = '9f'
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			#print('skipping junk')				
			#D3DXVECTOR3 p  - 12 bytes - vertex position
			#D3DXVECTOR3 t	- 12 bytes - vertex tangent
			#D3DXVECTOR3 b	- 12 bytes - vertex binormal
			#D3DXVECTOR3 n	- 12 bytes - vertex normal
			#D3DXVECTOR2 uv	- 8  bytes - vertex texture coords
			fmt = '2f'
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			u = data[0]
			v = 1-data[1]
			uvs.append([u,v])
			
		icount = int(icount/3)
		for i in range(icount):
			fmt = '3I'
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			a = data[0]
			b = data[1]
			c = data[2]
			#indices.append([a, b, c])
			#if (i < icount):
			faces.append([a, b, c])
			#faces.append([a])
		#print (uvs)	
		#print(vertices)
		#print(faces)
		mesh = bpy.data.meshes.new(object_name)
		#faces = [[0,1,2], [3,4,5], [6,7,8], [9,10,11]]
		mesh.from_pydata(vertices, [], faces)
		object = bpy.data.objects.new(object_name, mesh)
		bpy.context.scene.objects.link(object) # link object to scene	
		
		
		uvtex = mesh.uv_textures.new()
		#me = bpy.context.object.data
		#uvtex.uv_textures.new("test")
		mesh.uv_layers[-1].data.foreach_set("uv", [uv for pair in [uvs[l.vertex_index] for l in mesh.loops] for uv in pair])

		
		
		#	subset id 		- 4 byte UINT
		#	face start 		- 4 byte UINT
		#	face count		- 4 byte UINT
		#	vertex start	- 4 byte UINT
		#	vertex count	- 4 byte UINT		
		for i in range(scount):
			fmt = '5I' #20 is a size of one subset struct
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			subset_id = data[0]
			face_start = data[1]
			face_count = data[2]
			vertex_start = data[3]
			vertex_count = data[4]
		
		print('subset_id: %i'%subset_id)
		print('face_start: %i'%face_start)
		print('face_count: %i'%face_count)
		print('vertex_start: %i'%vertex_start)
		print('vertex_count: %i'%vertex_count)
		
		for i in range(scount):
			fmt = '17I' #DXMATERIAL9 struct - 68 bytes, search in net info about this struct   (search for D3DMATERIAL9 )
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
	
	

			
			fmt = 'I' #D_STR_SIZE - 4 byte UINT, length of relative path to diffuse texture
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			D_STR_SIZE = '{}s'.format(data[0])
			print('D_STR_SIZE: %s'%D_STR_SIZE)
			fmt = D_STR_SIZE
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			texture_filename = "".join(map(chr, data[0]))
			print('DIFF_NAME: %s'%texture_filename)

			fmt = 'I' #N_STR_SIZE - 4 byte UINT, length of relative path to diffuse texture
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			N_STR_SIZE = '{}s'.format(data[0])
			print('N_STR_SIZE: %s'%N_STR_SIZE)
			fmt = N_STR_SIZE
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			normal_filename = "".join(map(chr, data[0]))
			print('NORM_NAME: %s'%normal_filename)

			fmt = 'I' #S_STR_SIZE - 4 byte UINT, length of relative path to diffuse texture
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))			
			S_STR_SIZE = '{}s'.format(data[0])
			print('S_STR_SIZE: %s'%S_STR_SIZE)
			fmt = S_STR_SIZE
			data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			spec_filename = "".join(map(chr, data[0]))
			print('SPEC_NAME: %s'%spec_filename)	
			
			
			print(self.file.name)	
			print(os.path.basename(self.file.name))	
			dir_path = os.path.dirname(self.file.name)
			print('dir_path: %s'%dir_path)
			print('-----------------------------------')
			material_name = os.path.splitext(os.path.basename(texture_filename))[0]
			# Get material
			mat = bpy.data.materials.get(material_name)
			if mat is None:
				# create material
				print('-----------------------------------1')				
				mat = bpy.data.materials.new(name=material_name)
				mat.diffuse_intensity = 1
				mat.specular_intensity = 0
				# nodes block starts here
				mat.use_nodes = True
				nodes = mat.node_tree.nodes
				print('-----------------------------------2')				
				# Remove default
				#nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF')
				#nodes.remove(mat.node_tree.nodes.get('Material'))
				shaderNodeBaseColorImageTexture = nodes.new('ShaderNodeTexImage')
				shaderNodeBaseColorImageTexture.location = -300,500	
				shaderNodeBaseColorImageTexture.width = shaderNodeBaseColorImageTexture.width+300
				shaderNodePBRImageTexture = nodes.new('ShaderNodeTexImage')
				shaderNodePBRImageTexture.location = -300,0
				shaderNodePBRImageTexture.width = shaderNodePBRImageTexture.width+300
				shaderNodeSeparateRGB = nodes.new('ShaderNodeSeparateRGB')
				shaderNodeSeparateRGB.location = 300,0				
				shaderNodePrincipled = nodes.new('ShaderNodeBsdfPrincipled')
				shaderNodePrincipled.location = 535,185	
				
				shaderNodeOutputMaterial = nodes.new('ShaderNodeOutputMaterial')
				shaderNodeOutputMaterial.location = 900,500	
				
				
				shaderNodeOutput = nodes.get('Output')
				shaderNodeOutput.location = 1500,500	
				shaderNodeOutput.mute = True
				shaderNodeMaterial = nodes.get('Material')
				shaderNodeMaterial.location = 1200,500					
				print('-----------------------------------3')				
				base_image_filename = material_name+".png"
				pbr_image_filename = material_name+"_spec.dds"
				print(material_name)
				print(dir_path+"\\"+pbr_image_filename)
				base_image = bpy.data.images.load(dir_path+"\\"+base_image_filename, check_existing=True)
				shaderNodeBaseColorImageTexture.image = base_image
				pbr_image = bpy.data.images.load(dir_path+"\\"+pbr_image_filename, check_existing=True)
				shaderNodePBRImageTexture.image = pbr_image
				shaderNodePBRImageTexture.color_space = 'NONE'
				#bpy.data.images.load("/home/zeffii/Desktop/some_image.png", check_existing=True)
				print('-----------------------------------4')				
				mat.node_tree.links.new(shaderNodeBaseColorImageTexture.outputs['Color'], shaderNodePrincipled.inputs['Base Color'])	
				mat.node_tree.links.new(shaderNodePBRImageTexture.outputs['Color'], shaderNodeSeparateRGB.inputs['Image'])
				mat.node_tree.links.new(shaderNodeSeparateRGB.outputs['R'], shaderNodePrincipled.inputs['Metallic'])
				mat.node_tree.links.new(shaderNodeSeparateRGB.outputs['G'], shaderNodePrincipled.inputs['Roughness'])	
				mat.node_tree.links.new(shaderNodePrincipled.outputs['BSDF'], shaderNodeOutputMaterial.inputs['Surface'])	
				print('-----------------------------------5')								
				#principled = material.node_tree.nodes.new('Principled BSDF')
				#principled.inputs['Strength'].default_value = 5.0				
				# nodes block ends here				
				#mat.use_transparency = True
				#mat.alpha = 0
				#mat.transparency_method = 'Z_TRANSPARENCY'

				#for c in range(18):
				#	if mat.texture_slots[c] != None:
				#		mat.texture_slots.clear(c)
			tex = bpy.data.textures.get(material_name)
			if tex is None:
				# create texture
				tex = bpy.data.textures.new(name=material_name, type='IMAGE')
				#print(os.path.realpath(self.file))
				tex.image = bpy.data.images.load(dir_path+"\\"+texture_filename)
			
			slot = mat.texture_slots.add()
			slot.texture = tex	
			slot.use_map_alpha = 1

				
			object.data.materials.append(mat)
			#data = struct.unpack('{}s'.format(len(data)), data)
		
			#(l,), data = struct.unpack("I", data[:4]), data[4:]
			#s, data = data[:l], data[l:]
			#print('s: %i'%s)
			#print(data)
			
			#fmt = 'I' #D_STR_SIZE - 4 byte UINT, length of relative path to diffuse texture
			#data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			#diffuse_name_length = data[0];
			#fmt = 'I' #D_STR_SIZE - 4 byte UINT, length of relative path to diffuse texture
			#data = struct.unpack(fmt, file_object.read(struct.calcsize(fmt)))
			#diffuse_name_length = data[0];			
#next for every subset repeatedly:
#	DXMATERIAL9 struct - 68 bytes, search in net info about this struct   (search for D3DMATERIAL9 )
#			typedef struct D3DMATERIAL9 {
#			  D3DCOLORVALUE Diffuse;
#			  D3DCOLORVALUE Ambient;
#			  D3DCOLORVALUE Specular;
#			  D3DCOLORVALUE Emissive;
#			  float         Power;
#			} D3DMATERIAL9, *LPD3DMATERIAL9;
#			typedef struct _D3DCOLORVALUE {
#			  float r;
#			  float g;
#			  float b;
#			  float a;
#			} D3DCOLORVALUE;

#	D_STR_SIZE - 4 byte UINT, length of relative path to diffuse texture
#	DIFF_NAME - ansi string with D_STR_SIZE characters
#	N_STR_SIZE - 4 byte UINT, length of relative path to normal texture
#	NORM_NAME - ansi string with N_STR_SIZE characters
#	S_STR_SIZE - 4 byte UINT, length of relative path to specular texture
#	SPEC_NAME - ansi string with N_STR_SIZE characters		
		
		
		#ICOUNT	- 4 bytes UINT - count of indices in index array
		#SCOUNT	- 4 bytes UINT - count of subsets
		
		#VCOUNT	- 4 bytes UINT - count of vertices of model
		#print('header is %s'%bytes(data))
		#print('header is %s'''.join(data).strip('\0'))
		#data = struct.unpack(fmt, bytes(bytearray(file_object.read(struct.calcsize(fmt)))))[0]
		#print(data)
		#data = struct.unpack(fmt, bytes(bytearray(file_object.read(struct.calcsize(fmt)))))[0]
		#print(data)		
		#return data		
		
	#def read_h5m_header(self):
		#bytes = self.read_whole_file(self.file)
		#print(bytes)
		#return struct.unpack('3c', bytes)[0]
		#.strip('\0')

class FormatError(ValueError):
	pass

def h5m_load(file,name):
	r = H5MReader(file,name)
	r.read_whole_file()
	#r.read_h5m_header()
	#r.read_header()
	#name = r.read_header()[6:]

	
