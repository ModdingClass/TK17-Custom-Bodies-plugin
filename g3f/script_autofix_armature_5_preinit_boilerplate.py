bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.data.objects["Armature"].select = True
bpy.context.scene.objects.active = bpy.data.objects["Armature"]
bpy.ops.object.editmode_toggle()

armature_data = bpy.data.objects['Armature']
ebones = armature_data.data.edit_bones

amw = armature_data.matrix_world
amwi = amw.inverted()

