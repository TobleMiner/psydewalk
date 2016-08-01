#!/bin/env python3

from psydewalk import Simulation, behavior
from psydewalk.behavior import BehaviorManager

sim = Simulation()
mngr = BehaviorManager(sim)

print(mngr.getNextBehavior(behavior.Sleep))
