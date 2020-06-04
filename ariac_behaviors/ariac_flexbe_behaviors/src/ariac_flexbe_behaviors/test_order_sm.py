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
from flexbe_states.wait_state import WaitState
from flexbe_states.log_state import LogState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_behaviors.get_order_sm import GetOrderSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 28 2020
@author: PV
'''
class TestOrderSM(Behavior):
	'''
	tests order
	'''


	def __init__(self):
		super(TestOrderSM, self).__init__()
		self.name = 'Test Order'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(GetOrderSM, 'Get Order')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:30 y:365, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.shipment_index = 0
		_state_machine.userdata.part_index = 0
		_state_machine.userdata.part_type_L = ''
		_state_machine.userdata.part_type_R = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.part_pose_L = []
		_state_machine.userdata.part_pose_R = []
		_state_machine.userdata.order_id = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:30 y:40
			OperatableStateMachine.add('Start',
										StartAssignment(),
										transitions={'continue': 'Get Order'},
										autonomy={'continue': Autonomy.Off})

			# x:218 y:153
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=3),
										transitions={'done': 'Get Order'},
										autonomy={'done': Autonomy.Off})

			# x:456 y:100
			OperatableStateMachine.add('Log',
										LogState(text="done", severity=Logger.REPORT_INFO),
										transitions={'done': 'message'},
										autonomy={'done': Autonomy.Off})

			# x:510 y:253
			OperatableStateMachine.add('message',
										MessageState(),
										transitions={'continue': 'message_2'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_type_L'})

			# x:510 y:330
			OperatableStateMachine.add('message_2',
										MessageState(),
										transitions={'continue': 'Wait'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_type_R'})

			# x:159 y:25
			OperatableStateMachine.add('Get Order',
										self.use_behavior(GetOrderSM, 'Get Order'),
										transitions={'finished': 'Log', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'shipment_index': 'shipment_index', 'part_index': 'part_index', 'order_id': 'order_id', 'part_type_L': 'part_type_L', 'part_type_R': 'part_type_R', 'agv_id': 'agv_id', 'part_pose_L': 'part_pose_L', 'part_pose_R': 'part_pose_R'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
