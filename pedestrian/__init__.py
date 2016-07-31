from ..entity import SmoothMovingEntity
from ..jitter import Jitter
from ..data import DataProvider

class Pedestrian(SmoothMovingEntity, DataProvider, Jitter):
	def __init__(self):
		DataProvider.__init__(self)
		Jitter.__init__(self)
		SmoothMovingEntity.__init__(self)

	def move(self, interval=100):
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
