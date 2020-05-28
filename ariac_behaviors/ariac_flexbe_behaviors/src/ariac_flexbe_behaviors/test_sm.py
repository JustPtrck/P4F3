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
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
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
		# x:322 y:574, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.camera_frame = 'logical_camera_shelf2_frame'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_shelf2'
		_state_machine.userdata.ref_frame = 'torso_main'
		_state_machine.userdata.part = 'gear_part_blue'
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.config_name = 'Full_Shelf'
		_state_machine.userdata.pose = []
		_state_machine.userdata.offset = 0.4
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.joint_values = 'joint_values'
		_state_machine.userdata.joint_names = 'joint_names'
		_state_machine.userdata.tool_link = 'right_ee_link'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('start',
										StartAssignment(),
										transitions={'continue': 'MOve'},
										autonomy={'continue': Autonomy.Off})

			# x:164 y:116
			OperatableStateMachine.add('MOve',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'cam', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:285 y:343
			OperatableStateMachine.add('Compute grasp',
										ComputeGraspAriacState(joint_names=['torso_base_main_joint','right_elbow_joint','right_shoulder_lift_joint','right_shoulder_pan_joint','right_wrist_1_joint','right_wrist_2_joint','right_wrist_3_joint']),
										transitions={'continue': 'move', 'failed': 'Compute grasp'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:295 y:199
			OperatableStateMachine.add('cam',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'Compute grasp', 'failed': 'failed', 'not_found': 'Compute grasp'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:277 y:429
			OperatableStateMachine.add('move',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
