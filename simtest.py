#!/bin/env python3

from psydewalk import Simulation
from psydewalk.human import Human
from psydewalk.geo import Coordinate
from psydewalk.tracking import TrackingServer

import logging

logging.basicConfig(level=logging.INFO)

sim = Simulation()
human = Human(sim, Coordinate(54.355474, 10.131083))

tracker = TrackingServer()
tracker.track('me', human)
tracker.runInBackground()

human.start()
