from psydewalk.transport import Transport
from psydewalk.transport.transports import *

class Place():
	"""docstring for Place"""
	def __init__(self, supported):
		self.transport = {}
		self.supported = supported

	def addTransport(self, transport, cnt=1):
		if not transport in self.transport:
			self.transport[transport] = cnt
		else:
			self.transport[transport] += cnt
			if cnt < 0:
				self.transport[transport] = -1 # Infinity

	def removeTransport(self, transport, cnt=1):
		if self.transport[transport] == -1:
			return True
		if self.transport[transport] < cnt:
			return False
		self.transport[transport] -= cnt
		return True

	def getSupportedTransports(self):
		return self.supported

class Home(Place): # TODO?LOW Unserialize palces from human readable config file
	"""docstring for Home"""
	def __init__(self):
		super(Home, self).__init__([Bike, Bus, Foot, Car])
