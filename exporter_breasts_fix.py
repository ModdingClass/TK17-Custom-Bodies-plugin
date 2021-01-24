import sys
import os
from math import radians
from math import degrees
from os.path import join

from .dictionaries import *
import math
from mathutils import Vector
from mathutils import Matrix


def export_breasts_fix(exportfolderpath, bodyNo):
	#
	breast_R_joint = bpy.data.objects[ "_breast_R_joint"]
	breast_L_joint = bpy.data.objects[ "_breast_L_joint"]
	breast_deform02_R_jointEnd = bpy.data.objects[ "_breast_deform02_R_jointEnd"]
	breast_deform02_L_jointEnd = bpy.data.objects[ "_breast_deform02_L_jointEnd"]	
	#
	breasts_fix_string = "\n";
	#
	#breast_L_raClips1__breast_init_LSource
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:breast_L_raClips1__breast_init_LSource.Curve[2] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(breast_L_joint.location.y+ 0)    +" {:.6g}f,".format(breast_L_joint.location.z+ 0)    +" {:.6g}f".format(breast_L_joint.location.x + 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	breasts_fix_string = breasts_fix_string+snippet
	breasts_fix_string=breasts_fix_string + "\n"		
	#	
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:breast_L_raClips1__breast_init_LSource.Curve[3] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(breast_deform02_L_jointEnd.location.y+ 0)    +" {:.6g}f,".format(breast_deform02_L_jointEnd.location.z+ 0)    +" {:.6g}f".format(breast_deform02_L_jointEnd.location.x + 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	breasts_fix_string = breasts_fix_string+snippet
	breasts_fix_string=breasts_fix_string + "\n"	
	#	
	#breast_R_raClips1__breast_init_RSource
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:breast_R_raClips1__breast_init_RSource.Curve[2] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(breast_R_joint.location.y+ 0)    +" {:.6g}f,".format(breast_R_joint.location.z+ 0)    +" {:.6g}f".format(breast_R_joint.location.x + 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	breasts_fix_string = breasts_fix_string+snippet
	breasts_fix_string=breasts_fix_string + "\n"		
	#	
	snippet = "var :mySplineVector3f :Person\" + :person + \"Anim:Model01:breast_R_raClips1__breast_init_RSource.Curve[3] ?;"
	mySplineVectorString = "("+" {:.6g}f,".format(breast_deform02_R_jointEnd.location.y+ 0)    +" {:.6g}f,".format(breast_deform02_R_jointEnd.location.z+ 0)    +" {:.6g}f".format(breast_deform02_R_jointEnd.location.x + 0)   +" )"
	snippet = snippet+"\n:mySplineVector3f.KeyValue [ " + mySplineVectorString+" , "+mySplineVectorString +" ];" 
	snippet = snippet+"\ndel :mySplineVector3f;"
	breasts_fix_string = breasts_fix_string+snippet
	breasts_fix_string=breasts_fix_string + "\n"	
	#	
	print (breasts_fix_string)
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'a')
	f.write(breasts_fix_string)
	f.flush()
	f.close()


