from psydewalk.transport import Transport
from psydewalk.behavior.behaviors import *

class Car(Transport): # TODO?LOW Unserialize transports from human readable config file
	"""docstring for Car"""
	BEHAVIOR = DriveTo
	PLACE = ParkingLot

	def __init__(self, registry):
		super(Car, self).__init__(registry) # TODO?HIGH Implement behaviors

class Bus(Transport):
	BEHAVIOR = DriveTo
	PLACE = BusStop

	"""docstring for Bus"""
	def __init__(self, registry):
		super(Bus, self).__init__()

class Foot(Transport):
	BEHAVIOR = WalkTo
	PLACE = None

	"""docstring for Foot"""
	def __init__(self, registry):
		super(Foot, self).__init__()

class Bike(Transport):
	BEHAVIOR = RideTo
	PLACE = BikeRack

	"""docstring for Bike"""
	def __init__(self, registry):
		super(Bike, self).__init__()
