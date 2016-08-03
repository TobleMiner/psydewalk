from datetime import datetime
from psydewalk.transport import TransportRegistry
from psydewalk.transport.transports import *
from psydewalk.place.places import *

__all__ = ['pedestrian', 'tracking']

class Simulation():
	"""docstring for Simulation"""
	def __init__(self):
		super(Simulation, self).__init__()
		self.transportRegistry = TransportRegistry()
		self.placeRegistry = PlaceRegistry()
		self.initPlaces()

	def getDatetime(self):
		return datetime.now()

	def getTransportRegistry(self):
		return self.transportRegistry

	def initPlaces(self):
		self.placeRegistry.addPlace(Home())
		self.placeRegistry.addPlace(Work())

	def getPlaceRegistry(self):
		return self.placeRegistry
