
ebones["vagina_joint01.R"].head = amwi * vagina_joint01_R_head
ebones["vagina_joint01.R"].tail = amwi * vagina_joint01_R_tail

ebones["vagina_jointEnd.R"].head = amwi * vagina_jointEnd_R_head
ebones["vagina_jointEnd.R"].tail = amwi * vagina_jointEnd_R_tail

ebones["vagina_joint01.L"].head = amwi * vagina_joint01_L_head
ebones["vagina_joint01.L"].tail = amwi * vagina_joint01_L_tail

ebones["vagina_jointEnd.L"].head = amwi * vagina_jointEnd_L_head
ebones["vagina_jointEnd.L"].tail = amwi * vagina_jointEnd_L_tail

#########################################################################

ebones["anus_joint"].head = amwi * anus_head
ebones["anus_joint"].tail = amwi * anus_tail

ebones["hip_joint.R"].head = amwi * hip_R_head
ebones["hip_joint.R"].tail = amwi * knee_R_head

ebones["knee_joint.R"].head = amwi * knee_R_head
ebones["knee_joint.R"].tail = amwi * ankle_R_head

ebones["ankle_joint.R"].head = amwi * ankle_R_head
ebones["ankle_joint.R"].tail = amwi * ankle_R_tail

ebones["ball_joint.R"].head = amwi * ball_R_head
ebones["ball_joint.R"].tail = amwi * ball_R_tail

ebones["toe_joint.R"].head = amwi * toe_R_head
ebones["toe_joint.R"].tail = amwi * toe_R_tail


ebones["ball_joint.R"].length /=2


ebones["toe_deform01_joint01.R"].head = amwi * toe_deform01_joint01_R_head
ebones["toe_deform01_joint01.R"].tail = amwi * toe_deform01_joint01_R_tail

ebones["toe_deform01_jointEnd.R"].head = amwi * toe_deform01_jointEnd_R_head
ebones["toe_deform01_jointEnd.R"].tail = amwi * toe_deform01_jointEnd_R_tail

ebones["toe_deform02_joint01.R"].head = amwi * toe_deform02_joint01_R_head
ebones["toe_deform02_joint01.R"].tail = amwi * toe_deform02_joint01_R_tail

ebones["toe_deform02_jointEnd.R"].head = amwi * toe_deform02_jointEnd_R_head
ebones["toe_deform02_jointEnd.R"].tail = amwi * toe_deform02_jointEnd_R_tail


ebones["hip_joint.L"].head = amwi * hip_L_head
ebones["hip_joint.L"].tail = amwi * knee_L_head

ebones["knee_joint.L"].head = amwi * knee_L_head
ebones["knee_joint.L"].tail = amwi * ankle_L_head

ebones["ankle_joint.L"].head = amwi * ankle_L_head
ebones["ankle_joint.L"].tail = amwi * ankle_L_tail

ebones["ball_joint.L"].head = amwi * ball_L_head
ebones["ball_joint.L"].tail = amwi * ball_L_tail

ebones["toe_joint.L"].head = amwi * toe_L_head
ebones["toe_joint.L"].tail = amwi * toe_L_tail


ebones["ball_joint.L"].length /=2


ebones["toe_deform01_joint01.L"].head = amwi * toe_deform01_joint01_L_head
ebones["toe_deform01_joint01.L"].tail = amwi * toe_deform01_joint01_L_tail

ebones["toe_deform01_jointEnd.L"].head = amwi * toe_deform01_jointEnd_L_head
ebones["toe_deform01_jointEnd.L"].tail = amwi * toe_deform01_jointEnd_L_tail

ebones["toe_deform02_joint01.L"].head = amwi * toe_deform02_joint01_L_head
ebones["toe_deform02_joint01.L"].tail = amwi * toe_deform02_joint01_L_tail

ebones["toe_deform02_jointEnd.L"].head = amwi * toe_deform02_jointEnd_L_head
ebones["toe_deform02_jointEnd.L"].tail = amwi * toe_deform02_jointEnd_L_tail


#right hand
ebones["clavicle_joint.R"].head = amwi * clavicle_R_head
ebones["clavicle_joint.R"].tail = amwi * shoulder_R_head

ebones["shoulder_joint.R"].head = amwi * shoulder_R_head
ebones["shoulder_joint.R"].tail = amwi * elbow_R_head

