import bpy
import sys
import os
from math import radians
from math import degrees
from os.path import join
import mathutils
import math
from mathutils import Vector
from mathutils import Matrix

from .dictionaries import *


#//	Object.Name "Model01:knee_LClips1__knee_L_initSource";
#//var :mySplineVector3f :Person" + :person + "Anim:Model01:leg_LClips1__leg_L_initSource.Curve[1] ?;
#//:mySplineVector3f.KeyValue [ (0.9113f, 0f, -0.095f), (0.9113f, 0f, -0.095f)];

#Model01:arm_L_effector ->Swrist_L_joint

def export_boilerplate_header(exportfolderpath, bodyNo):
	#
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'w+')
	header = ""
	header += "//BSB6\n"
	header += "AppModel . {\n"
	header += "\t.ComponentArray [ AppImportScene . {\n"
	header += "\t.NodeName \"Body\" + :person + \"Collision\";\n"
	header += "\t\t.ParentPath \"/Primary01\";\n"
	header += "\t\t.SceneFile \"Shared/Body/body"+bodyNo+"_collision\";\n"
	header += "\t};\n"
	header += "\n"	
	header += "\tAppScript . {\n"
	header += "\t\t.MainContext True;\n"
	header += "\t\t.Script \"\n"
	header += "\n"
	f.write(header)
	f.close()

def export_boilerplate_tail(exportfolderpath, bodyNo):
	#
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	tail = "\n"
	tail += "\t\t\t\";\n"
	tail += "\t\t};\n"
	tail += "\t];\n"
	tail += "};\n"
	f.write(tail)
	f.close()




