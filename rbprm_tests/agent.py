# Robert White @ ILLC & LAAS
import sys
# import socket
# import threading 
from hpp.corbaserver import Client
from hpp.corbaserver.rbprm.problem_solver import ProblemSolver
from hpp.corbaserver.rbprm.rbprmbuilder import Builder


class Agent ():

	name = 0
	type = ''
	# client = socket.socket()
	# host = ''
	# port = 0
	cl = Client()

	# rbprmBuilder 
	robot = None
	# problem solver
	ps = None
	
	# initial configuration and goal configuration 
	start = (0,0)
	current = (0,0)
	end = (0,0)

	rootJointType = 'freeflyer'
	packageName = 'hpp-rbprm-corba'
	meshPackageName = 'hpp-rbprm-corba'
	urdfName = 'hyq_trunk'
	urdfNameRom = ['hyq_lhleg_rom','hyq_lfleg_rom','hyq_rfleg_rom','hyq_rhleg_rom']
	urdfSuffix = ""
	srdfSuffix = ""

	def __init__(self, type, name, start, end, mode):
		# threading.Thread.__init__(self) 
		self.name = name
		if type == 'hyq':
			self.type = 'hyq'
			# the agent was set to its initial configuration at the beginning of the game 
			self.start = start
			self.end = end
			self.current = start
			if mode == 'rbprm':
				self.cl.problem.selectProblem("rbprm")
				# build the robot
				self.robot = Builder ()
				self.robot.loadModel(urdfName, urdfNameRom, rootJointType, meshPackageName, packageName, urdfSuffix, srdfSuffix)
				self.robot.setFilter(['hyq_rhleg_rom', 'hyq_lfleg_rom', 'hyq_rfleg_rom','hyq_lhleg_rom'])
				self.robot.setNormalFilter('hyq_lhleg_rom', [0,0,1], 0.9)
				self.robot.setNormalFilter('hyq_rfleg_rom', [0,0,1], 0.9)
				self.robot.setNormalFilter('hyq_lfleg_rom', [0,0,1], 0.9)
				self.robot.setNormalFilter('hyq_rhleg_rom', [0,0,1], 0.9)
				self.robot.boundSO3([-0.1,0.1,-1,1,-1,1])
				self.robot.setJointBounds ("base_joint_xyz", [-35,10, -4, 4, -1, 1])
				# problem solver:
				self.ps = ProblemSolver( self.robot )
				self.ps.addPathOptimizer("RandomShortcut")
				self.ps.setInitialConfig (self.start)
				self.ps.addGoalConfig (self.end)

		else:
			print 'the agent is not hyq and further specification is required'
			# this project so far deals only with HyQ robots



	def print_name:
		print 'this is agent', str(self.name)