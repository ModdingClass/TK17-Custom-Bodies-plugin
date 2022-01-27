vertexGroupsForRemoval = ['lIndex3', 'lMid3', 'lRing3', 'lPinky3', 'rIndex3', 'rMid3', 'rRing3', 'rPinky3', 'lThumb3', 'lIndex2', 'lMid2', 'lRing2', 'lPinky2', 'rThumb3', 'rIndex2', 'rMid2', 'rRing2', 'rPinky2', 'tongue04', 'lThumb2', 'lIndex1', 'lMid1', 'lRing1', 'lPinky1', 'rThumb2', 'rIndex1', 'rMid1', 'rRing1', 'rPinky1', 'tongue03', 'lThumb1', 'lCarpal1', 'lCarpal2', 'lCarpal3', 'lCarpal4', 'rThumb1', 'rCarpal1', 'rCarpal2', 'rCarpal3', 'rCarpal4', 'tongue02', 'lHand', 'rHand', 'tongue01', 'lNasolabialLower', 'rNasolabialLower', 'lNasolabialMouthCorner', 'rNasolabialMouthCorner', 'lLipCorner', 'lLipLowerOuter', 'lLipLowerInner', 'LipLowerMiddle', 'rLipLowerInner', 'rLipLowerOuter', 'rLipCorner', 'LipBelow', 'Chin', 'lCheekLower', 'rCheekLower', 'BelowJaw', 'lJawClench', 'rJawClench', 'lForearmTwist', 'rForearmTwist', 'lowerTeeth', 'rBrowInner', 'rBrowMid', 'rBrowOuter', 'lBrowInner', 'lBrowMid', 'lBrowOuter', 'CenterBrow', 'MidNoseBridge', 'lEyelidInner', 'lEyelidUpperInner', 'lEyelidUpper', 'lEyelidUpperOuter', 'lEyelidOuter', 'lEyelidLowerOuter', 'lEyelidLower', 'lEyelidLowerInner', 'rEyelidInner', 'rEyelidUpperInner', 'rEyelidUpper', 'rEyelidUpperOuter', 'rEyelidOuter', 'rEyelidLowerOuter', 'rEyelidLower', 'rEyelidLowerInner', 'lSquintInner', 'lSquintOuter', 'rSquintInner', 'rSquintOuter', 'lCheekUpper', 'rCheekUpper', 'Nose', 'lNostril', 'rNostril', 'lLipBelowNose', 'rLipBelowNose', 'lLipUpperOuter', 'lLipUpperInner', 'LipUpperMiddle', 'rLipUpperInner', 'rLipUpperOuter', 'lLipNasolabialCrease', 'rLipNasolabialCrease', 'lNasolabialUpper', 'rNasolabialUpper', 'lNasolabialMiddle', 'rNasolabialMiddle', 'lSmallToe4_2', 'lSmallToe3_2', 'lSmallToe2_2', 'lSmallToe1_2', 'lBigToe_2', 'rSmallToe4_2', 'rSmallToe3_2', 'rSmallToe2_2', 'rSmallToe1_2', 'rBigToe_2', 'lForearmBend', 'rForearmBend', 'upperTeeth', 'lowerJaw', 'lEye', 'rEye', 'lEar', 'rEar', 'lSmallToe4', 'lSmallToe3', 'lSmallToe2', 'lSmallToe1', 'lBigToe', 'rSmallToe4', 'rSmallToe3', 'rSmallToe2', 'rSmallToe1', 'rBigToe', 'lShldrTwist', 'rShldrTwist', 'head', 'lMetatarsals', 'lHeel', 'rMetatarsals', 'rHeel', 'lShldrBend', 'rShldrBend', 'neckUpper', 'lFoot', 'rFoot', 'lCollar', 'rCollar', 'neckLower', 'lShin', 'rShin', 'chestUpper', 'lPectoral', 'rPectoral', 'lThighTwist', 'rThighTwist', 'chestLower', 'lThighBend', 'rThighBend', 'abdomenUpper', 'pelvis', 'abdomenLower']
jaw = ["lowerTeeth"]
head_weights = ['head', 'upperTeeth', 'lowerJaw', 'lEye', 'rEye', 'lEar', 'rEar','rBrowInner', 'rBrowMid', 'rBrowOuter', 'lBrowInner', 'lBrowMid', 'lBrowOuter', 'CenterBrow', 'MidNoseBridge', 'lEyelidInner', 'lEyelidUpperInner', 'lEyelidUpper', 'lEyelidUpperOuter', 'lEyelidOuter', 'lEyelidLowerOuter', 'lEyelidLower', 'lEyelidLowerInner', 'rEyelidInner', 'rEyelidUpperInner', 'rEyelidUpper', 'rEyelidUpperOuter', 'rEyelidOuter', 'rEyelidLowerOuter', 'rEyelidLower', 'rEyelidLowerInner', 'lSquintInner', 'lSquintOuter', 'rSquintInner', 'rSquintOuter', 'lCheekUpper', 'rCheekUpper', 'Nose', 'lNostril', 'rNostril', 'lLipBelowNose', 'rLipBelowNose', 'lLipUpperOuter', 'lLipUpperInner', 'LipUpperMiddle', 'rLipUpperInner', 'rLipUpperOuter', 'lLipNasolabialCrease', 'rLipNasolabialCrease', 'lNasolabialUpper', 'rNasolabialUpper', 'lNasolabialMiddle', 'rNasolabialMiddle', 'tongue01', 'lNasolabialLower', 'rNasolabialLower', 'lNasolabialMouthCorner', 'rNasolabialMouthCorner', 'lLipCorner', 'lLipLowerOuter', 'lLipLowerInner', 'LipLowerMiddle', 'rLipLowerInner', 'rLipLowerOuter', 'rLipCorner', 'LipBelow', 'Chin', 'lCheekLower', 'rCheekLower', 'BelowJaw', 'lJawClench', 'rJawClench']
leg_weights_matching = [
# source bone used for head, source bone used for tail, target bone
#["lThighBend", "lThighTwist", "hip_joint.L"], ###"lThighBend + lThighTwist"
#["rThighBend", "rThighTwist", "hip_joint.R"], ###"rThighBend + rThighTwist" 

["lShin", "lShin", "knee_joint.L"],
["rShin", "rShin", "knee_joint.R"],

#["lFoot", "lFoot", "ankle_joint.L"],
#["rFoot", "rFoot", "ankle_joint.R"],

["lToe", "lToe", "ball_joint.L"],
["rToe", "rToe", "ball_joint.R"],

#["lBigToe_2","lBigToe_2","toe_deform01_joint01.L"],
#["rBigToe_2","rBigToe_2","toe_deform01_joint01.R"],

#["lSmallToe2_2","lSmallToe2_2","toe_deform02_joint01.L"],
#["rSmallToe2_2","rSmallToe2_2","toe_deform02_joint01.R"]

]

