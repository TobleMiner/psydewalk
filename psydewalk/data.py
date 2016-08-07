from psydewalk.exception import MethodNotImplementedException

class DataProvider():
	def __init__(self):
		pass

class LocationProvider():
	"""docstring for LocationProvider"""

	def getLocation(self):
		raise MethodNotImplementedException()

class PlaceProvider():
	"""docstring for PlaceProvider"""

	def getPlace(self):
		raise MethodNotImplementedException()

class SpeedProvider():
	"""docstring for SpeedProvider"""

	def getSpeed(self):
		raise MethodNotImplementedException()


class TrackingProvider(LocationProvider):
	"""docstring for TrackingProvider"""
	def __init__(self, arg):
		super(TrackingProvider, self).__init__()
		self.arg = arg
