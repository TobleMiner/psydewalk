#!/bin/env python3

from time import sleep

from datetime import datetime, timedelta
from psydewalk.timing import Alarm

class Foo():
	def __init__(self):
		self.foo = 'bar'

	def foobar(self):
		print(self.foo)

class Sim():
	def getDatetime(self):
		return datetime.now()

alarm = Alarm(Sim())
dt = timedelta(seconds=3)
now = datetime.now()
foo = Foo()

alarm.setup(now + dt, foo.foobar)
alarm.start()

