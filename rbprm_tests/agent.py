# Robert White @ ILLC & LAAS
import sys
# import socket
# import threading 

class Agent ():

	name = 0
	# client = socket.socket()
	host = ''
	port = 0
	start = (0,0)
	current = (0,0)
	end = (0,0)

	def __init__(self, name):
		# threading.Thread.__init__(self) 
		self.name = name

	def print_name:
		print self.name