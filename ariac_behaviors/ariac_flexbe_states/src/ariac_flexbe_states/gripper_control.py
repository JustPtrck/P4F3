#!/usr/bin/env python
import rospy
import rostopic

from flexbe_core import EventState, Logger
from osrf_gear.srv import VacuumGripperControl, VacuumGripperControlRequest, VacuumGripperControlResponse
from osrf_gear.msg import VacuumGripperState
from std_msgs.msg import String


class GripperControl(EventState):
	'''
	Example for a state to demonstrate which functionality is available for state implementation.
	This example lets the behavior wait until the given target_time has passed since the behavior has been started.

	-- enable 	bool 		Enables the vacuum.

	#> arm_id	string		Arm identifier.

	<= continue 			Succesful action.
	<= failed 			Failed.
	<= invalid_id			arm_id Invalid.

	'''

	def __init__(self, enable):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(GripperControl, self).__init__(input_keys = ['arm_id'], outcomes = ['continue', 'failed', 'invalid_id'])

		# Store state parameter for later use.

		self._enable = enable
		# The constructor is called when building the state machine, not when actually starting the behavior.
		# Thus, we cannot save the starting time now and will do so later.
	
	

	def execute(self, userdata):


		if userdata.arm_id == 'arm1':
			gripper_service = '/ariac/arm1/gripper/control'
			
		elif userdata.arm_id == 'arm2':
			gripper_service = '/ariac/arm2/gripper/control'

		else:
			return 'invalid_id'

		rospy.loginfo("Waiting for service")
		rospy.wait_for_service(gripper_service)
		try:
			gripper_control = rospy.ServiceProxy(gripper_service, VacuumGripperControl)
			request = VacuumGripperControlRequest()
			request.enable = self._enable

			service_response = gripper_control(request)

			if service_response.success == True:
				if self._enable == True:
					if userdata.arm_id == 'arm1':
						status = rospy.wait_for_message('/ariac/arm1/gripper/state', VacuumGripperState)
						if status.attached == True:
							return 'continue'
					elif userdata.arm_id == 'arm2':
						status = rospy.wait_for_message('/ariac/arm2/gripper/state', VacuumGripperState)
						if status.attached == True:
							return 'continue'
					else:
						return 'failed'
				else:
					return 'continue'
			else:
				return 'failed'

		except rospy.ServiceException, e:
			rospy.loginfo("Service call failed: %s"%e)
			return 'failed'

		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.
		pass # Nothing to do in this example.


	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		# The following code is just for illustrating how the behavior logger works.
		# Text logged by the behavior logger is sent to the operator and displayed in the GUI.
		pass # Nothing to do in this example.

	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do in this example.


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.

		# In this example, we use this event to set the correct start time.
		pass # Nothing to do in this example.

	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do in this example.
