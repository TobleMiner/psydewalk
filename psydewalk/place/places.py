from psydewalk.place import Place
from psydewalk.geo import Coordinate

class Home(Place): # TODO?LOW Unserialize palces from human readable config file
	"""docstring for Home"""
	def __init__(self):
		from psydewalk.transport.transports import Bike, Bus, Foot, Car
		super(Home, self).__init__([Bike, Bus, Foot, Car])
		self.loc = Coordinate(54.358255, 10.130676)
		self.subplaces = {
			ParkingLot: ParkingLot(Coordinate(54.358234, 10.131358)),
			BikeRack: BikeRack(Coordinate(54.358315, 10.130948)),
			BusStop: BusStop(self.loc)
		}

class Work(Place): # TODO?LOW Unserialize palces from human readable config file
	"""docstring for Work"""
	def __init__(self):
		from psydewalk.transport.transports import Bike, Bus, Foot, Car
		super(Work, self).__init__([Bike, Bus, Foot, Car])
		self.loc = Coordinate(54.338405, 10.122131)
		self.subplaces = {
			ParkingLot: [ParkingLot(Coordinate(54.336912, 10.123043)), ParkingLot(Coordinate(54.338886, 10.123417))],
			BikeRack: [BikeRack(Coordinate(54.337957, 10.122981)), BikeRack(Coordinate(54.338457, 10.123523))],
			BusStop: BusStop(self.loc)
		}

class Park(Place):
	"""docstring for Park"""
	def __init__(self, arg):
		from psydewalk.transport.transports import Bike, Bus, Foot, Car
		super(Park, self).__init__([Bike, Foot, Car])
		self.loc = Coordinate(54.345244, 10.124970)
		self.subplaces = {
			ParkingLot: [ParkingLot(Coordinate(54.343934, 10.127762)), ParkingLot(Coordinate(54.344841, 10.127842))],
			BikeRack: BikeRack(Coordinate(54.345535, 10.128303))
		}


class ParkingLot(Place):
	"""docstring for ParkingLot"""
	def __init__(self, loc):
		super(ParkingLot, self).__init__()
		self.loc = loc

class BikeRack(Place):
	"""docstring for BikeRack"""
	def __init__(self, loc):
		super(BikeRack, self).__init__()
		self.loc = loc

class BusStop(Place):
	"""docstring for BusStop"""
	def __init__(self, loc):
		super(BusStop, self).__init__()
		self.loc = loc

	def getLocation(self):
		return self.loc # TODO?LOW Use OSM to find nearest bus stop
