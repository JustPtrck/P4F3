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
from ariac_flexbe_behaviors.waitstate_sm import WaitstateSM
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from ariac_flexbe_behaviors.pick_red_part_sm import Pick_Red_PartSM
from ariac_flexbe_behaviors.place_red_part_sm import Place_Red_PartSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 02 2020
@author: Wouter Lax + Patrick Verwimp
'''
class IncomminggoodsSM(Behavior):
	'''
	Version 1
	'''


	def __init__(self):
		super(IncomminggoodsSM, self).__init__()
		self.name = 'Incomming goods'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(WaitstateSM, 'Waitstate')
		self.add_behavior(WaitstateSM, 'Waitstate_2')
		self.add_behavior(Pick_Red_PartSM, 'Pick_Red_Part')
		self.add_behavior(Place_Red_PartSM, 'Place_Red_Part')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1214 y:275, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_belt'
		_state_machine.userdata.camera_frame = 'logical_camera_belt_frame'
		_state_machine.userdata.home = 'Home'
		_state_machine.userdata.safe = 'Gantry_Bin'
		_state_machine.userdata.Up = 0.2
		_state_machine.userdata.power_off = 0
		_state_machine.userdata.power_on = 100
		_state_machine.userdata.move_group_gantry = 'Gantry'
		_state_machine.userdata.move_group_left = 'Left_Arm'
		_state_machine.userdata.move_group_right = 'Right_Arm'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:204 y:28
			OperatableStateMachine.add('Start_Assignment',
										StartAssignment(),
										transitions={'continue': 'Detect_Part'},
										autonomy={'continue': Autonomy.Off})

			# x:598 y:28
			OperatableStateMachine.add('Waitstate',
										self.use_behavior(WaitstateSM, 'Waitstate'),
										transitions={'finished': 'Move_R1_Home', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:358 y:118
			OperatableStateMachine.add('Stop_Belt',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'Move_R1_Home', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'power_off'})

			# x:788 y:28
			OperatableStateMachine.add('Waitstate_2',
										self.use_behavior(WaitstateSM, 'Waitstate_2'),
										transitions={'finished': 'Move_R2_Home', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:597 y:131
			OperatableStateMachine.add('Move_R1_Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move_R2_Home', 'planning_failed': 'Waitstate', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home', 'move_group': 'move_group_left', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:797 y:132
			OperatableStateMachine.add('Move_R2_Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Pick_Red_Part', 'planning_failed': 'Waitstate_2', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home', 'move_group': 'move_group_right', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:358 y:34
			OperatableStateMachine.add('Detect_Part',
										DetectFirstPartCameraAriacState(part_list=['gasket_part_blue','piston_rod_part_red'], time_out=0.5),
										transitions={'continue': 'Stop_Belt', 'failed': 'Detect_Part', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:1000 y:122
			OperatableStateMachine.add('Pick_Red_Part',
										self.use_behavior(Pick_Red_PartSM, 'Pick_Red_Part'),
										transitions={'finished': 'Place_Red_Part', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1002 y:218
			OperatableStateMachine.add('Place_Red_Part',
										self.use_behavior(Place_Red_PartSM, 'Place_Red_Part'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
