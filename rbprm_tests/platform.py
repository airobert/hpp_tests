from hpp.corbaserver.rbprm.rbprmbuilder import Builder
from hpp.gepetto import Viewer
from hpp.corbaserver.rbprm.problem_solver import ProblemSolver
import sys

from hpp.corbaserver.manipulation import Client as ManipClient
from hpp.corbaserver.manipulation import Robot as ManipRobot
from hpp.gepetto import PathPlayer


# from hpp.corbaserver.manipulation import ManipClient
# from hpp.corbaserver import BasicClient



# mcl = ManipClient()

# cl.robot.create ("name")

# cl.robot.insertRobotModel (....)

# cl.robot.insertRobotModel (....)

# cl.robot.insertRobotModel (....)


# bcl = BasicClient()

# cl.robot.isConfigValid (....)

class MetaAgent ():
	
	agents = []
	# the robot
	manipRobot = None
	# the client
	mcl = ManipClient()
	# the path player
	

	def __init__(self, agents):
		self.agents = agents
		self.mcl.problem.selectProblem("manip")

		ManipRobot.packageName = "hpp_tutorial"
		ManipRobot.meshPackageName = "pr2_description"
		ManipRobot.rootJointType = "planar"
		ManipRobot.urdfName = "pr2"
		ManipRobot.urdfSuffix = ""
		ManipRobot.srdfSuffix = ""
		# cl.robot.insertRobotModel ()
		manipRobot = ManipRobot ("robot-name", "agent1") # TODO
		for a in self.agents:
			agent_name = 'agent' + str(a.name)
			manipRobot.loadModel(agent_name, ManipRobot.rootJointType) # I am not sure about this line

			# , ManipRobot.packageName, ManipRobot.urdfName, ManipRobot.urdfSuffix, ManipRobot.srdfSuffix)
		# "agent3/base_joint_xyz"

	def check_validity ():
		return False



class Platform ():
	viewer = None
	meta_agent = None
	tree = None
	# path player
	pp = None
	# pp = PathPlayer (rbprmBuilder.client.basic,ls r)
	def __init__(self, agents):
		self.meta_agent = MetaAgent(agents)
		# initialise a tree to get prepared to expand the tree

	def plan ():
		# if there is plan, then return true, otherwise, return false.
		return (False, [])


def main(spc_file):
	print 'start the platform'
	# parse how many agent I need
	f = open (spc_file, 'r')
	lines = f.read()
	lines = lines.split('\n')
	
	# first of all see how many agents are there
	amount =  int(lines[0].split(' ')[-1])
	print 'the platform got ', amount, ' agents in this planning task'

	agents = []
	# initialise an empty list of agent types. 
	agent_types = [''] * amount
	agent_start_config = [[]] * amount
	agent_end_config = [[]] * amount
	
	for a in range(amount):
		name = int(lines[a*4 + 1].split(' ')[-1])
		if (name == a):
			print 'name: ', name
			agent_types[a] = lines[a*4 + 2].split(' ')[-1] 
			print 'type: ', agent_types[a]
			agent_start_config = map (int, lines[a*4 + 3].split(' ')[2,:])
			print 'initial config: ', agent_start_config
			agent_end_config = map (int, lines[a*4 + 4].split(' ')[2,:])
			print 'end config: ', agent_end_config




	# start_end = [[[0,0],[0,0]]] * 11 # up to ten agents in the environment in this demo
	# scene = []
	# amount = 0
	# for r in range (len(lines)):
	# 	line = lines[r]
	# 	line = line.split(' ')
	# 	row = []
	# 	for l in range (len(line)):
	# 		c = line[l]
	# 		if (c == 'X'):
	# 			row.append(1)
	# 		else:
	# 			row.append(0)
	# 			if (int(c) > 0): # it is a destination of an agent
	# 				[start, end] = start_end[abs(int(c))]
	# 				end = [r, l]
	# 				start_end[abs(int(c))] = [start, end]
	# 				if amount < int(c):
	# 					amount = int(c)
	# 			elif (int(int(c) < 0)):
	# 				[start, end] = start_end[abs(int(c))]
	# 				start = [r, l]
	# 				start_end[abs(int(c))] = [start, end]
	# 	print row 
	# 	scene.append(row)
	# # print start_end

	print 'There are ', amount, ' agents living here.'
	print 'create the platform'
	# start_end = start_end[1:amount+1]
	# print start_end
	# p = Platform(scene, 'localhost', 2024, amount, start_end)

	# p.begin()
	# p.plan()

if __name__ == "__main__":
	main(sys.argv[1]) # pass the filename here