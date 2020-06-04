#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.gripper_control import GripperControl
from ariac_flexbe_states.get_agv_pose import GetAGVPose
from ariac_flexbe_states.ComputeDropPartOffsetGraspAriacState import ComputeDropPartOffsetGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.offset_calc import part_offsetCalc
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.replace_state import ReplaceState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 03 2020
@author: Patrick Verwimp
'''
class PartToAgvSM(Behavior):
	'''
	part to agv
	'''


	def __init__(self):
		super(PartToAgvSM, self).__init__()
		self.name = 'PartToAgv'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:181 y:520, x:145 y:331
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'part_pose', 'arm_id', 'part'])
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.arm_id = ''
		_state_machine.userdata.pre_agv = ''
		_state_machine.userdata.home = 'Home'
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.offset = 0.2
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.part = ''
		_state_machine.userdata.offset_up = 0.1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:101 y:25
			OperatableStateMachine.add('PartInGripper?',
										GripperControl(enable=True),
										transitions={'continue': 'agv_pose', 'failed': 'finished', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:326 y:19
			OperatableStateMachine.add('agv_pose',
										GetAGVPose(ref_frame='world'),
										transitions={'continue': 'AgvPos', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'arm_id': 'arm_id', 'agv_pose': 'agv_pose', 'move_pos': 'pre_agv'})

			# x:1056 y:175
			OperatableStateMachine.add('computeDrop',
										ComputeDropPartOffsetGraspAriacState(),
										transitions={'continue': 'Move', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'part_pose': 'part_pose', 'agv_pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1108 y:243
			OperatableStateMachine.add('Move',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Drop', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1144 y:309
			OperatableStateMachine.add('Drop',
										GripperControl(enable=False),
										transitions={'continue': 'UpOffset', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:1129 y:99
			OperatableStateMachine.add('Offset',
										part_offsetCalc(),
										transitions={'succes': 'computeDrop', 'unknown_id': 'failed'},
										autonomy={'succes': Autonomy.Off, 'unknown_id': Autonomy.Off},
										remapping={'part_type': 'part', 'part_offset': 'offset'})

			# x:524 y:20
			OperatableStateMachine.add('AgvPos',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'computeDrop_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'pre_agv', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:773 y:596
			OperatableStateMachine.add('ArmHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'ArmHome', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home', 'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:684 y:19
			OperatableStateMachine.add('computeDrop_2',
										ComputeDropPartOffsetGraspAriacState(),
										transitions={'continue': 'Move_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'part_pose': 'part_pose', 'agv_pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:915 y:19
			OperatableStateMachine.add('Move_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Offset', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:741 y:446
			OperatableStateMachine.add('computeDrop_3',
										ComputeDropPartOffsetGraspAriacState(),
										transitions={'continue': 'Move_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'part_pose': 'part_pose', 'agv_pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:760 y:528
			OperatableStateMachine.add('Move_3',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'ArmHome', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:765 y:369
			OperatableStateMachine.add('UpOffset',
										ReplaceState(),
										transitions={'done': 'computeDrop_3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'offset_up', 'result': 'offset'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
