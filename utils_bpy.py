import bpy


#borrowed from difeomorphic utils.py
#########################################################################################
def getActiveObject(context):
	return context.scene.objects.active

def setActiveObject(ob):
	try:
		bpy.context.scene.objects.active = ob
		return True
	except RuntimeError:
		return False

def activateObject( ob):
	try:
		if bpy.context.object:
			bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.select_all(action='DESELECT')
		ob.select = True
	except RuntimeError:
		print("Could not activate", ob)
	bpy.context.scene.objects.active = ob


def deleteObject(ob):
	if ob is None:
		return
	if bpy.context.object:
		bpy.ops.object.mode_set(mode='OBJECT')
	bpy.ops.object.select_all(action='DESELECT')
	ob.select = True
	for scn in bpy.data.scenes:
		if ob in scn.objects.values():
			scn.objects.unlink(ob)
	for grp in bpy.data.groups:
		if ob.name in grp.objects:
			grp.objects.unlink(ob)
	bpy.ops.object.delete(use_global=False)
	del ob

############### ???????????????????? ################################
def toggleEditMode():
    try:
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.editmode_toggle()
    except RuntimeError:
        print("Could not update", bpy.context.object)
        pass
#########################################################################################

def getChildrenRecursive( parent, result, level, levels ):
	# Does nothing if level is reached
	if level < levels:
		# Keeps meshes
		if parent.type == 'MESH':
			result.append(parent)
		# Look over children at next level
		for child in parent.children:
			getChildrenRecursive( child, result, level + 1, levels )