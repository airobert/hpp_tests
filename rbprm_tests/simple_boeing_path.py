from hpp.corbaserver.rbprm.rbprmbuilder import Builder
from hpp.gepetto import Viewer

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
rbprmBuilder.setJointBounds ("base_joint_xyz", [-6,5, -4, 4, 0.6, 2])
rbprmBuilder.setFilter(['hyq_rhleg_rom', 'hyq_lfleg_rom', 'hyq_rfleg_rom','hyq_lhleg_rom'])
rbprmBuilder.setNormalFilter('hyq_lhleg_rom', [0,0,1], 0.9)
rbprmBuilder.setNormalFilter('hyq_rfleg_rom', [0,0,1], 0.9)
rbprmBuilder.setNormalFilter('hyq_lfleg_rom', [0,0,1], 0.9)
rbprmBuilder.setNormalFilter('hyq_rhleg_rom', [0,0,1], 0.9)
rbprmBuilder.boundSO3([-0.1,0.1,-1,1,-1,1])

#~ from hpp.corbaserver.rbprm. import ProblemSolver
from hpp.corbaserver.rbprm.problem_solver import ProblemSolver

ps = ProblemSolver( rbprmBuilder )

r = Viewer (ps)



rbprmBuilder.setJointBounds ("base_joint_xyz", [-4,4, -35, 22, -1, 1])
q_init = [0, 4, 0,1,0,0,0];
q_goal = [0, -33, 0, 1, 0, 0, 0];
# rbprmBuilder.setCurrentConfig (q_init); r (q_init)

# q_init = rbprmBuilder.getCurrentConfig ();
# q_init = [-6,-3,0.8,1,0,0,0]; 

# q_goal = [4, 4, 0.8, 1, 0, 0, 0]; r (q_goal)

ps.addPathOptimizer("RandomShortcut")
ps.setInitialConfig (q_init)
ps.addGoalConfig (q_goal)

ps.client.problem.selectConFigurationShooter("RbprmShooter")
ps.client.problem.selectPathValidation("RbprmPathValidation",0.01)
r.loadObstacleModel (packageName, name_of_scene, "planning")
r.client.gui.setColor('planning', [1,1,1,0.3])

r(q_init)


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

#~ pp (0)
#~ pp (1)
pp (0)
# r (q_goal)