from ..entity import NavigateableTrackableEntity
from ..geo import Coordinate


class Pedestrian(NavigateableTrackableEntity):
	def __init__(self, loc=Coordinate(), speed=1.67, logger='pedestrian'):
		super(Pedestrian, self).__init__('foot', loc, speed, logger)
