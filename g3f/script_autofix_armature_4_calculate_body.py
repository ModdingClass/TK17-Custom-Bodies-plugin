vagina_center = getCenter (vagina_center, obj )

vagina_joint01_R_tail = getCenter (vagina_R, obj )
vagina_joint01_R_head = vagina_center.copy()
vagina_joint01_R_head.x = vagina_joint01_R_tail.x

vagina_jointEnd_R_head = vagina_joint01_R_tail.copy()
vagina_jointEnd_R_tail = vagina_joint01_R_tail.copy()
vagina_jointEnd_R_tail.x -= 0.02

vagina_joint01_L_tail = getCenter (vagina_L, obj )
vagina_joint01_L_head = vagina_center.copy()
vagina_joint01_L_head.x = vagina_joint01_L_tail.x

vagina_jointEnd_L_head = vagina_joint01_L_tail.copy()
vagina_jointEnd_L_tail = vagina_joint01_L_tail.copy()
vagina_jointEnd_L_tail.x += 0.02



anus_head = getCenter (anus_center, obj )
anus_tail = anus_head.copy()
anus_tail.x += 0.02

#############**************************************************

knee_R_center = getCenter (knee_R_hardcoded_R_X, obj )

hip_R_head = getCenter (hip_R, obj)
knee_R_head = getCenter (knee_R, obj)
ankle_R_head = getCenter (ankle_R, obj)
ball_R_head = getCenter (ball_top_R, obj)
toe_R_head = getCenter (toe_top_R, obj)
toe_R_head.y -= 0.01

hip_R_head.x = knee_R_center.x
knee_R_head.x = knee_R_center.x
ankle_R_head.x = knee_R_center.x
ball_R_head.x = knee_R_center.x
toe_R_head.x = knee_R_center.x

hip_R_tail = knee_R_head.copy()
knee_R_tail = ankle_R_head.copy()
ankle_R_tail = ball_R_head.copy()
ball_R_tail = toe_R_head.copy()
toe_R_tail = toe_R_head.copy()
toe_R_tail.x -= 0.02

toe_deform01_joint01_R_head =  getCenter (toe_deform01_base_R, obj)
toe_deform01_jointEnd_R_head =  getCenter (toe_deform01_top_R, obj)

toe_deform01_joint01_R_tail =  toe_deform01_jointEnd_R_head.copy()
toe_deform01_jointEnd_R_tail =  toe_deform01_jointEnd_R_head.copy()
toe_deform01_jointEnd_R_tail.x -= 0.02

toe_deform02_joint01_R_head =  getCenter (toe_deform02_base_R, obj)
toe_deform02_jointEnd_R_head =  getCenter (toe_deform02_top_R, obj)

toe_deform02_joint01_R_tail =  toe_deform02_jointEnd_R_head.copy()
toe_deform02_jointEnd_R_tail =  toe_deform02_jointEnd_R_head.copy()
toe_deform02_jointEnd_R_tail.x -= 0.02


knee_L_center = getCenter (knee_L_hardcoded_L_X, obj )

hip_L_head = getCenter (hip_L, obj)
knee_L_head = getCenter (knee_L, obj)
ankle_L_head = getCenter (ankle_L, obj)
ball_L_head = getCenter (ball_top_L, obj)
toe_L_head = getCenter (toe_top_L, obj)
toe_L_head.y -= 0.01

hip_L_head.x = knee_L_center.x
knee_L_head.x = knee_L_center.x
ankle_L_head.x = knee_L_center.x
ball_L_head.x = knee_L_center.x
toe_L_head.x = knee_L_center.x

hip_L_tail = knee_L_head.copy()
knee_L_tail = ankle_L_head.copy()
ankle_L_tail = ball_L_head.copy()
ball_L_tail = toe_L_head.copy()
toe_L_tail = toe_L_head.copy()
toe_L_tail.x += 0.02

toe_deform01_joint01_L_head =  getCenter (toe_deform01_base_L, obj)
toe_deform01_jointEnd_L_head =  getCenter (toe_deform01_top_L, obj)

toe_deform01_joint01_L_tail =  toe_deform01_jointEnd_L_head.copy()
toe_deform01_jointEnd_L_tail =  toe_deform01_jointEnd_L_head.copy()
toe_deform01_jointEnd_L_tail.x += 0.02

toe_deform02_joint01_L_head =  getCenter (toe_deform02_base_L, obj)
toe_deform02_jointEnd_L_head =  getCenter (toe_deform02_top_L, obj)

