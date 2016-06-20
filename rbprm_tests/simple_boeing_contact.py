from hpp.corbaserver.rbprm.rbprmbuilder import Builder
from hpp.corbaserver.rbprm.rbprmfullbody import FullBody
from hpp.gepetto import Viewer
from time import sleep

import simple_boeing_path as tp


packageName = "hyq_description"
meshPackageName = "hyq_description"
rootJointType = "freeflyer"
name_of_scene = "simple_boeing"


#  Information to retrieve urdf and srdf files.
urdfName = "hyq"
urdfSuffix = ""
srdfSuffix = ""

#  This time we load the full body model of HyQ
fullBody = FullBody () 
fullBody.loadFullBodyModel(urdfName, rootJointType, meshPackageName, packageName, urdfSuffix, srdfSuffix)

#  Setting a number of sample configurations used
nbSamples = 10000

ps = tp.ProblemSolver(fullBody)
r = tp.Viewer (ps)

rootName = 'base_joint_xyz'

#  Creating limbs
# cType is "_3_DOF": positional constraint, but no rotation (contacts are punctual)
cType = "_3_DOF"
# string identifying the limb
rLegId = 'rfleg'
# First joint of the limb, as in urdf file
rLeg = 'rf_haa_joint'
# Last joint of the limb, as in urdf file
rfoot = 'rf_foot_joint'
# Specifying the distance between last joint and contact surface
rLegOffset = [0.,-0.021,0.]
# Specifying the contact surface direction when the limb is in rest pose
rLegNormal = [0,1,0]
# Specifying the rectangular contact surface length
rLegx = 0.02; rLegy = 0.02
# remaining parameters are the chosen heuristic (here, manipulability), and the resolution of the octree (here, 10 cm).
fullBody.addLimb(rLegId,rLeg,rfoot,rLegOffset,rLegNormal, rLegx, rLegy, nbSamples, "manipulability", 0.1, cType)

lLegId = 'lhleg'
lLeg = 'lh_haa_joint'
lfoot = 'lh_foot_joint'
lLegOffset = [0.,-0.021,0.]
lLegNormal = [0,1,0]
lLegx = 0.02; lLegy = 0.02
fullBody.addLimb(lLegId,lLeg,lfoot,lLegOffset,rLegNormal, lLegx, lLegy, nbSamples, "manipulability", 0.05, cType)

rarmId = 'rhleg'
rarm = 'rh_haa_joint'
rHand = 'rh_foot_joint'
rArmOffset = [0.,-0.021,0.]
rArmNormal = [0,1,0]
rArmx = 0.02; rArmy = 0.02
fullBody.addLimb(rarmId,rarm,rHand,rArmOffset,rArmNormal, rArmx, rArmy, nbSamples, "manipulability", 0.05, cType)

larmId = 'lfleg'
larm = 'lf_haa_joint'
lHand = 'lf_foot_joint'
lArmOffset = [0.,-0.021,0.]
lArmNormal = [0,1,0]
lArmx = 0.02; lArmy = 0.02
fullBody.addLimb(larmId,larm,lHand,lArmOffset,lArmNormal, lArmx, lArmy, nbSamples, "forward", 0.05, cType)
# RB: this line is never used?
q_0 = fullBody.getCurrentConfig(); 

fullBody.client.basic.robot.setJointConfig('lf_hfe_joint',[-1.4])
fullBody.client.basic.robot.setJointConfig('lh_hfe_joint',[-1.4])
fullBody.client.basic.robot.setJointConfig('rf_hfe_joint',[-1.4])
fullBody.client.basic.robot.setJointConfig('rh_hfe_joint',[-1.4])

q_init = fullBody.getCurrentConfig(); q_init[0:7] = tp.q_init[0:7]
q_goal = fullBody.getCurrentConfig(); q_goal[0:7] = tp.q_goal[0:7]


# Randomly generating a contact configuration at q_init
fullBody.setCurrentConfig (q_init)
q_init = fullBody.generateContacts(q_init, [0,0,1])

# Randomly generating a contact configuration at q_end
fullBody.setCurrentConfig (q_goal)
q_goal = fullBody.generateContacts(q_goal, [0,-1,0])

# specifying the full body configurations as start and goal state of the problem
fullBody.setStartState(q_init,[])
fullBody.setEndState(q_goal,[rLegId,lLegId,rarmId,larmId])


r(q_init)
# computing the contact sequence
configs = fullBody.interpolate(0.2, 1, 0)
# RB: Is this line redundent?
r.loadObstacleModel ('hpp-rbprm-corba', name_of_scene, "contact")
r.client.gui.setColor('contact', [1,1,1,0.3])

i = 0;
#~ # fullBody.draw(configs[i],r); i=i+1; i-1
#~ 
while (i < len(configs)):
	fullBody.draw(configs[i],r)
	sleep(0.05)
	i = i + 1

print "Animation finished!"
