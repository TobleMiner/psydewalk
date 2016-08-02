from psydewalk import Simulation
from psydewalk.geo import Coordinate
from psydewalk.pedestrian import Pedestrian
from psydewalk.behavior import BehaviorManager

import logging

class Human():
	"""A human"""
	def __init__(self, sim, loc=Coordinate(), logger='human'):
		self.logger = logging.getLogger(logger)
		self.sim = sim
		self.loc = loc
		self.setMode(Pedestrian, loc)
		self.controller = BehaviorManager(self)
		#TODO?LOW Temporary hard-coded values. Replace by proper mechanism soon
		self.attributes = {'work': {'loc': Coordinate(54.336875, 10.123047)}, 'home': {'loc': Coordinate(54.355541, 10.131542)}}

	def getSimulation(self):
		return self.sim

	def getLocation(self):
		if self.mode:
			return self.mode.getLocation()
		return self.loc

	def getSpeed(self):
		if self.mode:
			return self.mode.getSpeed()
		return -1

	def navigateTo(self, coord):
		self.mode.navigateTo(coord)
		self.mode.run()

	def setMode(self, mode, loc):
		self.logger.info('Setting mode: ' + mode.__name__)
		self.mode = mode(loc)

	def changeMode(self, mode):
		loc = self.mode.getLocation()
		self.setMode(mode, loc)

	def start(self):
		self.controller.start()
