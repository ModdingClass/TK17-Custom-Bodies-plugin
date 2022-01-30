import sys
import os
from math import radians
from math import degrees
from os.path import join

from .ik_tools import *
from .dictionaries import *
import math
from mathutils import Vector
from mathutils import Matrix
from mathutils.geometry import intersect_point_line



def export_spine_fix(exportfolderpath, bodyNo):
    #
    #
    spineCVArray = []
    spine_fix_string = "\n";

    #
    
    spine_joint01 = bpy.data.objects[ "_spine_joint01"]
    spine_joint02 = bpy.data.objects[ "_spine_joint02"]
    spine_joint03 = bpy.data.objects[ "_spine_joint03"]
    spine_joint04 = bpy.data.objects[ "_spine_joint04"]
    spine_jointEnd = bpy.data.objects[ "_spine_jointEnd"]
    neck_joint01 = bpy.data.objects[ "_neck_joint01"]

    #help_spine_group01
    values = spine_joint01.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group01"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(-values.x + 0)    +" {:.6f}f,".format(-values.z + 0)    +" {:.6f}f".format(values.y + 0)   +" );\n"   # -1*(xz-y)
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #
    #help_spine_group02
    values = spine_joint01.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group02"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle01
    values = spine_joint01.matrix_world.translation
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle01"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle01Shape
    values = spine_joint01.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle01Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #
    #
    #help_spine_group03
    loc0 = spine_joint01.matrix_world.translation
    loc1 = spine_joint02.matrix_world.translation
    length = (loc0 - loc1).length
    move_up_one_third_transformation_local =    Vector([0,length/3,0]) 
    move_up_one_third_transformation_world = spine_joint01.matrix_world.to_3x3() * move_up_one_third_transformation_local  
    values = spine_joint01.matrix_world.translation + move_up_one_third_transformation_world  
    #bpy.context.scene.cursor_location = values
    #
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group03"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #
    #spine_clusterHandle02
    #values already calculated above
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle02"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle02Shape
    #values already calculated above
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle02Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #

    #help_spine_group04
    values = spine_joint02.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group04"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle03
    values = spine_joint02.matrix_world.translation
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle03"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle03Shape
    values = spine_joint02.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle03Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  



    #help_spine_group05
    values = spine_joint03.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group05"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle04
    values = spine_joint03.matrix_world.translation
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle04"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle04Shape
    values = spine_joint03.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle04Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  





    #help_spine_group06
    values = spine_joint04.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group06"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle05
    values = spine_joint04.matrix_world.translation
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle05"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle05Shape
    values = spine_joint04.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle05Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  


    #help_spine_group07
    values = spine_jointEnd.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group07"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle06
    values = spine_jointEnd.matrix_world.translation
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle06"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle06Shape
    values = spine_jointEnd.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle06Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  


    #help_spine_group08
    loc0 = spine_jointEnd.matrix_world.translation
    loc1 = neck_joint01.matrix_world.translation
    length = (loc0 - loc1).length
    move_up_one_third_transformation_local =    Vector([0,length/3*2,0]) 
    move_up_one_third_transformation_world = spine_jointEnd.matrix_world.to_3x3() * move_up_one_third_transformation_local  
    values = spine_jointEnd.matrix_world.translation + move_up_one_third_transformation_world  
    #bpy.context.scene.cursor_location = values
    #
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_group08"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #
    #spine_clusterHandle07
    #values already calculated above
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle07"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle07Shape
    #values already calculated above
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle07Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #


    #help_spine_groupEnd
    values = neck_joint01.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"help_spine_groupEnd"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle08
    values = neck_joint01.matrix_world.translation
    spineCVArray.append(values)
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle08"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.ScalingPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.RotationPivot ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"   #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"    
    #spine_clusterHandle08Shape
    values = neck_joint01.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_clusterHandle08Shape"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Origin ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  


    #spine_ikHandle
    values = neck_joint01.matrix_world.translation
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_ikHandle"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(values.x + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(-values.y + 0)   +" );\n"       #xz-y
    snippet = snippet+ "\t.Rotation ("        +" {:.6f}f,".format(180)    +" {:.6f}f,".format(0.2126652)    +" {:.6f}f".format(90)   +" );\n"       #xz-y    
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  

    #spine_effector
    values = neck_joint01.location
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_effector"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.Translation ("        +" {:.6f}f,".format(values.y + 0)    +" {:.6f}f,".format(values.z + 0)    +" {:.6f}f".format(values.x + 0)   +" );\n"       # yzx just like joints in exporter_empties_0.py
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  


    #
    #spine_splineShapeOrig
    len1 = (spine_joint01.matrix_world.translation - spine_joint02.matrix_world.translation).length
    len2 = len1+(spine_joint02.matrix_world.translation - spine_joint03.matrix_world.translation).length
    len3 = len2+(spine_joint03.matrix_world.translation - spine_joint04.matrix_world.translation).length
    len4 = len3+(spine_joint04.matrix_world.translation - spine_jointEnd.matrix_world.translation).length
    len5 = len3+(spine_jointEnd.matrix_world.translation - neck_joint01.matrix_world.translation).length
    spine_knots = [
	0,
    0,
    0,
    len1,
    len2,
    len3,
    len4,
    len5,
    len5,
    len5]
    knotstr = str([ "{:.6f}f".format(float(i)) for i in spine_knots ])
    knotstr = knotstr.replace("-0.000000f", "0.0f").replace("0.000000f", "0.0f").replace("-1.000000f", "-1.0f").replace("1.000000f", "1.0f").replace("'", "").replace("[", "").replace("]", "")
    cvarraystr = str([ "( {:.6f}f, {:.6f}f, {:.6f}f ) ".format(float(v[0]+0),float(v[2]+0),float(-v[1]+0)) for v in spineCVArray ])
    cvarraystr = cvarraystr.replace("-0.000000f", "0.0f").replace("0.000000f", "0.0f").replace("-1.000000f", "-1.0f").replace("1.000000f", "1.0f").replace("'", "").replace("[", "").replace("]", "")
    snippet = ":Person\" + :person + \"Anim:Model01:"
    snippet = snippet+"spine_splineShapeOrig"
    snippet = snippet + ".SNode? . {\n";
    snippet = snippet+ "\t.KnotArray [ "         +knotstr +" ] ;\n"       # yzx just like joints in exporter_empties_0.py
    snippet = snippet+ "\t.CVArray [ "         +cvarraystr +" ] ;\n"       # yzx just like joints in exporter_empties_0.py
    snippet = snippet+ "};\n"
    spine_fix_string = spine_fix_string+snippet + "\n"  

    print (spine_fix_string)
    file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
    f = open(file_path, 'a')
    f.write(spine_fix_string)
    f.flush()
    f.close()



