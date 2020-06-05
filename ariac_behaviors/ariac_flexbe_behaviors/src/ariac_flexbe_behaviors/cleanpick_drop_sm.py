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
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.offset_calc import part_offsetCalc
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Jun 05 2020
@author: Patrick Verwimp
'''
class CleanPickDropSM(Behavior):
	'''
	Picks or drops parts smoothly
	'''


	def __init__(self):
		super(CleanPickDropSM, self).__init__()
		self.name = 'CleanPick/Drop'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1179 y:428, x:477 y:521
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['pose', 'arm_id', 'part'])
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.pose = ''
		_state_machine.userdata.arm_id = ''
		_state_machine.userdata.offset = 1
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.drop = 0
		_state_machine.userdata.one = 1
		_state_machine.userdata.zero = 0
		_state_machine.userdata.part = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:106 y:45
			OperatableStateMachine.add('CheckGripper',
										GripperControl(enable=True),
										transitions={'continue': 'drop1', 'failed': 'drop0', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:392 y:264
			OperatableStateMachine.add('ComputeLocation',
										ComputeGraspAriacState(),
										transitions={'continue': 'Move_2', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1015 y:163
			OperatableStateMachine.add('ComputePostLocation',
										ComputeGraspAriacState(),
										transitions={'continue': 'Move_3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:400 y:343
			OperatableStateMachine.add('Offset',
										part_offsetCalc(),
										transitions={'succes': 'ComputeLocation', 'unknown_id': 'failed'},
										autonomy={'succes': Autonomy.Off, 'unknown_id': Autonomy.Off},
										remapping={'part_type': 'part', 'part_offset': 'offset'})

			# x:1010 y:91
			OperatableStateMachine.add('AddOffset',
										AddNumericState(),
										transitions={'done': 'ComputePostLocation'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'offset', 'value_b': 'offset', 'result': 'offset'})

			# x:113 y:346
			OperatableStateMachine.add('Move',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Offset', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:387 y:171
			OperatableStateMachine.add('Move_2',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Drop?', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1006 y:238
			OperatableStateMachine.add('Move_3',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:808 y:238
			OperatableStateMachine.add('EnableGripper',
										GripperControl(enable=True),
										transitions={'continue': 'AddOffset', 'failed': 'ComputeLocation', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:809 y:58
			OperatableStateMachine.add('DisableGripper',
										GripperControl(enable=False),
										transitions={'continue': 'AddOffset', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:188 y:159
			OperatableStateMachine.add('drop1',
										ReplaceState(),
										transitions={'done': 'ComputePreLocation'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'one', 'result': 'drop'})

			# x:0 y:161
			OperatableStateMachine.add('drop0',
										ReplaceState(),
										transitions={'done': 'ComputePreLocation'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'zero', 'result': 'drop'})

			# x:581 y:60
			OperatableStateMachine.add('Drop?',
										EqualState(),
										transitions={'true': 'DisableGripper', 'false': 'EnableGripper'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'drop', 'value_b': 'one'})

			# x:116 y:265
			OperatableStateMachine.add('ComputePreLocation',
										ComputeGraspAriacState(),
										transitions={'continue': 'Move', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
