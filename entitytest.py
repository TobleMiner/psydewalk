#!/bin/env python3

from entity import *
from geo import Coordinate

from datetime import datetime

from threading import Thread

def wörkwörk(entity):
	start = datetime.now()
	print('Start: ' + str(start))
	
	entity.move()
	
	end = datetime.now()
	print('End: ' + str(end))
	print('Duration: ' + str(end - start))

home = Coordinate(54.355420, 10.135980)

finance = Coordinate(54.355695, 10.131490)

speed = 25 / 3.6

dist = home.dist(finance)

print('distance: {0} m, speed: {1} m/s, duration: {2} s'.format(dist, speed, dist / speed))

entity = SmoothMovingEntity(home, finance, speed)

Thread(target=wörkwörk, args=(entity,)).start()

sleep(2)

print('SPEED=2')
entity.setSpeed(2)

sleep(5)

print('SPEED=25')
entity.setSpeed(25)

