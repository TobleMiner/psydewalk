from psydewalk.exception import MethodNotImplementedException

class DataProvider():
	def __init__(self):
		pass

class LocationProvider():
	"""docstring for LocationProvider"""
	def __init__(self):
		super(LocationProvider, self).__init__()

	def getLocation(self):
		raise MethodNotImplementedException()
