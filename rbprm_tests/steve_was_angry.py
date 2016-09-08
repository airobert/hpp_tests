
#gepetto-viewer-server
#hppcorbaserver

from hpp.corbaserver.robot import Robot as Parent

##
#  Control of robot PR2 in hpp
#
#  This class implements a client to the corba server implemented in
#  hpp-corbaserver. It derive from class hpp.corbaserver.robot.Robot.
#
#  This class is also used to initialize a client to rviz in order to
#  display configurations of the PR2 robot.
#
#  At creation of an instance, the urdf and srdf files are loaded using
#  idl interface hpp::corbaserver::Robot::loadRobotModel.
class Robot (Parent):
    ##
    #  Information to retrieve urdf and srdf files.
    packageName = "tp-rrt"
    meshPackageName = "tp-rrt"
    rootJointType = "planar"
    ##
    #  Information to retrieve urdf and srdf files.
    urdfName = "buggy"
    urdfSuffix = ""
    srdfSuffix = ""
    def __init__ (self, robotName, load = True):
        Parent.__init__ (self, robotName, self.rootJointType, load)
        self.tf_root = "base_footprint"

packageName = "tp-rrt"
#~ urdfName = "buggy"	
urdfSuffix = ""
srdfSuffix = ""
rootJointType = "planar"

pr2 = Robot("pr2")


#~ def loadRobot(urdfName): 
    #~ client= BasicClient()
    #~ return client.robot.loadRobotModel(urdfName, rootJointType, packageName, urdfName, urdfSuffix, srdfSuffix)
# ------------------------------

# the above was not working but the following works if you have the hyq installed
from hpp.corbaserver.robot import Robot as Parent

##
#  Control of robot PR2 in hpp
#
#  This class implements a client to the corba server implemented in
#  hpp-corbaserver. It derive from class hpp.corbaserver.robot.Robot.
#
#  This class is also used to initialize a client to rviz in order to
#  display configurations of the PR2 robot.
#
#  At creation of an instance, the urdf and srdf files are loaded using
#  idl interface hpp::corbaserver::Robot::loadRobotModel.
class HYQ (Parent):
    ##
    #  Information to retrieve urdf and srdf files.
    packageName = "hyq_description"
    meshPackageName = "hyq_description"
    rootJointType = "planar"
    ##
    #  Information to retrieve urdf and srdf files.
    urdfName = "hyq"
    urdfSuffix = ""
    srdfSuffix = ""
    def __init__ (self, robotName, load = True):
        Parent.__init__ (self, robotName, self.rootJointType, load)
        self.tf_root = "base_footprint"

packageName = "hyq_description"
#~ urdfName = "buggy"   
urdfSuffix = ""
srdfSuffix = ""
rootJointType = "planar"

robot = HYQ("h")


from hpp.corbaserver import ProblemSolver
from hpp.gepetto import ViewerFactory
from hpp.gepetto import PathPlayer

robot.rankInConfiguration('lf_kfe_joint')
q_goal [rank] = -0.5

ps = ProblemSolver (robot)
vf = ViewerFactory (ps)

ps.selectPathPlanner ("VisibilityPrmPlanner")
ps.addPathOptimizer ("RandomShortcut")

r = vf.createViewer()
q_init = robot.getCurrentConfig ()
q_init[6] = -0.5 
q_init[9] = 0.5
q_init[12] = -0.5
q_init[15] = 0.5
q_goal = q_init [::]
q_goal[0] = 1
q_goal[1] = 1
q_goal[2] = 1


ps.setInitialConfig(q_init)
ps.addGoalConfig (q_goal)

print ps.solve ()

pp = PathPlayer (robot.client, r)
pp (0)