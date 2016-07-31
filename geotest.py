#!/bin/env python3

from psydewalk.geo import Coordinate

home = Coordinate(54.355420, 10.135980)
print(home)

centralpark = Coordinate(40.782783, -73.965409)
print(centralpark)

dist = home.dist(centralpark)
print(dist)

dir = (centralpark - home) / dist
print(dir)

print(home + dir * dist)

print(Coordinate().dist(dir))
