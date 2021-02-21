
############################################################
ear_L_head = getCenter (ear_base_L, obj)
ear_L_tail = getCenter (ear_tip_L, obj)
ear_jointEnd_L_head = ear_L_tail.copy()
ear_jointEnd_L_tail = ear_L_tail.copy()
ear_jointEnd_L_tail.x += 0.01

ear_R_head = getCenter (ear_base_R, obj)
ear_R_tail = getCenter (ear_tip_R, obj)
ear_jointEnd_R_head = ear_R_tail.copy()
ear_jointEnd_R_tail = ear_R_tail.copy()
ear_jointEnd_R_tail.x -= 0.01

#############################################################
cheek_joint01_L_head = getCenter (cheek_base_L, obj)
cheek_joint01_L_tail = getCenter (cheek_top_L, obj)
cheek_jointEnd_L_head = cheek_joint01_L_tail.copy()
cheek_jointEnd_L_tail = cheek_joint01_L_tail.copy()
cheek_jointEnd_L_tail.x += 0.01

cheek_joint01_R_head = getCenter (cheek_base_R, obj)
cheek_joint01_R_tail = getCenter (cheek_top_R, obj)
cheek_jointEnd_R_head = cheek_joint01_R_tail.copy()
cheek_jointEnd_R_tail = cheek_joint01_R_tail.copy()
cheek_jointEnd_R_tail.x -= 0.01

#############################################################
eye_socket_joint_L_head = getCenter (eye_socket_base_L, obj)
eye_socket_joint_L_tail = getCenter (eye_base_L, obj)
eye_socket_joint_L_head.x=eye_socket_joint_L_tail.x
eye_socket_joint_L_head.z=eye_socket_joint_L_tail.z
eye_joint_L_head = eye_socket_joint_L_tail.copy()
eye_joint_L_tail = eye_socket_joint_L_tail.copy()
eye_joint_L_tail.x += 0.01

eye_brow_joint01_L_head = getCenter (eye_brow_joint01_base_L, obj)
eye_brow_joint02_L_head = getCenter (eye_brow_joint02_base_L, obj)
eye_brow_jointEnd_L_head = getCenter (eye_brow_jointEnd_base_L, obj)
eye_brow_jointEnd_L_tail = eye_brow_jointEnd_L_head.copy()
eye_brow_jointEnd_L_tail.x += 0.01


eye_socket_joint_R_head = getCenter (eye_socket_base_R, obj)
eye_socket_joint_R_tail = getCenter (eye_base_R, obj)
eye_socket_joint_R_head.x=eye_socket_joint_R_tail.x
eye_socket_joint_R_head.z=eye_socket_joint_R_tail.z
eye_joint_R_head = eye_socket_joint_R_tail.copy()
eye_joint_R_tail = eye_socket_joint_R_tail.copy()
eye_joint_R_tail.x -= 0.01

eye_brow_joint01_R_head = getCenter (eye_brow_joint01_base_R, obj)
eye_brow_joint02_R_head = getCenter (eye_brow_joint02_base_R, obj)
eye_brow_jointEnd_R_head = getCenter (eye_brow_jointEnd_base_R, obj)
eye_brow_jointEnd_R_tail = eye_brow_jointEnd_R_head.copy()
eye_brow_jointEnd_R_tail.x -= 0.01

#############################################################
nose_joint01_head = getCenter (nose_joint01_base, obj)
nose_joint02_tail = getCenter (nose_joint02_tip, obj)
#
nose_joint01_tail = nose_joint01_head.copy()
nose_joint01_tail.z = nose_joint02_tail.z
nose_joint02_head = nose_joint01_tail.copy() 
nose_joint02_head.y = nose_joint01_head.y
#
nose_jointEnd_head = nose_joint02_tail.copy() 
nose_jointEnd_tail = nose_jointEnd_head.copy() 
nose_jointEnd_tail.x -= 0.01

forehead_joint01_head = nose_joint01_head.copy()
forehead_joint01_tail = getCenter (forehead, obj)

forehead_jointEnd_head = forehead_joint01_tail.copy()
forehead_jointEnd_tail = forehead_jointEnd_head.copy()
forehead_jointEnd_tail.x -= 0.01
#############################################################
upper_lip_joint01_L_head = getCenter (upper_lip_joint01_base_L, obj)
upper_lip_joint01_L_head.x -= 0.001
upper_lip_joint02_L_head = getCenter (upper_lip_joint02_base_L, obj)
upper_lip_joint03_L_head = getCenter (upper_lip_joint03_base_L, obj)
upper_lip_jointEnd_L_head = getCenter (upper_lip_jointEnd_center, obj)
upper_lip_jointEnd_L_head.x += 0.001 #slight adjust


