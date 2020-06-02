#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger


class part_offsetCalc(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	># part_type	string 		part name
	#> part_offset	float		part part_offset

	<= succes 			Given time has passed.
	<= unknown_id 				Example for a failure outcome.

	'''

	def __init__(self):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(part_offsetCalc, self).__init__(input_keys = ['part_type'], output_keys = ['part_offset'], outcomes = ['succes', 'unknown_id'])

		# Store state parameter for later use.
		

		# The constructor is called when building the state machine, not when actually starting the behavior.
		# Thus, we cannot save the starting time now and will do so later.
	


	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.

		if self._part == 'gear_part_red':
			userdata.part_offset = 0.02
			return 'succes'
		elif self._part == 'piston_rod_part_red':
			userdata.part_offset = 0.015
			return 'succes'
		elif self._part == 'pulley_part_red':
			userdata.part_offset = 0.08
			return 'succes'
		elif self._part == 'gasket_part_red':
			userdata.part_offset = 0.03
			return 'succes'
		elif self._part == 'gear_part_blue':
			userdata.part_offset = 0.02
			return 'succes'
		elif self._part == 'piston_rod_part_blue':
			userdata.part_offset = 0.015
			return 'succes'
		elif self._part == 'pulley_part_blue':
			userdata.part_offset = 0.08
			return 'succes'
		elif self._part == 'gasket_part_blue':
			userdata.part_offset = 0.03
			return 'succes'
		else:
			return 'unknown_id'


	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		# The following code is just for illustrating how the behavior logger works.
		# Text logged by the behavior logger is sent to the operator and displayed in the GUI.
		self._part = userdata.part_type


	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything unknown_id, the behavior would not even be started.

		# In this example, we use this event to set the correct start time.
		pass # Nothing to do in this example.


	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do in this example.
		
