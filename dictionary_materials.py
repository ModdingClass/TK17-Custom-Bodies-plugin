import bpy
import mathutils
from collections import OrderedDict

stock_materials = [
	['body_leg_lower_R','822',0],
	['body_leg_lower_L','823',1],
	['body_main_lower','824',2],
	['body_arm_lower_R','825',3],
	['body_arm_lower_L','826',4],
	['body_fingernails_R','827',5],
	['body_arm_upper_R','828',6],
	['body_arm_upper_L','829',7],
	['body_leg_upper_R','830',8],
	['body_leg_upper_L','831',9],
	['body_foot_L','832',10],
	['body_hand01_L','833',11],
	['body_genital01','834',12],
	['body_head01','835',13],
	['body_main_upper','242',14],
	['body_hand01_R','836',15],
	['body_foot_R','837',16],
	['body_fingernails_L','838',17],
	['body_eyelash01','839',18]
	#['body_teeth01','461',19],
]	

# stock_materials_ordered_dictionary = OrderedDict()
# for mat in stock_materials:
	# stock_materials_ordered_dictionary[mat[0]]={}
	# stock_materials_ordered_dictionary[mat[0]]['local']=mat[1]
	# stock_materials_ordered_dictionary[mat[0]]['index']=mat[2]


# stock_materials = [
	# ['body_teeth01','461',0],
	# ['body_leg_lower_R','822',1],
	# ['body_leg_lower_L','823',2],
	# ['body_main_lower','824',3],
	# ['body_arm_lower_R','825',4],
	# ['body_arm_lower_L','826',5],
	# ['body_fingernails_R','827',6],
	# ['body_arm_upper_R','828',7],
	# ['body_arm_upper_L','829',8],
	# ['body_leg_upper_R','830',9],
	# ['body_leg_upper_L','831',10],
	# ['body_foot_L','832',11],
	# ['body_hand01_L','833',12],
	# ['body_genital01','834',13],
	# ['body_head01','835',14],
	# ['body_main_upper','242',15],
	# ['body_hand01_R','836',16],
	# ['body_foot_R','837',17],
	# ['body_fingernails_L','838',18],
	# ['body_eyelash01','839',19]
# ]	