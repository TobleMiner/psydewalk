from geo import Coordinate

from time import sleep
import math

class Entity():
	def __init__(self, loc=Coordinate()):
		self.loc = loc

	def getLocation(self):
		return self.loc

class MovingEntity(Entity):

	DEST_MAX_DIST = 0.23 # Maximum distance to destination for it to be reached

	def __init__(self, loc=Coordinate(), dest=Coordinate(), speed=0):
		super().__init__(loc)
		self.dest = dest
		self.setSpeed(speed)

	def setSpeed(self, speed):
		self.speed = speed

	def move(self, interval=1000):
		while self.loc.dist(self.dest) > self.DEST_MAX_DIST:
			dist = self.loc.dist(self.dest)
			print(dist)
			delta = self.dest - self.loc
			vect = delta / dist
			if dist > self.speed * interval / 1000:
				vect = vect * (self.speed * interval / 1000);
			else:
				vect = vect * self.DEST_MAX_DIST
			self.loc = self.loc + vect
			sleep(interval / 1000)

class SmoothMovingEntity(MovingEntity):
	def __init__(self, loc=Coordinate(), dest=Coordinate(), speed=0):
		self.speed = 0
		super().__init__(loc, dest, speed)

	def setSpeed(self, speed):
		self.speeddelta = speed - self.speed
		self.maxspeed = speed
		self.speedaproxcnt = 0

	def move(self, interval=100):
		self.speedaproxcnt = 0
		while self.loc.dist(self.dest) > self.DEST_MAX_DIST:
			if(self.speeddelta > 0):
				self.speed += (1 - 1 / abs(self.speeddelta)) ** self.speedaproxcnt
			else:
				self.speed -= (1 - 1 / abs(self.speeddelta)) ** self.speedaproxcnt
			self.speedaproxcnt += 1
			dist = self.loc.dist(self.dest)
			delta = self.dest - self.loc
			vect = delta / dist
			if dist > self.speed * interval / 1000:
				vect = vect * (self.speed * interval / 1000);
			else:
				vect = vect * self.DEST_MAX_DIST
			self.loc = self.loc + vect
			sleep(interval / 1000)
