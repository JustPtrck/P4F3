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
from ariac_flexbe_states.compute_bin_drop import ComputeDropPart
from ariac_flexbe_states.gripper_control import GripperControl
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jun 05 2020
@author: Wouter Lax
'''
class Place_Blue_PartSM(Behavior):
	'''
	Place the blue picked part
[Version]
	'''


	def __init__(self):
		super(Place_Blue_PartSM, self).__init__()
		self.name = 'Place_Blue_Part'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:884 y:573, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.arm_id = 'Right_Arm'
		_state_machine.userdata.pose = []
		_state_machine.userdata.offset = 0.020
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_stock1'
		_state_machine.userdata.camera_frame = 'logical_camera_stock1_frame'
		_state_machine.userdata.home = 'Gantry_Home'
		_state_machine.userdata.part = 'gasket_part_blue'
		_state_machine.userdata.full_home = 'Full_Home_Blue'
		_state_machine.userdata.clearance = 0.05
		_state_machine.userdata.bin = 'Gantry_Bin_Blue'
		_state_machine.userdata.bin_pose = []
		_state_machine.userdata.part_pose = 'None'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:102 y:30
			OperatableStateMachine.add('Move_Bin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Get_Object_Place', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'bin', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:312 y:27
			OperatableStateMachine.add('Compute_Place',
										ComputeDropPart(),
										transitions={'continue': 'Move_To_Place', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'part_pose': 'part_pose', 'bin_pose': 'bin_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:698 y:26
			OperatableStateMachine.add('Gripper_Off',
										GripperControl(enable=False),
										transitions={'continue': 'Add_Clearance', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:842 y:232
			OperatableStateMachine.add('Move_Clear',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Move_Home', 'planning_failed': 'Move_Home', 'control_failed': 'Move_Clear'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:844 y:24
			OperatableStateMachine.add('Add_Clearance',
										AddNumericState(),
										transitions={'done': 'Compute_Place_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'clearance', 'value_b': 'offset', 'result': 'offset'})

			# x:846 y:330
			OperatableStateMachine.add('Move_Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'full_home', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:482 y:20
			OperatableStateMachine.add('Move_To_Place',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Gripper_Off', 'planning_failed': 'failed', 'control_failed': 'Gripper_Off'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:24 y:178
			OperatableStateMachine.add('Get_Object_Place',
										GetObjectPoseState(object_frame='bin1_frame', ref_frame='world'),
										transitions={'continue': 'Compute_Place', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'bin_pose'})

			# x:854 y:117
			OperatableStateMachine.add('Compute_Place_2',
										ComputeDropPart(),
										transitions={'continue': 'Move_Clear', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'part_pose': 'part_pose', 'bin_pose': 'bin_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
