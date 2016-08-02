#!/bin/env python3

from psydewalk import Simulation
from psydewalk.human import Human

import logging

logging.basicConfig(level=logging.DEBUG)

sim = Simulation()
human = Human(sim)

