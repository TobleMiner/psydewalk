from ..entity import NavigateableTrackableEntity
from ..geo import Coordinate

class Driver(NavigateableTrackableEntity):
	"""docstring for Driver"""
	def __init__(self, loc=Coordinate(), speed=13.89, logger='driver'):
		super(Driver, self).__init__('car', loc, speed, logger)
