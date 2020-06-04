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
from ariac_flexbe_behaviors.bin_shelfpick_sm import BinShelfPickSM
from ariac_flexbe_behaviors.get_order_sm import GetOrderSM
from ariac_flexbe_behaviors.parttoagv_sm import PartToAgvSM
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.equal_state import EqualState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue Jun 02 2020
@author: Patrick Verwimp
'''
class MainAssignment1SM(Behavior):
	'''
	Integration of sub-systems
v1.1
	'''


	def __init__(self):
		super(MainAssignment1SM, self).__init__()
		self.name = 'MainAssignment1'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(BinShelfPickSM, 'RightArmPick')
		self.add_behavior(BinShelfPickSM, 'LeftArmPick')
		self.add_behavior(GetOrderSM, 'Get Order')
		self.add_behavior(PartToAgvSM, 'PartToAgv')
		self.add_behavior(PartToAgvSM, 'PartToAgv_2')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:628 y:339, x:672 y:155
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part_type_R = ''
		_state_machine.userdata.arm_R = 'Right_Arm'
		_state_machine.userdata.part_pose_R = []
		_state_machine.userdata.part_type_L = ''
		_state_machine.userdata.arm_L = 'Left_Arm'
		_state_machine.userdata.part_pose_L = []
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.part_index = 0
		_state_machine.userdata.shipment_index = 0
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.home_pos = 'Full_Home'
		_state_machine.userdata.none = 'None'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:18 y:65
			OperatableStateMachine.add('Start',
										StartAssignment(),
										transitions={'continue': 'MoveHome'},
										autonomy={'continue': Autonomy.Off})

			# x:613 y:28
			OperatableStateMachine.add('RightArmPick',
										self.use_behavior(BinShelfPickSM, 'RightArmPick'),
										transitions={'finished': 'PartTypeL=None', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'part_type_R', 'arm_id': 'arm_R'})

			# x:1030 y:23
			OperatableStateMachine.add('LeftArmPick',
										self.use_behavior(BinShelfPickSM, 'LeftArmPick'),
										transitions={'finished': 'MoveHome_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'part_type_L', 'arm_id': 'arm_L'})

			# x:376 y:23
			OperatableStateMachine.add('Get Order',
										self.use_behavior(GetOrderSM, 'Get Order'),
										transitions={'finished': 'RightArmPick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'shipment_index': 'shipment_index', 'part_index': 'part_index', 'part_type_L': 'part_type_L', 'part_type_R': 'part_type_R', 'agv_id': 'agv_id', 'part_pose_L': 'part_pose_L', 'part_pose_R': 'part_pose_R'})

			# x:940 y:260
			OperatableStateMachine.add('PartToAgv',
										self.use_behavior(PartToAgvSM, 'PartToAgv'),
										transitions={'finished': 'PartTypeL=None_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_pose': 'part_pose_R', 'arm_id': 'arm_R', 'part': 'part_type_R'})

			# x:947 y:403
			OperatableStateMachine.add('PartToAgv_2',
										self.use_behavior(PartToAgvSM, 'PartToAgv_2'),
										transitions={'finished': 'MoveHome', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_pose': 'part_pose_L', 'arm_id': 'arm_L', 'part': 'part_type_L'})

			# x:165 y:109
			OperatableStateMachine.add('MoveHome',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Get Order', 'planning_failed': 'failed', 'control_failed': 'MoveHome', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_pos', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:950 y:198
			OperatableStateMachine.add('MoveHome_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'PartToAgv', 'planning_failed': 'failed', 'control_failed': 'MoveHome_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'home_pos', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:805 y:27
			OperatableStateMachine.add('PartTypeL=None',
										EqualState(),
										transitions={'true': 'MoveHome_2', 'false': 'LeftArmPick'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'none', 'value_b': 'part_type_L'})

			# x:946 y:333
			OperatableStateMachine.add('PartTypeL=None_2',
										EqualState(),
										transitions={'true': 'MoveHome', 'false': 'PartToAgv_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'none', 'value_b': 'part_type_L'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
