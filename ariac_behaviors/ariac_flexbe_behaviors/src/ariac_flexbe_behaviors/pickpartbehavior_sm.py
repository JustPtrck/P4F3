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
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_behaviors.cleanpick_drop_sm import CleanPickDropSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 01 2020
@author: Patrick Verwimp
'''
class PickPartBehaviorSM(Behavior):
	'''
	Picks parts from bin
Input part and arm
v2.0
	'''


	def __init__(self):
		super(PickPartBehaviorSM, self).__init__()
		self.name = 'PickPartBehavior'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(CleanPickDropSM, 'CleanPick/Drop')

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
		_state_machine.userdata.part = 'gear_part_red'
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
		_state_machine.userdata.zero = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:118 y:24
			OperatableStateMachine.add('FindPart',
										FindPart(time_out=0.2),
										transitions={'bin': 'BinTo1', 'shelf': 'BinTo0', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'bin': Autonomy.Off, 'shelf': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'part_type': 'part', 'arm_id': 'arm_id', 'gantry_pos': 'config_name', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame'})

			# x:167 y:236
			OperatableStateMachine.add('SafePosBetweenBin',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPartPose', 'planning_failed': 'failed', 'control_failed': 'SafePosBetweenBin', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'safe', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:107 y:400
			OperatableStateMachine.add('PreGrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'CleanPick/Drop', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1044 y:400
			OperatableStateMachine.add('ArmHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'SafePosBetweenBin_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home', 'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1038 y:475
			OperatableStateMachine.add('SafePosBetweenBin_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'SafePosBetweenBin_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'safe', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:0 y:171
			OperatableStateMachine.add('ToShelf',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ToShelf1', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'preShelf', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:0 y:233
			OperatableStateMachine.add('ToShelf1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetPartPose', 'planning_failed': 'failed', 'control_failed': 'ToShelf1', 'param_error': 'failed'},
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
										transitions={'reached': 'ToShelf_2', 'planning_failed': 'failed', 'control_failed': 'ToShelf1_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'shelf', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:96 y:330
			OperatableStateMachine.add('GetPartPose',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'PreGrasp', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:0 y:113
			OperatableStateMachine.add('BinTo0',
										ReplaceState(),
										transitions={'done': 'ToShelf'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'bin'})

			# x:541 y:328
			OperatableStateMachine.add('CleanPick/Drop',
										self.use_behavior(CleanPickDropSM, 'CleanPick/Drop'),
										transitions={'finished': 'Bin1?', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'pose': 'pose', 'arm_id': 'arm_id', 'part': 'part', 'drop': 'one', 'joint_names': 'joint_names', 'joint_values': 'joint_values'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
