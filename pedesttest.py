#!/bin/env python3

from time import sleep
import logging

from psydewalk.pedestrian import Pedestrian
from psydewalk.geo import Coordinate
from psydewalk.tracking import TrackingServer

logging.basicConfig(level=logging.DEBUG)

tracking = TrackingServer()

speed = 25 / 3.6

asdf = Pedestrian(Coordinate(54.355561, 10.131721), speed)

tracking.track('me', asdf)
tracking.runInBackground()

asdf.navigateTo(Coordinate(54.336107, 10.076489))

asdf.run()

sleep(1)
