from psydewalk.geo import Coordinate

from time import sleep
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

	def setSpeed(self, speed):
		self.speeddelta = speed - self.speed
		self.logger.debug('Setting speed: {0} m/s, delta: {1} m/s'.format(speed, self.speeddelta))
		self.maxspeed = speed
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