toe_deform02_joint01_L_tail =  toe_deform02_jointEnd_L_head.copy()
toe_deform02_jointEnd_L_tail =  toe_deform02_jointEnd_L_head.copy()
toe_deform02_jointEnd_L_tail.x += 0.02

############################################################################

clavicle_R_head = getCenter (clavicle_R, obj)
shoulder_R_head = getCenter (shoulder_R, obj)
elbow_R_head = getCenter (elbow_R, obj)
wrist_R_head = getCenter (wrist_R, obj)

forearm_R_head = Vector(( (elbow_R_head.x+wrist_R_head.x)/2 , (elbow_R_head.y+wrist_R_head.y)/2 , (elbow_R_head.z+wrist_R_head.z)/2 ))
#forearm_L_head = Vector(( (elbow_L_head.x+wrist_L_head.x)/2 , (elbow_L_head.y+wrist_L_head.y)/2 , (elbow_L_head.z+wrist_L_head.z)/2 ))

hand_R_head = getCenter (hand_R, obj)
finger01_joint01_R_head = getCenter (finger01_joint01_R, obj)
finger01_joint02_R_head = getCenter (finger01_joint02_R, obj)
finger01_joint03_R_head = getCenter (finger01_joint03_R, obj)
finger01_jointEnd_R_head = getCenter (finger01_jointEnd_R, obj)

finger02_joint01_R_head = getCenter (finger02_joint01_R, obj)
finger02_joint02_R_head = getCenter (finger02_joint02_R, obj)
finger02_joint03_R_head = getCenter (finger02_joint03_R, obj)
finger02_joint04_R_head = getCenter (finger02_joint04_R, obj)
finger02_jointEnd_R_head = getCenter (finger02_jointEnd_R, obj)

finger03_joint01_R_head = getCenter (finger03_joint01_R, obj)
finger03_joint02_R_head = getCenter (finger03_joint02_R, obj)
finger03_joint03_R_head = getCenter (finger03_joint03_R, obj)
finger03_joint04_R_head = getCenter (finger03_joint04_R, obj)
finger03_jointEnd_R_head = getCenter (finger03_jointEnd_R, obj)

finger04_joint01_R_head = getCenter (finger04_joint01_R, obj)
finger04_joint02_R_head = getCenter (finger04_joint02_R, obj)
finger04_joint03_R_head = getCenter (finger04_joint03_R, obj)
finger04_joint04_R_head = getCenter (finger04_joint04_R, obj)
finger04_jointEnd_R_head = getCenter (finger04_jointEnd_R, obj)

finger05_joint01_R_head = getCenter (finger05_joint01_R, obj)
finger05_joint02_R_head = getCenter (finger05_joint02_R, obj)
finger05_joint03_R_head = getCenter (finger05_joint03_R, obj)
finger05_joint04_R_head = getCenter (finger05_joint04_R, obj)
finger05_jointEnd_R_head = getCenter (finger05_jointEnd_R, obj)

clavicle_L_head = getCenter (clavicle_L, obj)
shoulder_L_head = getCenter (shoulder_L, obj)
elbow_L_head = getCenter (elbow_L, obj)
wrist_L_head = getCenter (wrist_L, obj)

forearm_L_head = Vector(( (elbow_L_head.x+wrist_L_head.x)/2 , (elbow_L_head.y+wrist_L_head.y)/2 , (elbow_L_head.z+wrist_L_head.z)/2 ))

hand_L_head = getCenter (hand_L, obj)
finger01_joint01_L_head = getCenter (finger01_joint01_L, obj)
finger01_joint02_L_head = getCenter (finger01_joint02_L, obj)
finger01_joint03_L_head = getCenter (finger01_joint03_L, obj)
finger01_jointEnd_L_head = getCenter (finger01_jointEnd_L, obj)

finger02_joint01_L_head = getCenter (finger02_joint01_L, obj)
finger02_joint02_L_head = getCenter (finger02_joint02_L, obj)
finger02_joint03_L_head = getCenter (finger02_joint03_L, obj)
finger02_joint04_L_head = getCenter (finger02_joint04_L, obj)
finger02_jointEnd_L_head = getCenter (finger02_jointEnd_L, obj)

finger03_joint01_L_head = getCenter (finger03_joint01_L, obj)
finger03_joint02_L_head = getCenter (finger03_joint02_L, obj)
finger03_joint03_L_head = getCenter (finger03_joint03_L, obj)
finger03_joint04_L_head = getCenter (finger03_joint04_L, obj)
finger03_jointEnd_L_head = getCenter (finger03_jointEnd_L, obj)