# source bone used for head, source bone used for tail, target bone
spine_weights_matching = [
["pelvis", "pelvis", "root"],         #!!!!!!!!!!!!!!!! not going to set the root yet, as it could be hardcoded in many other places
["abdomenLower", "abdomenLower", "spine_joint02"],

["abdomenUpper", "abdomenUpper", "spine_joint03"],
["chestLower", "chestLower", "spine_joint04"], ####so and so , maybe I need a mix with joint_03
["chestUpper", "chestUpper", "spine_jointEnd"],

["neckLower", "neckLower", "neck_joint01"],
["neckUpper", "neckUpper", "neck_jointEnd"],
#["head", "head", "head_joint02"]
]


hand_weights_matching = [
["lCollar", "lCollar", "clavicle_joint.L"],
["rCollar", "rCollar", "clavicle_joint.R"],
#["lShldrBend", "lShldrTwist", "shoulder_joint.L"],  ### ????", "lShldrBend + lShldrTwist"
#["rShldrBend", "rShldrTwist", "shoulder_joint.R"],  ### ????", "rShldrBend + rShldrTwist"

["lForearmBend", "lForearmBend", "elbow_joint.L"],
["rForearmBend", "rForearmBend", "elbow_joint.R"],
["lForearmTwist", "lForearmTwist", "forearm_joint.L"],
["rForearmTwist", "rForearmTwist", "forearm_joint.R"],

["lHand", "lHand", "wrist_joint.L"],
["rHand", "rHand", "wrist_joint.R"],

["lThumb1", "lThumb1", "finger01_joint01.L"],
["lCarpal1", "lCarpal1", "finger02_joint01.L"],
["lCarpal2", "lCarpal2", "finger03_joint01.L"],
["lCarpal3", "lCarpal3", "finger04_joint01.L"],
["lCarpal4", "lCarpal4", "finger05_joint01.L"],

["lThumb2", "lThumb2", "finger01_joint02.L"],
["lThumb3", "lThumb3", "finger01_joint03.L"],

["lIndex1", "lIndex1", "finger02_joint02.L"],
["lIndex2", "lIndex2", "finger02_joint03.L"],
["lIndex3", "lIndex3", "finger02_joint04.L"],

["lMid1", "lMid1", "finger03_joint02.L"],
["lMid2", "lMid2", "finger03_joint03.L"],
["lMid3", "lMid3", "finger03_joint04.L"],

["lRing1", "lRing1", "finger04_joint02.L"],
["lRing2", "lRing2", "finger04_joint03.L"],
["lRing3", "lRing3", "finger04_joint04.L"],

["lPinky1", "lPinky1", "finger05_joint02.L"],
["lPinky2", "lPinky2", "finger05_joint03.L"],
["lPinky3", "lPinky3", "finger05_joint04.L"],

["rThumb1", "rThumb1", "finger01_joint01.R"],
["rCarpal1", "rCarpal1", "finger02_joint01.R"],
["rCarpal2", "rCarpal2", "finger03_joint01.R"],
["rCarpal3", "rCarpal3", "finger04_joint01.R"],
["rCarpal4", "rCarpal4", "finger05_joint01.R"],

["rThumb2", "rThumb2", "finger01_joint02.R"],
["rThumb3", "rThumb3", "finger01_joint03.R"],
           
["rIndex1", "rIndex1", "finger02_joint02.R"],
["rIndex2", "rIndex2", "finger02_joint03.R"],
["rIndex3", "rIndex3", "finger02_joint04.R"],

["rMid1", "rMid1", "finger03_joint02.R"],
["rMid2", "rMid2", "finger03_joint03.R"],
["rMid3", "rMid3", "finger03_joint04.R"],

["rRing1", "rRing1", "finger04_joint02.R"],
["rRing2", "rRing2", "finger04_joint03.R"],
["rRing3", "rRing3", "finger04_joint04.R"],

["rPinky1", "rPinky1", "finger05_joint02.R"],
["rPinky2", "rPinky2", "finger05_joint03.R"],
["rPinky3", "rPinky3", "finger05_joint04.R"]
]
