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
from ariac_flexbe_states.gripper_control import GripperControl
from ariac_flexbe_states.find_correct_bin import FindPart
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 25 2020
@author: Patrick Verwimp
'''
class GetPartRightArmSM(Behavior):
	'''
	Gets product from bin or shelf for right arm
v0.2
	'''


	def __init__(self):
		super(GetPartRightArmSM, self).__init__()
		self.name = 'GetPartRightArm'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:328 y:654, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_type_R'])
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.part_type = part_type_R
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.move_group_R = 'Right_Arm'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = 'gantry'
		_state_machine.userdata.config_name_R = 'Right_Shelf'
		_state_machine.userdata.pose = []
		_state_machine.userdata.offset = 0.03
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.tool_link = 'right_ee_link'
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.config_name = 'Full_Shelf'
		_state_machine.userdata.part_type_R = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('start',
										StartAssignment(),
										transitions={'continue': 'Find'},
										autonomy={'continue': Autonomy.Off})

			# x:290 y:149
			OperatableStateMachine.add('MOve',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'cam', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R', 'move_group': 'move_group_R', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:285 y:343
			OperatableStateMachine.add('Compute grasp',
										ComputeGraspAriacState(joint_names=['right_elbow_joint','right_shoulder_lift_joint','right_shoulder_pan_joint','right_wrist_1_joint','right_wrist_2_joint','right_wrist_3_joint']),
										transitions={'continue': 'move', 'failed': 'Compute grasp'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group_R', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:279 y:232
			OperatableStateMachine.add('cam',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'Compute grasp', 'failed': 'failed', 'not_found': 'Compute grasp'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:277 y:429
			OperatableStateMachine.add('move',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'grip', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group_R', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:274 y:503
			OperatableStateMachine.add('grip',
										GripperControl(enable=True),
										transitions={'continue': 'MOve_2_2', 'failed': 'move', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'move_group_R'})

			# x:293 y:68
			OperatableStateMachine.add('MOve_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MOve', 'planning_failed': 'failed', 'control_failed': 'MOve_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:469 y:553
			OperatableStateMachine.add('MOve_2_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'MOve_2_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:30 y:102
			OperatableStateMachine.add('Find',
										FindPart(time_out=0.2),
										transitions={'found': 'MOve_2', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'part_type': 'part_type', 'gantry_pos': 'gantry_pos', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
