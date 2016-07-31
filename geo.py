import math

EARTH_RADIUS = 6378137

class Coordinate():
	def __init__(self, lat=0, lng=0):
		self.lat = lat
		self.lng = lng
		self.__div__ = self.__truediv__

	def __add__(self, coord):
		lat = (90 + (self.lat + coord.lat)) % 180 - 90
		lng = (180 + (self.lng + coord.lng)) % 360 - 180
		return Coordinate(lat, lng)

	def __sub__(self, coord):
		lat = (90 + (self.lat - coord.lat)) % 180 - 90
		lng = (180 + (self.lng - coord.lng)) % 360 - 180
		return Coordinate(lat, lng)

	def __mul__(self, scalar):
		lat = (90 + (self.lat * scalar)) % 180 - 90
		lng = (180 + (self.lng * scalar)) % 360 - 180
		return Coordinate(lat, lng)

	def __truediv__(self, scalar):
		return self * (1 / scalar)

	def __str__(self):
		return '({0} N, {1} E)'.format(self.lat, self.lng)

	def dist(self, coord):
		dlat = math.radians(coord.lat - self.lat)
		dlng = math.radians(coord.lng - self.lng)
		fact = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(self.lat)) * math.cos(math.radians(coord.lat)) * math.sin(dlng / 2) * math.sin(dlng / 2)
		fact = 2 * math.atan2(math.sqrt(fact), math.sqrt(1 - fact))
		return EARTH_RADIUS * fact
