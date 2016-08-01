#!/bin/env python3

from time import sleep
import logging

from psydewalk.pedestrian import Pedestrian
from psydewalk.geo import Coordinate
from psydewalk.tracking import TrackingServer

from pyroutelib2.route import Router
from pyroutelib2.loadOsm import LoadOsm

logging.basicConfig(level=logging.DEBUG)

osm = LoadOsm("foot")

tracking = TrackingServer()

speed = 25 / 3.6

asdf = Pedestrian(Coordinate(54.355561, 10.131721), speed)

tracking.track('me', asdf)
tracking.runInBackground()

home = osm.findNode(54.357069, 10.130382)
finance = osm.findNode(54.310372, 10.131111)

print(home)
print(finance)

router = Router(osm)
result, route = router.doRoute(home, finance)

if result == 'success':
	for i in route:
		node = osm.rnodes[i]
		print("%d: %f,%f" % (i,node[0],node[1]))
		asdf.addWaypoint(Coordinate(node[0], node[1]))
else:
	print('Failed to get route: ' + result)


asdf.run()

