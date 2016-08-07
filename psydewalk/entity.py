from psydewalk.geo import Coordinate
from psydewalk.data import TrackingProvider

from pyroutelib2.route import Router
from pyroutelib2.loadOsm import LoadOsm

from asyncio import Queue
from threading import Thread, Lock
from time import sleep
import asyncio
import math
import logging

class Entity():
	def __init__(self, loc=Coordinate()):
		self.loc = loc

	def getLocation(self):
		return self.loc

class MovingEntity(Entity):

	DEST_MAX_DIST = 0.23 # Maximum distance to destination for it to be reached

	def __init__(self, loc=Coordinate(), speed=0, logger='MovingEntity'):
		super().__init__(loc)
		self.logger = logging.getLogger(logger)
		self.setSpeed(speed)

	def getSpeed(self):
		return self.speed

	def setSpeed(self, speed):
		self.logger.debug('Setting speed: {0} m/s'.format(speed))
		self.speed = speed

	def moveTo(self, dest, interval=1000):
		while self.loc.dist(dest) > self.DEST_MAX_DIST:
			dist = self.loc.dist(dest)
			delta = dest - self.loc
			vect = delta / dist
			if dist > self.speed * interval / 1000:
				vect = vect * (self.speed * interval / 1000);
			else:
				vect = vect * self.DEST_MAX_DIST
			self.loc = self.loc + vect
			sleep(interval / 1000)

class SmoothMovingEntity(MovingEntity):
	def __init__(self, loc=Coordinate(), speed=0, logger='SmoothMovingEntity'):
		self.speed = 0
		super().__init__(loc, speed, logger)

	def setSpeed(self, speed, temp=False):
		if temp:
			self.speed = speed
		else:
			self.maxspeed = speed
		self.speeddelta = self.maxspeed - self.speed
		self.logger.debug('Setting speed: {0} m/s, delta: {1} m/s ({2})'.format(speed, self.speeddelta, 'temp' if temp else 'perm'))
		self.speedaproxcnt = 0

	def moveTo(self, dest, interval=100):
		while self.loc.dist(dest) > self.DEST_MAX_DIST:
			if(self.speeddelta > 0):
				self.speed += (1 - 1 / abs(self.speeddelta)) ** self.speedaproxcnt
			else:
				self.speed -= (1 - 1 / abs(self.speeddelta)) ** self.speedaproxcnt
			self.speedaproxcnt += 1
			dist = self.loc.dist(dest)
			delta = dest - self.loc
			vect = delta / dist
			if dist > self.speed * interval / 1000:
				vect = vect * (self.speed * interval / 1000);
			else:
				vect = vect * self.DEST_MAX_DIST
			self.loc = self.loc + vect
			sleep(interval / 1000)

class NavigateableTrackableEntity(SmoothMovingEntity, TrackingProvider):
	"""docstring for NavigateableTrackableEntity"""
	def __init__(self, osmmode, loc=Coordinate(), speed=0, logger='navtrackentity'):
		super(NavigateableTrackableEntity, self).__init__(loc, speed, logger)
		try:
			self.loop = asyncio.get_event_loop()
		except RuntimeError:
			self.loop = asyncio.new_event_loop()
			asyncio.set_event_loop(self.loop)
		self.waypoints = Queue()
		self.doTerminate = False
		self.terminated = False
		self.running = False
		self.preRunLock = Lock()
		self.preRunLock.acquire()
		self.runLock = Lock()
		self.stateLock = Lock()
		self.osm = LoadOsm(osmmode)

	def navigateTo(self, coord):
		self.logger.debug('Searching start-/endpoint')
		start = self.osm.findNode(self.loc)
		end = self.osm.findNode(coord)
		if start == end:
			self.logger.debug('Start- and endpoint are the same')
			return
		router = Router(self.osm)
		self.logger.debug('Starting routing to {0}'.format(coord))
		try:
			result, route = router.doRoute(start, end)
		except Exception as err:
			result = str(err)
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
		try:
			self.runLock.acquire()
			self.preRunLock.release()
			self.logger.info('Starting @{0}'.format(self.loc))
			while True:
				self.stateLock.acquire()
				self.running = True
				if self.waypoints.empty():
					self.setSpeed(0, True)
					break # TODO?MID Temporary, needs callbacks and a worker
				waypoint = self.loop.run_until_complete(self.waypoints.get())
				if self.doTerminate:
					self.logger.debug('Terminating navigation loop')
					break
				self.logger.info('Moving to {0}'.format(waypoint))
				self.moveTo(waypoint, interval)
				self.logger.info('Reached {0}'.format(waypoint))
				self.stateLock.release()
			self.logger.debug('Navigation loop terminated')
			self.logger.debug(self.terminated)
			self.terminated = True
			self.logger.debug(self.terminated)
			self.runLock.release()
			self.stateLock.release()
		except Error as err:
			print(err)
			raise err

	def terminate(self):
		if self.terminated:
			return True
		self.stateLock.acquire()
		if not self.running:
			return True
		self.doTerminate = True
		self.stateLock.release()
		self.runLock.acquire()
