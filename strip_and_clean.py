import bpy

class StripAndClean:
    @classmethod
    def doItNow(cls, obj, vg=False, sk=False, mat=False, mod=False, all=False):
        """
        Strips the given mesh object of various properties based on the provided parameters.
        
        Parameters:
            obj (bpy.types.Object): The mesh object to be cleaned.
            vg (bool): Remove vertex groups if True. Default is False.
            sk (bool): Remove shape keys if True. Default is False.
            mat (bool): Remove materials if True. Default is False.
            mod (bool): Remove modifiers if True. Default is False.
            all (bool): If True, removes all properties regardless of other parameters. Default is False.
        """
        # If 'all' is True, override all other parameters to True
        if all:
            vg = sk = mat = mod = True
        
        # Ensure the object is a mesh
        if obj.type != 'MESH':
            print("Object {} is not a mesh. Skipping.".format(obj.name))
            return
        
        # Remove Vertex Groups if vg is True
        if vg:
            if obj.vertex_groups:
                obj.vertex_groups.clear()
                print("Removed all vertex groups from {}.".format(obj.name))
        
        # Remove Shape Keys if sk is True
        if sk:
            if obj.data.shape_keys:
                # Remove all shape keys
                obj.shape_key_clear()
                print("Removed all shape keys from {}.".format(obj.name))
        
        # Remove Materials if mat is True
        if mat:
            if obj.material_slots:
                obj.data.materials.clear()
                print("Removed all materials from {}.".format(obj.name))
        
        # Remove Modifiers if mod is True
        if mod:
            if obj.modifiers:
                for modifier in obj.modifiers:
                    obj.modifiers.remove(modifier)
                print("Removed all modifiers from {}.".format(obj.name))
        
        print("Cleaning of {} completed.".format(obj.name))