finger04_joint01_L_head = getCenter (finger04_joint01_L, obj)
finger04_joint02_L_head = getCenter (finger04_joint02_L, obj)
finger04_joint03_L_head = getCenter (finger04_joint03_L, obj)
finger04_joint04_L_head = getCenter (finger04_joint04_L, obj)
finger04_jointEnd_L_head = getCenter (finger04_jointEnd_L, obj)

finger05_joint01_L_head = getCenter (finger05_joint01_L, obj)
finger05_joint02_L_head = getCenter (finger05_joint02_L, obj)
finger05_joint03_L_head = getCenter (finger05_joint03_L, obj)
finger05_joint04_L_head = getCenter (finger05_joint04_L, obj)
finger05_jointEnd_L_head = getCenter (finger05_jointEnd_L, obj)


breast_joint_R_head = getCenter (breast_base_R, obj)
breast_joint_R_tail = getCenter (breast_top_R, obj)

nipple_joint01_R_head = getCenter (nipple_base_R, obj)
nipple_joint01_R_tail = getCenter (nipple_top_R, obj)

breast_scale_joint_R_head = breast_joint_R_tail
breast_scale_joint_R_tail = nipple_joint01_R_head

breast_deform01_joint01_R_head = breast_joint_R_tail
breast_deform02_joint01_R_head = breast_joint_R_tail
breast_deform02_joint01_R_head = breast_joint_R_tail

breast_deform01_joint01_R_tail = getCenter (breast_deform01_R, obj)
breast_deform02_joint01_R_tail = getCenter (breast_deform02_R, obj)
breast_deform03_joint01_R_tail = getCenter (breast_deform03_R, obj)

breast_joint_L_head = getCenter (breast_base_L, obj)
breast_joint_L_tail = getCenter (breast_top_L, obj)

nipple_joint01_L_head = getCenter (nipple_base_L, obj)
nipple_joint01_L_tail = getCenter (nipple_top_L, obj)

breast_scale_joint_L_head = breast_joint_L_tail
breast_scale_joint_L_tail = nipple_joint01_L_head

breast_deform01_joint01_L_head = breast_joint_L_tail
breast_deform02_joint01_L_head = breast_joint_L_tail
breast_deform02_joint01_L_head = breast_joint_L_tail

breast_deform01_joint01_L_tail = getCenter (breast_deform01_L, obj)
breast_deform02_joint01_L_tail = getCenter (breast_deform02_L, obj)
breast_deform03_joint01_L_tail = getCenter (breast_deform03_L, obj)


stomach_joint01_head = getCenter (stomach_base, obj)
stomach_joint01_tail = getCenter (stomach_top, obj)
stomach_joint01_head.z = stomach_joint01_tail.z
#
stomach_jointEnd_head = stomach_joint01_tail.copy()
stomach_jointEnd_tail = stomach_joint01_tail.copy()
stomach_jointEnd_tail.x += 0.02



rib_joint01_R_head = getCenter (rib_base_R, obj)
rib_joint01_R_tail = getCenter (rib_top_R, obj)
rib_jointEnd_R_head = rib_joint01_R_tail.copy()
rib_jointEnd_R_tail = rib_jointEnd_R_head.copy()
rib_jointEnd_R_tail.x += -0.02

rib_joint01_L_head = getCenter (rib_base_L, obj)
rib_joint01_L_tail = getCenter (rib_top_L, obj)
rib_jointEnd_L_head = rib_joint01_L_tail.copy()
rib_jointEnd_L_tail = rib_jointEnd_L_head.copy()
rib_jointEnd_L_tail.x += 0.02


butt_joint01_R_head = getCenter (butt_base_R, obj)
butt_joint01_R_tail = getCenter (butt_top_R, obj)
butt_joint01_R_head.z = butt_joint01_R_tail.z
butt_jointEnd_R_head = butt_joint01_R_tail
butt_jointEnd_R_tail = butt_jointEnd_R_head.copy()
butt_jointEnd_R_tail.x += -0.02

butt_joint01_L_head = getCenter (butt_base_L, obj)
butt_joint01_L_tail = getCenter (butt_top_L, obj)
butt_joint01_L_head.z = butt_joint01_L_tail.z
butt_jointEnd_L_head = butt_joint01_L_tail
butt_jointEnd_L_tail = butt_jointEnd_L_head.copy()
butt_jointEnd_L_tail.x += 0.02


