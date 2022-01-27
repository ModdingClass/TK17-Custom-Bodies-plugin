leg_bones_matching = [
# source bone used for head, source bone used for tail, target bone
["lThighBend", "lThighTwist", "hip_joint.L"], ###"lThighBend + lThighTwist"
["rThighBend", "rThighTwist", "hip_joint.R"], ###"rThighBend + rThighTwist" 

["lShin", "lShin", "knee_joint.L"],
["rShin", "rShin", "knee_joint.R"],

["lFoot", "lFoot", "ankle_joint.L"],
["rFoot", "rFoot", "ankle_joint.R"],

["lToe", "lToe", "ball_joint.L"],
["rToe", "rToe", "ball_joint.R"]
]

spine_bones_matching = [
# source bone used for head, source bone used for tail, target bone
["pelvis", "pelvis", "root"],
["abdomenLower", "abdomenLower", "spine_joint02"],

["abdomenUpper", "abdomenUpper", "spine_joint03"],
["chestLower", "chestLower", "spine_joint04"], ####so and so , maybe I need a mix with joint_03
["chestUpper", "chestUpper", "spine_jointEnd"],

["neckLower", "neckLower", "neck_joint01"],
["neckUpper", "neckUpper", "neck_jointEnd"],
["head", "head", "head_joint02"]
]


hand_bones_matching = [
["lCollar", "lCollar", "clavicle_joint.L"],
["rCollar", "rCollar", "clavicle_joint.R"],
["lShldrBend", "lShldrTwist", "shoulder_joint.L"],  ### ????", "lShldrBend + lShldrTwist"
["rShldrBend", "rShldrTwist", "shoulder_joint.R"],  ### ????", "rShldrBend + rShldrTwist"

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

bones_matching = [


# source bone used for head, source bone used for tail, target bone

["lThighBend", "lThighTwist", "hip_joint.L"], ###"lThighBend + lThighTwist"
["rThighBend", "rThighTwist", "hip_joint.R"], ###"rThighBend + rThighTwist" 

["lShin", "lShin", "knee_joint.L"],
["rShin", "rShin", "knee_joint.R"],

["lFoot", "lFoot", "ankle_joint.L"],
["rFoot", "rFoot", "ankle_joint.R"],

["lToe", "lToe", "ball_joint.L"],
["rToe", "rToe", "ball_joint.R"],

["pelvis", "pelvis", "root"],
["abdomenLower", "abdomenLower", "spine_joint02"],

["abdomenUpper", "abdomenUpper", "spine_joint03"],
["chestLower", "chestLower", "spine_joint04"], ####so and so , maybe I need a mix with joint_03
["chestUpper", "chestUpper", "spine_jointEnd"],

["neckLower", "neckLower", "neck_joint01"],
["neckUpper", "neckUpper", "neck_jointEnd"],
["head", "head", "head_joint02"],

["lCollar", "lCollar", "clavicle_joint.L"],
["rCollar", "rCollar", "clavicle_joint.R"],
["lShldrBend", "lShldrTwist", "shoulder_joint.L"],  ### ????", "lShldrBend + lShldrTwist"
["rShldrBend", "rShldrTwist", "shoulder_joint.R"],  ### ????", "rShldrBend + rShldrTwist"

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