ebones["elbow_joint.R"].head = amwi * elbow_R_head
ebones["elbow_joint.R"].tail = amwi * forearm_R_head

ebones["forearm_joint.R"].head = amwi * forearm_R_head
ebones["forearm_joint.R"].tail = amwi * wrist_R_head

ebones["wrist_joint.R"].head = amwi * wrist_R_head
ebones["wrist_joint.R"].tail = amwi * hand_R_head

ebones["finger01_joint01.R"].head = amwi * finger01_joint01_R_head
ebones["finger01_joint01.R"].tail = amwi * finger01_joint02_R_head

ebones["finger01_joint02.R"].head = amwi * finger01_joint02_R_head
ebones["finger01_joint02.R"].tail = amwi * finger01_joint03_R_head

ebones["finger01_joint03.R"].head = amwi * finger01_joint03_R_head
ebones["finger01_joint03.R"].tail = amwi * finger01_jointEnd_R_head

ebones["finger01_jointEnd.R"].head = amwi * finger01_jointEnd_R_head
ebones["finger01_jointEnd.R"].tail = amwi * finger01_jointEnd_R_head + Vector ((0,0,0.005))

#############
ebones["finger02_joint01.R"].head = amwi * finger02_joint01_R_head
ebones["finger02_joint01.R"].tail = amwi * finger02_joint02_R_head

ebones["finger02_joint02.R"].head = amwi * finger02_joint02_R_head
ebones["finger02_joint02.R"].tail = amwi * finger02_joint03_R_head

ebones["finger02_joint03.R"].head = amwi * finger02_joint03_R_head
ebones["finger02_joint03.R"].tail = amwi * finger02_joint04_R_head

ebones["finger02_joint04.R"].head = amwi * finger02_joint04_R_head
ebones["finger02_joint04.R"].tail = amwi * finger02_jointEnd_R_head


ebones["finger02_jointEnd.R"].head = amwi * finger02_jointEnd_R_head
ebones["finger02_jointEnd.R"].tail = amwi * finger02_jointEnd_R_head + Vector ((0,0,0.005))

#############
ebones["finger03_joint01.R"].head = amwi * finger03_joint01_R_head
ebones["finger03_joint01.R"].tail = amwi * finger03_joint02_R_head

ebones["finger03_joint02.R"].head = amwi * finger03_joint02_R_head
ebones["finger03_joint02.R"].tail = amwi * finger03_joint03_R_head

ebones["finger03_joint03.R"].head = amwi * finger03_joint03_R_head
ebones["finger03_joint03.R"].tail = amwi * finger03_joint04_R_head

ebones["finger03_joint04.R"].head = amwi * finger03_joint04_R_head
ebones["finger03_joint04.R"].tail = amwi * finger03_jointEnd_R_head


ebones["finger03_jointEnd.R"].head = amwi * finger03_jointEnd_R_head
ebones["finger03_jointEnd.R"].tail = amwi * finger03_jointEnd_R_head + Vector ((0,0,0.005))

#############
ebones["finger04_joint01.R"].head = amwi * finger04_joint01_R_head
ebones["finger04_joint01.R"].tail = amwi * finger04_joint02_R_head

ebones["finger04_joint02.R"].head = amwi * finger04_joint02_R_head
ebones["finger04_joint02.R"].tail = amwi * finger04_joint03_R_head

ebones["finger04_joint03.R"].head = amwi * finger04_joint03_R_head
ebones["finger04_joint03.R"].tail = amwi * finger04_joint04_R_head

ebones["finger04_joint04.R"].head = amwi * finger04_joint04_R_head
ebones["finger04_joint04.R"].tail = amwi * finger04_jointEnd_R_head


ebones["finger04_jointEnd.R"].head = amwi * finger04_jointEnd_R_head
ebones["finger04_jointEnd.R"].tail = amwi * finger04_jointEnd_R_head + Vector ((0,0,0.005))

#############
ebones["finger05_joint01.R"].head = amwi * finger05_joint01_R_head
ebones["finger05_joint01.R"].tail = amwi * finger05_joint02_R_head

ebones["finger05_joint02.R"].head = amwi * finger05_joint02_R_head
ebones["finger05_joint02.R"].tail = amwi * finger05_joint03_R_head

