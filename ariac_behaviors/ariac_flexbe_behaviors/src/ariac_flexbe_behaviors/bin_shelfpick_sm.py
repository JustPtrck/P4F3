#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.find_correct_bin import FindPart
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.gripper_control import GripperControl
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.offset_calc import part_offsetCalc
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 01 2020
@author: Patrick Verwimp
'''
class BinShelfPickSM(Behavior):
	'''
	Picks parts from bin
Input part and arm
v1.1
	'''


	def __init__(self):
		super(BinShelfPickSM, self).__init__()
		self.name = 'Bin+ShelfPick'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:982 y:568, x:604 y:185
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part', 'arm_id'])
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.arm_id = 'Left_Arm'
		_state_machine.userdata.tool_link = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.offset = 0.15
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.part = 'gear_part_blue'
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.home = 'Home'
		_state_machine.userdata.safe = 'Full_Bin'
		_state_machine.userdata.Up = 0.2
		_state_machine.userdata.preShelf = 'Gantry_PreShelf'
		_state_machine.userdata.shelf = 'Full_Shelf'
		_state_machine.userdata.one = 1
		_state_machine.userdata.bin = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:89 y:59
			OperatableStateMachine.add('FindPart',
										FindPart(time_out=0.2),
										transitions={'bin': 'BinTo1', 'shelf': 'ToShelf', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'bin': Autonomy.Off, 'shelf': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'part_type': 'part', 'arm_id': 'arm_id', 'gantry_pos': 'config_name', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame'})

			# x:839 y:25
			OperatableStateMachine.add('MoveToPart',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'EnableGripper', 'planning_failed': 'failed', 'control_failed': 'EnableGripper'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1048 y:25
			OperatableStateMachine.add('EnableGripper',
										GripperControl(enable=True),
										transitions={'continue': 'OffsetUp', 'failed': 'MoveToPart', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:167 y:236
			OperatableStateMachine.add('SafePosBetweenBin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPartPose', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'safe', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:107 y:400
			OperatableStateMachine.add('PreGrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputePick_3', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:361 y:25
			OperatableStateMachine.add('Offset',
										part_offsetCalc(),
										transitions={'succes': 'ComputePick', 'unknown_id': 'failed'},
										autonomy={'succes': Autonomy.Off, 'unknown_id': Autonomy.Off},
										remapping={'part_type': 'part', 'part_offset': 'offset'})

			# x:1044 y:400
			OperatableStateMachine.add('ArmHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SafePosBetweenBin_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home', 'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1038 y:475
			OperatableStateMachine.add('SafePosBetweenBin_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'safe', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1025 y:89
			OperatableStateMachine.add('OffsetUp',
										ReplaceState(),
										transitions={'done': 'ComputePick_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Up', 'result': 'offset'})

			# x:970 y:155
			OperatableStateMachine.add('ComputePick_2',
										ComputeGraspAriacState(),
										transitions={'continue': 'MoveToPart_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:938 y:244
			OperatableStateMachine.add('MoveToPart_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Bin1?', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:103 y:469
			OperatableStateMachine.add('ComputePick_3',
										ComputeGraspAriacState(),
										transitions={'continue': 'MoveToPart_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:95 y:540
			OperatableStateMachine.add('MoveToPart_3',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Offset', 'planning_failed': 'MoveToPart_3', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:647 y:24
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(),
										transitions={'continue': 'MoveToPart', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:0 y:171
			OperatableStateMachine.add('ToShelf',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ToShelf1', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'preShelf', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:0 y:233
			OperatableStateMachine.add('ToShelf1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPartPose', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'shelf', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:936 y:329
			OperatableStateMachine.add('Bin1?',
										EqualState(),
										transitions={'true': 'ArmHome_2', 'false': 'ToShelf1_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'bin', 'value_b': 'one'})

			# x:160 y:170
			OperatableStateMachine.add('BinTo1',
										ReplaceState(),
										transitions={'done': 'SafePosBetweenBin'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'one', 'result': 'bin'})

			# x:830 y:467
			OperatableStateMachine.add('ToShelf_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'preShelf', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:826 y:396
			OperatableStateMachine.add('ToShelf1_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ToShelf_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'shelf', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:96 y:330
			OperatableStateMachine.add('GetPartPose',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'PreGrasp', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
