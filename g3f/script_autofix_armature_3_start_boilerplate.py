import bpy

scene = bpy.context.scene

bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects["body_subdiv_cage"].select = True
bpy.context.scene.objects.active = bpy.data.objects["body_subdiv_cage"]
	
#bpy.ops.object.editmode_toggle()
#bpy.ops.mesh.select_all(action='DESELECT')


obj = bpy.context.active_object



