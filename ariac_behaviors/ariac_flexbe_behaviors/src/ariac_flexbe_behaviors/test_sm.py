#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from flexbe_states.log_state import LogState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 25 2020
@author: PV
'''
class TestSM(Behavior):
	'''
	test v1
	'''


	def __init__(self):
		super(TestSM, self).__init__()
		self.name = 'Test'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.camera_frame = 'logical_camera_bins2_frame'
		_state_machine.userdata.camera_topic = 'ariac/logical_camera_bins2'
		_state_machine.userdata.ref_frame = 'torso_base_main_joint'
		_state_machine.userdata.part = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('start',
										StartAssignment(),
										transitions={'continue': 'scan'},
										autonomy={'continue': Autonomy.Off})

			# x:148 y:149
			OperatableStateMachine.add('scan',
										DetectFirstPartCameraAriacState(part_list=[pulley_part, gear_part_blue, gear_part_red], time_out=0.5),
										transitions={'continue': 'log', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:30 y:102
			OperatableStateMachine.add('log',
										LogState(text=part, severity=Logger.REPORT_INFO),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
