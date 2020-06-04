#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_behaviors.waitstate_sm import WaitstateSM
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.cumpute_bin_drop import ComputeDropPart
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 03 2020
@author: Wouter Lax
'''
class BluePartSM(Behavior):
	'''
	Program to pick and place the blue parts from the belt to the correct bin
	'''


	def __init__(self):
		super(BluePartSM, self).__init__()
		self.name = 'BluePart'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(WaitstateSM, 'Waitstate')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:386 y:51, x:238 y:167
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part', 'arm_id'])
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.arm_id = 'Right_Arm'
		_state_machine.userdata.tool_link = 'right_ee_link'
		_state_machine.userdata.pose = []
		_state_machine.userdata.offset = 0
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.home = 'Home'
		_state_machine.userdata.part = ''
		_state_machine.userdata.belt = 'Gantry_PreShelf'
		_state_machine.userdata.agv_pose = ''
		_state_machine.userdata.part_pose = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('Move_Belt',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Bin_Pose', 'planning_failed': 'Waitstate', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'belt', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:26 y:242
			OperatableStateMachine.add('Waitstate',
										self.use_behavior(WaitstateSM, 'Waitstate'),
										transitions={'finished': 'Move_Belt', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:400 y:146
			OperatableStateMachine.add('Bin_Pose',
										GetObjectPoseState(object_frame='bin5', ref_frame='world'),
										transitions={'continue': 'Compute_drop', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'bin_pose'})

			# x:614 y:186
			OperatableStateMachine.add('Compute_drop',
										ComputeDropPart(),
										transitions={'continue': 'Detect_Part', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'part_pose': 'part_pose', 'agv_pose': 'bin_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:776 y:184
			OperatableStateMachine.add('Detect_Part',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'finished', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'part_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
