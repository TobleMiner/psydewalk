#!/bin/env python3

from pyroutelib2.route import Router
from pyroutelib2.loadOsm import LoadOsm

osm = LoadOsm("foot")

#home = osm.findNode(54.355561, 10.131721)
home = osm.findNode(54.357069, 10.130382)

#finance = osm.findNode(54.344639, 10.132518)
finance = osm.findNode(54.310372, 10.131111)

print(home)
print(finance)

router = Router(osm)
result, route = router.doRoute(home, finance)

if result == 'success':
	for i in route:
		node = osm.rnodes[i]
		print("%d: %f,%f" % (i,node[0],node[1]))
else:
	print('Failed to get route: ' + result)
