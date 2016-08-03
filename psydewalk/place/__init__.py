from psydewalk.data import LocationProvider
from psydewalk.exception import MissingInfrastructureException

class Place(LocationProvider):
	"""docstring for Place"""
	def __init__(self, supported):
		super().__init__(self)
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

	def getTransportEndpoint(self, transport):
		if not transport.PLACE:
			return self.getLocation()
		if not transport.PLACE in self.subplaces:
			raise MissingInfrastructureException(self, transport)
		return self.getSubplace(transport.PLACE)

	def getSubplace(self, type): # Name is a bit deceiving, can return multiple places as an array
		return self.subplaces[type]

	def getLocation(self):
		return self.loc

	class PlaceRegistry():
		"""docstring for PlaceRegistry"""
		def __init__(self):
			super(PlaceRegistry, self).__init__()
			self.places = {}

		def addPlace(self, place):
			self.places[type(place)] = place