ebones["finger05_joint03.R"].head = amwi * finger05_joint03_R_head
ebones["finger05_joint03.R"].tail = amwi * finger05_joint04_R_head

ebones["finger05_joint04.R"].head = amwi * finger05_joint04_R_head
ebones["finger05_joint04.R"].tail = amwi * finger05_jointEnd_R_head


ebones["finger05_jointEnd.R"].head = amwi * finger05_jointEnd_R_head
ebones["finger05_jointEnd.R"].tail = amwi * finger05_jointEnd_R_head + Vector ((0,0,0.005))


# fix right fingers on a straight line

finger_joint02_length = (ebones["finger02_joint02.R"].tail - ebones["finger02_joint02.R"].head).length
finger_joint03_length = (ebones["finger02_joint03.R"].tail - ebones["finger02_joint03.R"].head).length
finger_joint04_length = (ebones["finger02_joint04.R"].tail - ebones["finger02_joint04.R"].head).length

fingers_new_length = (ebones["finger02_jointEnd.R"].head - ebones["finger02_joint02.R"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger02_joint02.R"].head = ebones["finger02_joint02.R"].head
ebones["finger02_joint02.R"].tail = ebones["finger02_jointEnd.R"].head.copy()
ebones["finger02_joint02.R"].length = fingers_new_length * finger_joint02_scale 

ebones["finger02_joint03.R"].head = ebones["finger02_joint02.R"].tail
ebones["finger02_joint03.R"].tail = ebones["finger02_jointEnd.R"].head
ebones["finger02_joint03.R"].length = fingers_new_length * finger_joint03_scale

ebones["finger02_joint04.R"].head = ebones["finger02_joint03.R"].tail
ebones["finger02_joint04.R"].tail = ebones["finger02_jointEnd.R"].head
ebones["finger02_joint04.R"].length = fingers_new_length * finger_joint04_scale


finger_joint02_length = (ebones["finger03_joint02.R"].tail - ebones["finger03_joint02.R"].head).length
finger_joint03_length = (ebones["finger03_joint03.R"].tail - ebones["finger03_joint03.R"].head).length
finger_joint04_length = (ebones["finger03_joint04.R"].tail - ebones["finger03_joint04.R"].head).length

fingers_new_length = (ebones["finger03_jointEnd.R"].head - ebones["finger03_joint02.R"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger03_joint02.R"].head = ebones["finger03_joint02.R"].head
ebones["finger03_joint02.R"].tail = ebones["finger03_jointEnd.R"].head.copy()
ebones["finger03_joint02.R"].length = fingers_new_length * finger_joint02_scale 

ebones["finger03_joint03.R"].head = ebones["finger03_joint02.R"].tail
ebones["finger03_joint03.R"].tail = ebones["finger03_jointEnd.R"].head
ebones["finger03_joint03.R"].length = fingers_new_length * finger_joint03_scale

ebones["finger03_joint04.R"].head = ebones["finger03_joint03.R"].tail
ebones["finger03_joint04.R"].tail = ebones["finger03_jointEnd.R"].head
ebones["finger03_joint04.R"].length = fingers_new_length * finger_joint04_scale

finger_joint02_length = (ebones["finger04_joint02.R"].tail - ebones["finger04_joint02.R"].head).length
finger_joint03_length = (ebones["finger04_joint03.R"].tail - ebones["finger04_joint03.R"].head).length
finger_joint04_length = (ebones["finger04_joint04.R"].tail - ebones["finger04_joint04.R"].head).length

fingers_new_length = (ebones["finger04_jointEnd.R"].head - ebones["finger04_joint02.R"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger04_joint02.R"].head = ebones["finger04_joint02.R"].head
ebones["finger04_joint02.R"].tail = ebones["finger04_jointEnd.R"].head.copy()
ebones["finger04_joint02.R"].length = fingers_new_length * finger_joint02_scale 

ebones["finger04_joint03.R"].head = ebones["finger04_joint02.R"].tail
ebones["finger04_joint03.R"].tail = ebones["finger04_jointEnd.R"].head
ebones["finger04_joint03.R"].length = fingers_new_length * finger_joint03_scale

ebones["finger04_joint04.R"].head = ebones["finger04_joint03.R"].tail
ebones["finger04_joint04.R"].tail = ebones["finger04_jointEnd.R"].head
ebones["finger04_joint04.R"].length = fingers_new_length * finger_joint04_scale


finger_joint02_length = (ebones["finger05_joint02.R"].tail - ebones["finger05_joint02.R"].head).length
finger_joint03_length = (ebones["finger05_joint03.R"].tail - ebones["finger05_joint03.R"].head).length
finger_joint04_length = (ebones["finger05_joint04.R"].tail - ebones["finger05_joint04.R"].head).length

fingers_new_length = (ebones["finger05_jointEnd.R"].head - ebones["finger05_joint02.R"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger05_joint02.R"].head = ebones["finger05_joint02.R"].head
ebones["finger05_joint02.R"].tail = ebones["finger05_jointEnd.R"].head.copy()
ebones["finger05_joint02.R"].length = fingers_new_length * finger_joint02_scale 

ebones["finger05_joint03.R"].head = ebones["finger05_joint02.R"].tail
ebones["finger05_joint03.R"].tail = ebones["finger05_jointEnd.R"].head
ebones["finger05_joint03.R"].length = fingers_new_length * finger_joint03_scale

ebones["finger05_joint04.R"].head = ebones["finger05_joint03.R"].tail
ebones["finger05_joint04.R"].tail = ebones["finger05_jointEnd.R"].head
ebones["finger05_joint04.R"].length = fingers_new_length * finger_joint04_scale

#left hand
ebones["clavicle_joint.L"].head = amwi * clavicle_L_head
ebones["clavicle_joint.L"].tail = amwi * shoulder_L_head

ebones["shoulder_joint.L"].head = amwi * shoulder_L_head
ebones["shoulder_joint.L"].tail = amwi * elbow_L_head

ebones["elbow_joint.L"].head = amwi * elbow_L_head
ebones["elbow_joint.L"].tail = amwi * forearm_L_head

ebones["forearm_joint.L"].head = amwi * forearm_L_head
ebones["forearm_joint.L"].tail = amwi * wrist_L_head

ebones["wrist_joint.L"].head = amwi * wrist_L_head
ebones["wrist_joint.L"].tail = amwi * hand_L_head

ebones["finger01_joint01.L"].head = amwi * finger01_joint01_L_head
ebones["finger01_joint01.L"].tail = amwi * finger01_joint02_L_head

ebones["finger01_joint02.L"].head = amwi * finger01_joint02_L_head
ebones["finger01_joint02.L"].tail = amwi * finger01_joint03_L_head

ebones["finger01_joint03.L"].head = amwi * finger01_joint03_L_head
ebones["finger01_joint03.L"].tail = amwi * finger01_jointEnd_L_head

ebones["finger01_jointEnd.L"].head = amwi * finger01_jointEnd_L_head
ebones["finger01_jointEnd.L"].tail = amwi * finger01_jointEnd_L_head + Vector ((0,0,0.005))

#############
ebones["finger02_joint01.L"].head = amwi * finger02_joint01_L_head
ebones["finger02_joint01.L"].tail = amwi * finger02_joint02_L_head

ebones["finger02_joint02.L"].head = amwi * finger02_joint02_L_head
ebones["finger02_joint02.L"].tail = amwi * finger02_joint03_L_head

ebones["finger02_joint03.L"].head = amwi * finger02_joint03_L_head
ebones["finger02_joint03.L"].tail = amwi * finger02_joint04_L_head

ebones["finger02_joint04.L"].head = amwi * finger02_joint04_L_head
ebones["finger02_joint04.L"].tail = amwi * finger02_jointEnd_L_head


ebones["finger02_jointEnd.L"].head = amwi * finger02_jointEnd_L_head
ebones["finger02_jointEnd.L"].tail = amwi * finger02_jointEnd_L_head + Vector ((0,0,0.005))


#armature_data = bpy.data.objects['Armature']
#ebones = armature_data.data.edit_bones


#############
ebones["finger03_joint01.L"].head = amwi * finger03_joint01_L_head
ebones["finger03_joint01.L"].tail = amwi * finger03_joint02_L_head

ebones["finger03_joint02.L"].head = amwi * finger03_joint02_L_head
ebones["finger03_joint02.L"].tail = amwi * finger03_joint03_L_head

ebones["finger03_joint03.L"].head = amwi * finger03_joint03_L_head
ebones["finger03_joint03.L"].tail = amwi * finger03_joint04_L_head

ebones["finger03_joint04.L"].head = amwi * finger03_joint04_L_head
ebones["finger03_joint04.L"].tail = amwi * finger03_jointEnd_L_head


ebones["finger03_jointEnd.L"].head = amwi * finger03_jointEnd_L_head
ebones["finger03_jointEnd.L"].tail = amwi * finger03_jointEnd_L_head + Vector ((0,0,0.005))


#############
ebones["finger04_joint01.L"].head = amwi * finger04_joint01_L_head
ebones["finger04_joint01.L"].tail = amwi * finger04_joint02_L_head

ebones["finger04_joint02.L"].head = amwi * finger04_joint02_L_head
ebones["finger04_joint02.L"].tail = amwi * finger04_joint03_L_head

ebones["finger04_joint03.L"].head = amwi * finger04_joint03_L_head
ebones["finger04_joint03.L"].tail = amwi * finger04_joint04_L_head

ebones["finger04_joint04.L"].head = amwi * finger04_joint04_L_head
ebones["finger04_joint04.L"].tail = amwi * finger04_jointEnd_L_head


ebones["finger04_jointEnd.L"].head = amwi * finger04_jointEnd_L_head
ebones["finger04_jointEnd.L"].tail = amwi * finger04_jointEnd_L_head + Vector ((0,0,0.005))


#############
ebones["finger05_joint01.L"].head = amwi * finger05_joint01_L_head
ebones["finger05_joint01.L"].tail = amwi * finger05_joint02_L_head

ebones["finger05_joint02.L"].head = amwi * finger05_joint02_L_head
ebones["finger05_joint02.L"].tail = amwi * finger05_joint03_L_head

ebones["finger05_joint03.L"].head = amwi * finger05_joint03_L_head
ebones["finger05_joint03.L"].tail = amwi * finger05_joint04_L_head

ebones["finger05_joint04.L"].head = amwi * finger05_joint04_L_head
ebones["finger05_joint04.L"].tail = amwi * finger05_jointEnd_L_head


ebones["finger05_jointEnd.L"].head = amwi * finger05_jointEnd_L_head
ebones["finger05_jointEnd.L"].tail = amwi * finger05_jointEnd_L_head + Vector ((0,0,0.005))

# fix left fingers on a straight line

finger_joint02_length = (ebones["finger02_joint02.L"].tail - ebones["finger02_joint02.L"].head).length
finger_joint03_length = (ebones["finger02_joint03.L"].tail - ebones["finger02_joint03.L"].head).length
finger_joint04_length = (ebones["finger02_joint04.L"].tail - ebones["finger02_joint04.L"].head).length

fingers_new_length = (ebones["finger02_jointEnd.L"].head - ebones["finger02_joint02.L"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger02_joint02.L"].head = ebones["finger02_joint02.L"].head
ebones["finger02_joint02.L"].tail = ebones["finger02_jointEnd.L"].head.copy()
ebones["finger02_joint02.L"].length = fingers_new_length * finger_joint02_scale 

ebones["finger02_joint03.L"].head = ebones["finger02_joint02.L"].tail
ebones["finger02_joint03.L"].tail = ebones["finger02_jointEnd.L"].head
ebones["finger02_joint03.L"].length = fingers_new_length * finger_joint03_scale

ebones["finger02_joint04.L"].head = ebones["finger02_joint03.L"].tail
ebones["finger02_joint04.L"].tail = ebones["finger02_jointEnd.L"].head
ebones["finger02_joint04.L"].length = fingers_new_length * finger_joint04_scale


finger_joint02_length = (ebones["finger03_joint02.L"].tail - ebones["finger03_joint02.L"].head).length
finger_joint03_length = (ebones["finger03_joint03.L"].tail - ebones["finger03_joint03.L"].head).length
finger_joint04_length = (ebones["finger03_joint04.L"].tail - ebones["finger03_joint04.L"].head).length

fingers_new_length = (ebones["finger03_jointEnd.L"].head - ebones["finger03_joint02.L"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger03_joint02.L"].head = ebones["finger03_joint02.L"].head
ebones["finger03_joint02.L"].tail = ebones["finger03_jointEnd.L"].head.copy()
ebones["finger03_joint02.L"].length = fingers_new_length * finger_joint02_scale 

ebones["finger03_joint03.L"].head = ebones["finger03_joint02.L"].tail
ebones["finger03_joint03.L"].tail = ebones["finger03_jointEnd.L"].head
ebones["finger03_joint03.L"].length = fingers_new_length * finger_joint03_scale

ebones["finger03_joint04.L"].head = ebones["finger03_joint03.L"].tail
ebones["finger03_joint04.L"].tail = ebones["finger03_jointEnd.L"].head
ebones["finger03_joint04.L"].length = fingers_new_length * finger_joint04_scale

finger_joint02_length = (ebones["finger04_joint02.L"].tail - ebones["finger04_joint02.L"].head).length
finger_joint03_length = (ebones["finger04_joint03.L"].tail - ebones["finger04_joint03.L"].head).length
finger_joint04_length = (ebones["finger04_joint04.L"].tail - ebones["finger04_joint04.L"].head).length

fingers_new_length = (ebones["finger04_jointEnd.L"].head - ebones["finger04_joint02.L"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger04_joint02.L"].head = ebones["finger04_joint02.L"].head
ebones["finger04_joint02.L"].tail = ebones["finger04_jointEnd.L"].head.copy()
ebones["finger04_joint02.L"].length = fingers_new_length * finger_joint02_scale 

ebones["finger04_joint03.L"].head = ebones["finger04_joint02.L"].tail
ebones["finger04_joint03.L"].tail = ebones["finger04_jointEnd.L"].head
ebones["finger04_joint03.L"].length = fingers_new_length * finger_joint03_scale

ebones["finger04_joint04.L"].head = ebones["finger04_joint03.L"].tail
ebones["finger04_joint04.L"].tail = ebones["finger04_jointEnd.L"].head
ebones["finger04_joint04.L"].length = fingers_new_length * finger_joint04_scale


finger_joint02_length = (ebones["finger05_joint02.L"].tail - ebones["finger05_joint02.L"].head).length
finger_joint03_length = (ebones["finger05_joint03.L"].tail - ebones["finger05_joint03.L"].head).length
finger_joint04_length = (ebones["finger05_joint04.L"].tail - ebones["finger05_joint04.L"].head).length

fingers_new_length = (ebones["finger05_jointEnd.L"].head - ebones["finger05_joint02.L"].head).length
fingers_old_length =  finger_joint02_length + finger_joint03_length + finger_joint04_length
finger_joint02_scale = finger_joint02_length/fingers_old_length
finger_joint03_scale = finger_joint03_length/fingers_old_length
finger_joint04_scale = finger_joint04_length/fingers_old_length



ebones["finger05_joint02.L"].head = ebones["finger05_joint02.L"].head
ebones["finger05_joint02.L"].tail = ebones["finger05_jointEnd.L"].head.copy()
ebones["finger05_joint02.L"].length = fingers_new_length * finger_joint02_scale 

ebones["finger05_joint03.L"].head = ebones["finger05_joint02.L"].tail
ebones["finger05_joint03.L"].tail = ebones["finger05_jointEnd.L"].head
ebones["finger05_joint03.L"].length = fingers_new_length * finger_joint03_scale

ebones["finger05_joint04.L"].head = ebones["finger05_joint03.L"].tail
ebones["finger05_joint04.L"].tail = ebones["finger05_jointEnd.L"].head
ebones["finger05_joint04.L"].length = fingers_new_length * finger_joint04_scale

#breast R

ebones["breast_joint.R"].head = amwi * breast_joint_R_head
ebones["breast_joint.R"].tail = amwi * breast_joint_R_tail

ebones["breast_scale_joint.R"].head = amwi * breast_scale_joint_R_head #actual breast_joint_R_tail
ebones["breast_scale_joint.R"].tail = amwi * breast_scale_joint_R_tail #actual nipple_joint01_R_head


ebones["nipple_joint01.R"].head = amwi * nipple_joint01_R_head
ebones["nipple_joint01.R"].tail = amwi * nipple_joint01_R_tail

#lets make the nipple twice distance to get the jointEnd tail then correct it back
ebones["nipple_joint01.R"].length *= 2
nipple_joint01_R_tail_doubled = ebones["nipple_joint01.R"].tail.copy()
ebones["nipple_joint01.R"].length /= 2

ebones["nipple_jointEnd.R"].head = amwi * nipple_joint01_R_tail
ebones["nipple_jointEnd.R"].tail = nipple_joint01_R_tail_doubled

#deform01
ebones["breast_deform01_joint01.R"].head = amwi * breast_joint_R_tail
ebones["breast_deform01_joint01.R"].tail = amwi * breast_deform01_joint01_R_tail
deform01_length = ebones["breast_deform01_joint01.R"].length
ebones["breast_deform01_joint01.R"].length += 	deform01_length*0.1							#make the tail a bit longer
breast_deform01_joint01_R_tail_longer = ebones["breast_deform01_joint01.R"].tail.copy()
ebones["breast_deform01_joint01.R"].length -= 	deform01_length*0.1							#fix the tail
#ebones["breast_deform01_joint01.R"].tail = amwi * breast_deform01_joint01_R_tail 	

ebones["breast_deform01_jointEnd.R"].head = amwi * breast_deform01_joint01_R_tail
ebones["breast_deform01_jointEnd.R"].tail = breast_deform01_joint01_R_tail_longer

#deform02
ebones["breast_deform02_joint01.R"].head = amwi * breast_joint_R_tail
ebones["breast_deform02_joint01.R"].tail = amwi * breast_deform02_joint01_R_tail
deform02_length = ebones["breast_deform02_joint01.R"].length
ebones["breast_deform02_joint01.R"].length += 	deform02_length*0.1							#make the tail a bit longer
breast_deform02_joint01_R_tail_longer = ebones["breast_deform02_joint01.R"].tail.copy()
ebones["breast_deform02_joint01.R"].length -= 	deform02_length*0.1							#fix the tail
#ebones["breast_deform02_joint01.R"].tail = amwi * breast_deform02_joint01_R_tail 	

ebones["breast_deform02_jointEnd.R"].head = amwi * breast_deform02_joint01_R_tail
ebones["breast_deform02_jointEnd.R"].tail = breast_deform02_joint01_R_tail_longer

#deform03
ebones["breast_deform03_joint01.R"].head = amwi * breast_joint_R_tail
ebones["breast_deform03_joint01.R"].tail = amwi * breast_deform03_joint01_R_tail
deform03_length = ebones["breast_deform03_joint01.R"].length
ebones["breast_deform03_joint01.R"].length += 	deform03_length*0.1							#make the tail a bit longer
breast_deform03_joint01_R_tail_longer = ebones["breast_deform03_joint01.R"].tail.copy()
ebones["breast_deform03_joint01.R"].length -= 	deform03_length*0.1							#fix the tail
#ebones["breast_deform03_joint01.R"].tail = amwi * breast_deform03_joint01_R_tail 	

ebones["breast_deform03_jointEnd.R"].head = amwi * breast_deform03_joint01_R_tail
ebones["breast_deform03_jointEnd.R"].tail = breast_deform03_joint01_R_tail_longer

#breast L

ebones["breast_joint.L"].head = amwi * breast_joint_L_head
ebones["breast_joint.L"].tail = amwi * breast_joint_L_tail

ebones["breast_scale_joint.L"].head = amwi * breast_scale_joint_L_head #actual breast_joint_L_tail
ebones["breast_scale_joint.L"].tail = amwi * breast_scale_joint_L_tail #actual nipple_joint01_L_head


ebones["nipple_joint01.L"].head = amwi * nipple_joint01_L_head
ebones["nipple_joint01.L"].tail = amwi * nipple_joint01_L_tail

#lets make the nipple twice distance to get the jointEnd tail then correct it back
ebones["nipple_joint01.L"].length *= 2
nipple_joint01_L_tail_doubled = ebones["nipple_joint01.L"].tail.copy()
ebones["nipple_joint01.L"].length /= 2

ebones["nipple_jointEnd.L"].head = amwi * nipple_joint01_L_tail
ebones["nipple_jointEnd.L"].tail = nipple_joint01_L_tail_doubled

#deform01
ebones["breast_deform01_joint01.L"].head = amwi * breast_joint_L_tail
ebones["breast_deform01_joint01.L"].tail = amwi * breast_deform01_joint01_L_tail
deform01_length = ebones["breast_deform01_joint01.L"].length
ebones["breast_deform01_joint01.L"].length += 	deform01_length*0.1							#make the tail a bit longer
breast_deform01_joint01_L_tail_longer = ebones["breast_deform01_joint01.L"].tail.copy()
ebones["breast_deform01_joint01.L"].length -= 	deform01_length*0.1							#fix the tail
#ebones["breast_deform01_joint01.L"].tail = amwi * breast_deform01_joint01_L_tail 	

ebones["breast_deform01_jointEnd.L"].head = amwi * breast_deform01_joint01_L_tail
ebones["breast_deform01_jointEnd.L"].tail = breast_deform01_joint01_L_tail_longer

#deform02
ebones["breast_deform02_joint01.L"].head = amwi * breast_joint_L_tail
ebones["breast_deform02_joint01.L"].tail = amwi * breast_deform02_joint01_L_tail
deform02_length = ebones["breast_deform02_joint01.L"].length
ebones["breast_deform02_joint01.L"].length += 	deform02_length*0.1							#make the tail a bit longer
breast_deform02_joint01_L_tail_longer = ebones["breast_deform02_joint01.L"].tail.copy()
ebones["breast_deform02_joint01.L"].length -= 	deform02_length*0.1							#fix the tail
#ebones["breast_deform02_joint01.L"].tail = amwi * breast_deform02_joint01_L_tail 	

ebones["breast_deform02_jointEnd.L"].head = amwi * breast_deform02_joint01_L_tail
ebones["breast_deform02_jointEnd.L"].tail = breast_deform02_joint01_L_tail_longer

#deform03
ebones["breast_deform03_joint01.L"].head = amwi * breast_joint_L_tail
ebones["breast_deform03_joint01.L"].tail = amwi * breast_deform03_joint01_L_tail
deform03_length = ebones["breast_deform03_joint01.L"].length
ebones["breast_deform03_joint01.L"].length += 	deform03_length*0.1							#make the tail a bit longer
breast_deform03_joint01_L_tail_longer = ebones["breast_deform03_joint01.L"].tail.copy()
ebones["breast_deform03_joint01.L"].length -= 	deform03_length*0.1							#fix the tail
#ebones["breast_deform03_joint01.L"].tail = amwi * breast_deform03_joint01_L_tail 	

ebones["breast_deform03_jointEnd.L"].head = amwi * breast_deform03_joint01_L_tail
ebones["breast_deform03_jointEnd.L"].tail = breast_deform03_joint01_L_tail_longer



ebones["stomach_joint01"].head = amwi * stomach_joint01_head
ebones["stomach_joint01"].tail = amwi * stomach_joint01_tail
ebones["stomach_jointEnd"].head = amwi * stomach_jointEnd_head
ebones["stomach_jointEnd"].tail = amwi * stomach_jointEnd_tail

ebones["rib_joint01.R"].head = amwi * rib_joint01_R_head
ebones["rib_joint01.R"].tail = amwi * rib_joint01_R_tail
ebones["rib_jointEnd.R"].head = amwi * rib_jointEnd_R_head
ebones["rib_jointEnd.R"].tail = amwi * rib_jointEnd_R_tail

ebones["butt_joint01.R"].head = amwi * butt_joint01_R_head
ebones["butt_joint01.R"].tail = amwi * butt_joint01_R_tail
ebones["butt_jointEnd.R"].head = amwi * butt_jointEnd_R_head
ebones["butt_jointEnd.R"].tail = amwi * butt_jointEnd_R_tail

ebones["rib_joint01.L"].head = amwi * rib_joint01_L_head
ebones["rib_joint01.L"].tail = amwi * rib_joint01_L_tail
ebones["rib_jointEnd.L"].head = amwi * rib_jointEnd_L_head
ebones["rib_jointEnd.L"].tail = amwi * rib_jointEnd_L_tail

ebones["butt_joint01.L"].head = amwi * butt_joint01_L_head
ebones["butt_joint01.L"].tail = amwi * butt_joint01_L_tail
ebones["butt_jointEnd.L"].head = amwi * butt_jointEnd_L_head
ebones["butt_jointEnd.L"].tail = amwi * butt_jointEnd_L_tail

