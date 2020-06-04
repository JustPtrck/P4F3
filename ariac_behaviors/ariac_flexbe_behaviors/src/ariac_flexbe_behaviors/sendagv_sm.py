#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.notify_shipment_ready_state import NotifyShipmentReadyState
from flexbe_states.wait_state import WaitState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.get_agv_status_state import GetAgvStatusState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 04 2020
@author: Patrick Verwimp
'''
class SendAGVSM(Behavior):
	'''
	sends agv
	'''


	def __init__(self):
		super(SendAGVSM, self).__init__()
		self.name = 'SendAGV'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:541 y:178, x:142 y:179
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'shipment_type'])
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.shipment_type = ''
		_state_machine.userdata.inspection_result = ''
		_state_machine.userdata.succes = 0
		_state_machine.userdata.agv_state = ''
		_state_machine.userdata.agv_ready_state = 'ready_to_deliver'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:40 y:32
			OperatableStateMachine.add('ShipmentReady',
										NotifyShipmentReadyState(),
										transitions={'continue': 'Wait', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type', 'success': 'success', 'message': 'message'})

			# x:222 y:29
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=0.2),
										transitions={'done': 'AgvState'},
										autonomy={'done': Autonomy.Off})

			# x:320 y:235
			OperatableStateMachine.add('AGVReady',
										EqualState(),
										transitions={'true': 'finished', 'false': 'Wait'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_state', 'value_b': 'agv_ready_state'})

			# x:354 y:27
			OperatableStateMachine.add('AgvState',
										GetAgvStatusState(),
										transitions={'continue': 'AGVReady', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'agv_state': 'agv_state'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
