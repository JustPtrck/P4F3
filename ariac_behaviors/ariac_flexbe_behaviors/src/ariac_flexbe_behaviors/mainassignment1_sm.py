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
	'''


	def __init__(self):
		super(MainAssignment1SM, self).__init__()
		self.name = 'MainAssignment1'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(BinShelfPickSM, 'RightArmPick')
		self.add_behavior(BinShelfPickSM, 'LeftArmPick')
		self.add_behavior(GetOrderSM, 'Get Order')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:825 y:299, x:130 y:365
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

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:18 y:65
			OperatableStateMachine.add('Start',
										StartAssignment(),
										transitions={'continue': 'Get Order'},
										autonomy={'continue': Autonomy.Off})

			# x:433 y:91
			OperatableStateMachine.add('RightArmPick',
										self.use_behavior(BinShelfPickSM, 'RightArmPick'),
										transitions={'finished': 'LeftArmPick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'part_type_R', 'arm_id': 'arm_R'})

			# x:793 y:84
			OperatableStateMachine.add('LeftArmPick',
										self.use_behavior(BinShelfPickSM, 'LeftArmPick'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'part_type_L', 'arm_id': 'arm_L'})

			# x:148 y:83
			OperatableStateMachine.add('Get Order',
										self.use_behavior(GetOrderSM, 'Get Order'),
										transitions={'finished': 'RightArmPick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'shipment_index': 'shipment_index', 'part_index': 'part_index', 'part_type_L': 'part_type_L', 'part_type_R': 'part_type_R', 'agv_id': 'agv_id', 'part_pose_L': 'part_pose_L', 'part_pose_R': 'part_pose_R'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
