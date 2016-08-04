PSYDEWALK
=========

Notes:
- Behaviors have a loose ordering via AFTER dependency
- Some Behaviors are carried out at certain places, others can have varying coordinates (e.g. work vs some bus stop)
- Transports connect places
- Transports use behaviors to simulate movement
- Each behavior has a associated mode, e.g. Pedestrian
- Modes have their own behaviors
- These behaviors activate for a maximum given amount of time controlled by the main behavior

Handoff behaviors:

Handoff behaviors are implemented by bots. Therefor there is a well defined set of rules:

1. A bot can specify specific behaviors to hand off to it
2. A bot can be interrupted by the simulation at any time to:
	- Enhance the simulation (breaks etc)
	- Totally kill the bot behavior (runtime exceeded)
3. A bot always gets a maximum runtime on handoff. It will be interrupted if it exceeds this runtime
4. A bot shouldn't implement simulation features like breaks by itself
5. A bot must decide on transports itself. It can however use the existing transport APIs to decide which transport would be the best
