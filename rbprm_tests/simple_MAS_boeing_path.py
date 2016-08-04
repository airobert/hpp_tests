from hpp.corbaserver.rbprm.rbprmbuilder import Builder
from hpp.corbaserver import Client
from hpp.gepetto import Viewer

cl = Client()
cl.problem.selectProblem("rbprm")

# gepetto-viewer-server 
# not hppcorbaserver 
# but hpp-rbprm-server

rootJointType = 'freeflyer'
packageName = 'hpp-rbprm-corba'
meshPackageName = 'hpp-rbprm-corba'
urdfName = 'hyq_trunk'
urdfNameRom = ['hyq_lhleg_rom','hyq_lfleg_rom','hyq_rfleg_rom','hyq_rhleg_rom']
urdfSuffix = ""
srdfSuffix = ""
# name_of_scene = "groundcrouch"
name_of_scene = "simple_boeing"

rbprmBuilder = Builder ()

rbprmBuilder.loadModel(urdfName, urdfNameRom, rootJointType, meshPackageName, packageName, urdfSuffix, srdfSuffix)
# rbprmBuilder.setJointBounds ("base_joint_xyz", [-6,5, -4, 4, 0.6, 2])
rbprmBuilder.setFilter(['hyq_rhleg_rom', 'hyq_lfleg_rom', 'hyq_rfleg_rom','hyq_lhleg_rom'])
rbprmBuilder.setNormalFilter('hyq_lhleg_rom', [0,0,1], 0.9)
rbprmBuilder.setNormalFilter('hyq_rfleg_rom', [0,0,1], 0.9)
rbprmBuilder.setNormalFilter('hyq_lfleg_rom', [0,0,1], 0.9)
rbprmBuilder.setNormalFilter('hyq_rhleg_rom', [0,0,1], 0.9)
rbprmBuilder.boundSO3([-0.1,0.1,-1,1,-1,1])
rbprmBuilder.setJointBounds ("base_joint_xyz", [-35,10, -4, 4, -1, 1])

#~ from hpp.corbaserver.rbprm. import ProblemSolver
from hpp.corbaserver.rbprm.problem_solver import ProblemSolver

ps = ProblemSolver( rbprmBuilder )

r = Viewer (ps)

q_init = [4, 0, 0.65, 1,0,0,0];
q_goal = [-27, 0, 0.65, 1,0,0,0];

ps.addPathOptimizer("RandomShortcut")
ps.setInitialConfig (q_init)
ps.addGoalConfig (q_goal)


r.loadObstacleModel (packageName, name_of_scene, "planning")
r.client.gui.setColor('planning', [1,1,1,0.3])
ps.client.problem.selectConFigurationShooter("RbprmShooter")
ps.client.problem.selectPathValidation("RbprmPathValidation",0.05)
# r(q_init)


r.addLandmark(r.sceneName,1)
#~ ps.solve ()
t = ps.solve ()
if isinstance(t, list):
	t = t[0]* 3600000 + t[1] * 60000 + t[2] * 1000 + t[3]
# f = open('log.txt', 'a')
# f.write("path computation " + str(t) + "\n")
# f.close()
#~ rbprmBuilder.exportPath (r, ps.client.problem, 1, 0.1, "obstacle_hyq_robust_10_path.txt")


from hpp.gepetto import PathPlayer
pp = PathPlayer (rbprmBuilder.client.basic, r)

from hpp.corbaserver.manipulation import Client as ManipClient
from hpp.corbaserver.manipulation import Robot as ManipRobot

mcl = ManipClient()
mcl.problem.selectProblem("manip")

ManipRobot.packageName = "hpp_tutorial"
ManipRobot.meshPackageName = "pr2_description"
ManipRobot.rootJointType = "planar"
ManipRobot.urdfName = "pr2"
ManipRobot.urdfSuffix = ""
ManipRobot.srdfSuffix = ""

manipRobot = ManipRobot ("robot-name", "agent1")
manipRobot.(insert|load)RobotModel("agent2", ManipRobot.rootJointType, ManipRobot.packageName, ManipRobot.urdfName, ManipRobot.urdfSuffix, ManipRobot.srdfSuffix)
manipRobot.(insert|load)RobotModel("agent3", ManipRobot.rootJointType, ManipRobot.packageName, ManipRobot.urdfName, ManipRobot.urdfSuffix, ManipRobot.srdfSuffix)
"agent3/base_joint_xyz"

# manipRobot.isConfigValid([list of configuration in a list]) # configuration as a list and put them together to check
# r(q_goal)
#pp (0)
#pp (1)
# pp (0)
# r (q_goal)