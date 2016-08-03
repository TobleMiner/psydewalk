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

Behavior lifecycle:
1. Instanciation, pass manager object
2. Read information like behavior place/location
3. Populate and terminate behavior
4. Initiate transport to place
5. Run behavior after arriving
