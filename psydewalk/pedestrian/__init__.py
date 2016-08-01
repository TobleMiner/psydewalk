from ..entity import SmoothMovingEntity
from ..jitter import Jitter
from ..data import DataProvider
from ..geo import Coordinate

from pyroutelib2.route import Router
from pyroutelib2.loadOsm import LoadOsm

import asyncio
from asyncio import Queue
from threading import Thread


class Pedestrian(SmoothMovingEntity, DataProvider, Jitter):
	def __init__(self, loc=Coordinate(), speed=0, logger='pedestrian'):
		DataProvider.__init__(self)
		Jitter.__init__(self)
		SmoothMovingEntity.__init__(self, loc, speed, logger)
		self.loop = asyncio.get_event_loop()
		self.waypoints = Queue()
		self.osm = LoadOsm("foot")

	def navigateTo(self, coord):
		start = self.osm.findNode(self.loc)
		end = self.osm.findNode(coord)
		router = Router(self.osm)
		result, route = router.doRoute(start, end)
		if result == 'success':
			for i in route:
				node = self.osm.rnodes[i]
				self.addWaypoint(Coordinate(node[0], node[1]))
		else:
			self.logger.warning('Failed to get route: {0} Using cross-country path'.format(result))
			self.addWaypoint(coord)

	def addWaypoint(self, coord):
		self.loop.run_until_complete(self.waypoints.put(coord))

	def run(self, interval=50):
		self.logger.info('Starting @{0}'.format(self.loc))
		while True:
			if self.waypoints.empty():
				self.setSpeed(0, True)
			waypoint = self.loop.run_until_complete(self.waypoints.get())
			self.logger.info('Moving to {0}'.format(waypoint))
			self.moveTo(waypoint, interval)
			self.logger.info('Reached {0}'.format(waypoint))
