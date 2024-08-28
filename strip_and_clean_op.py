import bpy

class OBJECT_OT_StripAndClean(bpy.types.Operator):
    """Strip and Clean Mesh Object"""
    bl_idname = "object.strip_and_clean"
    bl_label = "Strip and Clean"
    bl_options = {'REGISTER', 'UNDO'}

    vg = bpy.props.BoolProperty(name="Remove Vertex Groups", default=False)
    sk = bpy.props.BoolProperty(name="Remove Shape Keys", default=False)
    mat = bpy.props.BoolProperty(name="Remove Materials", default=False)
    mod = bpy.props.BoolProperty(name="Remove Modifiers", default=False)
    all = bpy.props.BoolProperty(name="Remove All", default=False)

    def execute(self, context):
        obj = context.active_object
        if obj.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh.")
            return {'CANCELLED'}
        if self.all:
            vg = sk = mat = mod = True
        else:
            vg = self.vg
            sk = self.sk
            mat = self.mat
            mod = self.mod
        if vg:
            # Remove all vertex groups
            bpy.ops.object.vertex_group_remove(all=True)
            #if obj.vertex_groups:
            #    obj.vertex_groups.clear()
            self.report({'INFO'}, "Removed all vertex groups from {}.".format(obj.name))
        if sk:
            if obj.data.shape_keys:
                bpy.ops.object.shape_key_remove(all=True)
            self.report({'INFO'}, "Removed all shape keys from {}.".format(obj.name))                
            #if obj.data.shape_keys:
            #    blocks = obj.data.shape_keys.key_blocks
            #    for ind in reversed(range(len(blocks))):
            #        bl = blocks[ind]
            #        obj.shape_key_remove(bl[ind])
            #    
            #if obj.data.shape_keys:
            #    shape_keys = obj.data.shape_keys.key_blocks
            #    for i in range(len(shape_keys) - 1, -1, -1):
            #        obj.shape_key_remove(shape_keys[i])
            #    self.report({'INFO'}, "Removed all shape keys from {}.".format(obj.name))
        if mat:
            if obj.material_slots:
                obj.active_material_index = 0
                print("removing materials")
                for x in bpy.context.object.material_slots: #For all of the materials in the selected object:
                    bpy.context.object.active_material_index = 0 #select the top material
                    bpy.ops.object.material_slot_remove() 
                    #delete it                  
            self.report({'INFO'}, "Removed all materials from {}.".format(obj.name))
        if mod:
            if obj.modifiers:
                for modifier in obj.modifiers:
                    obj.modifiers.remove(modifier)
                self.report({'INFO'}, "Removed all modifiers from {}.".format(obj.name))
            self.report({'INFO'}, "Cleaning of {} completed.".format(obj.name))
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_StripAndClean)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_StripAndClean)

if __name__ == "__main__":
    register()