upper_lip_joint01_L_tail = upper_lip_joint02_L_head.copy()
upper_lip_joint02_L_tail = upper_lip_joint03_L_head.copy()
upper_lip_joint03_L_tail = upper_lip_jointEnd_L_head.copy()
upper_lip_jointEnd_L_tail = upper_lip_jointEnd_L_head.copy()
upper_lip_jointEnd_L_tail.x += 0.005


upper_lip_joint01_R_head = getCenter (upper_lip_joint01_base_R, obj)
upper_lip_joint01_R_head.x += 0.001
upper_lip_joint02_R_head = getCenter (upper_lip_joint02_base_R, obj)
upper_lip_joint03_R_head = getCenter (upper_lip_joint03_base_R, obj)
upper_lip_jointEnd_R_head = getCenter (upper_lip_jointEnd_center, obj)
upper_lip_jointEnd_R_head.x -= 0.001 #slight adjust


upper_lip_joint01_R_tail = upper_lip_joint02_R_head.copy()
upper_lip_joint02_R_tail = upper_lip_joint03_R_head.copy()
upper_lip_joint03_R_tail = upper_lip_jointEnd_R_head.copy()
upper_lip_jointEnd_R_tail = upper_lip_jointEnd_R_head.copy()
upper_lip_jointEnd_R_tail.x -= 0.005
######################################
lower_lip_joint01_L_head = getCenter (lower_lip_joint01_base_L, obj)
lower_lip_joint01_L_head.x -= 0.001
lower_lip_joint02_L_head = getCenter (lower_lip_joint02_base_L, obj)
lower_lip_joint03_L_head = getCenter (lower_lip_joint03_base_L, obj)
lower_lip_jointEnd_L_head = getCenter (lower_lip_jointEnd_center, obj)
lower_lip_jointEnd_L_head.x += 0.001 #slight adjust

lower_lip_joint01_L_tail = lower_lip_joint02_L_head.copy()
lower_lip_joint02_L_tail = lower_lip_joint03_L_head.copy()
lower_lip_joint03_L_tail = lower_lip_jointEnd_L_head.copy()
lower_lip_jointEnd_L_tail = lower_lip_jointEnd_L_head.copy()
lower_lip_jointEnd_L_tail.x += 0.005

lower_lip_joint01_R_head = getCenter (lower_lip_joint01_base_R, obj)
lower_lip_joint01_R_head.x += 0.001
lower_lip_joint02_R_head = getCenter (lower_lip_joint02_base_R, obj)
lower_lip_joint03_R_head = getCenter (lower_lip_joint03_base_R, obj)
lower_lip_jointEnd_R_head = getCenter (lower_lip_jointEnd_center, obj)
lower_lip_jointEnd_R_head.x -= 0.001 #slight adjust

lower_lip_joint01_R_tail = lower_lip_joint02_R_head.copy()
lower_lip_joint02_R_tail = lower_lip_joint03_R_head.copy()
lower_lip_joint03_R_tail = lower_lip_jointEnd_R_head.copy()
lower_lip_jointEnd_R_tail = lower_lip_jointEnd_R_head.copy()
lower_lip_jointEnd_R_tail.x -= 0.005

#############################################################
lower_jaw_joint01_head = getCenter (lower_jaw_joint01_base, obj)
lower_jaw_jointEnd_head = getCenter (lower_jaw_jointEnd_base, obj)
chin_joint01_head = getCenter (chin01_base, obj)
chin_jointEnd_head = getCenter (chin01_tip, obj)

lower_jaw_joint01_tail = lower_jaw_jointEnd_head.copy()
lower_jaw_jointEnd_tail = chin_joint01_head.copy()
chin_joint01_tail = chin_jointEnd_head.copy()
chin_jointEnd_tail = chin_joint01_tail.copy()
chin_jointEnd_tail.x += 0.005
#############################################################

head01_head = getCenter (head_base, obj)
head01_tail = head01_head.copy()
head01_tail.z += 0.05
head02_head = head01_head.copy()
head02_tail = getCenter (head_top, obj)
head02_tail.z +=0.03
head_jointEnd_head = head02_tail.copy()
head_jointEnd_tail = head02_tail.copy()
head_jointEnd_tail.x += 0.02
##############################################################

