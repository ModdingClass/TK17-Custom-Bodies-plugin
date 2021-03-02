import sys
import os
import bpy
from math import radians
from math import degrees
from os.path import join



def export_values_cleanup(exportfolderpath, bodyNo):
	file_path = exportfolderpath+"AcBody"+bodyNo+"Collision.bs"
	f = open(file_path, 'rt')
	data = f.read()
	data = data.replace('7.45058e-09f', '0.0f')
	data = data.replace('1.49012e-08f', '0.0f')
	data = data.replace('2.98023e-08f', '0.0f')
	data = data.replace('5.96046e-08f', '0.0f')
	data = data.replace('0.00000000f', '0.0f').replace('0.000000f', '0.0f').replace('-0.0f', '0.0f') 
	f.close()
	f=open(file_path, "wt")
	f.write(data)
	f.flush()
	f.close()


