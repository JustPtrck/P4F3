#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_flexbe_behaviors.sendagv_sm import SendAGVSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 28 2020
@author: Patrick Verwimp
'''
class GetOrderSM(Behavior):
	'''
	Loads order, outputs 2 parts
v1.0
	'''


	def __init__(self):
		super(GetOrderSM, self).__init__()
		self.name = 'Get Order'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(SendAGVSM, 'SendAGV')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1281 y:234, x:672 y:189
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['shipment_index', 'part_index'], output_keys=['part_type_L', 'part_type_R', 'agv_id', 'part_pose_L', 'part_pose_R', 'shipment_index', 'part_index'])
		_state_machine.userdata.order_id = ''
		_state_machine.userdata.shipments = ''
		_state_machine.userdata.number_of_shipments = 0
		_state_machine.userdata.shipment_index = 0
		_state_machine.userdata.shipment_type = ''
		_state_machine.userdata.products = []
		_state_machine.userdata.number_of_products = 0
		_state_machine.userdata.part_index = 0
		_state_machine.userdata.part_type_R = ''
		_state_machine.userdata.part_pose_L = []
		_state_machine.userdata.part_type_L = []
		_state_machine.userdata.part_pose_R = []
		_state_machine.userdata.add_one = 1
		_state_machine.userdata.reset = 0
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.none = 'None'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:253 y:450
			OperatableStateMachine.add('ShipmentReady?',
										EqualState(),
										transitions={'true': 'ResetPartIndex', 'false': 'GetRPartPose'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_products', 'value_b': 'part_index'})

			# x:442 y:38
			OperatableStateMachine.add('GetShipment',
										GetProductsFromShipmentState(),
										transitions={'continue': 'GetRPartPose', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'shipment_index', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:658 y:37
			OperatableStateMachine.add('GetRPartPose',
										GetPartFromProductsState(),
										transitions={'continue': 'IncrementPartIndex', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'part_index', 'type': 'part_type_R', 'pose': 'part_pose_R'})

			# x:853 y:181
			OperatableStateMachine.add('GetLPartPose',
										GetPartFromProductsState(),
										transitions={'continue': 'IncrementPartIndex_2', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'part_index', 'type': 'part_type_L', 'pose': 'part_pose_L'})

			# x:1046 y:185
			OperatableStateMachine.add('IncrementShipIndex',
										AddNumericState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'add_one', 'result': 'shipment_index'})

			# x:262 y:171
			OperatableStateMachine.add('OrderReady?',
										EqualState(),
										transitions={'true': 'ResetShipmentIndex', 'false': 'GetShipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_shipments', 'value_b': 'shipment_index'})

			# x:853 y:253
			OperatableStateMachine.add('IncrementPartIndex_2',
										AddNumericState(),
										transitions={'done': 'ShipmentReady2?2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'part_index', 'value_b': 'add_one', 'result': 'part_index'})

			# x:853 y:111
			OperatableStateMachine.add('ShipmentReady2?',
										EqualState(),
										transitions={'true': 'None', 'false': 'GetLPartPose'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_products', 'value_b': 'part_index'})

			# x:249 y:387
			OperatableStateMachine.add('ResetPartIndex',
										ReplaceState(),
										transitions={'done': 'ShipIndex0'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'reset', 'result': 'part_index'})

			# x:260 y:107
			OperatableStateMachine.add('ResetShipmentIndex',
										ReplaceState(),
										transitions={'done': 'GetOrder'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'reset', 'result': 'shipment_index'})

			# x:261 y:38
			OperatableStateMachine.add('GetOrder',
										GetOrderState(),
										transitions={'continue': 'GetShipment'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:1044 y:110
			OperatableStateMachine.add('None',
										ReplaceState(),
										transitions={'done': 'IncrementShipIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'none', 'result': 'part_type_L'})

			# x:850 y:36
			OperatableStateMachine.add('IncrementPartIndex',
										AddNumericState(),
										transitions={'done': 'ShipmentReady2?'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'part_index', 'value_b': 'add_one', 'result': 'part_index'})

			# x:1041 y:257
			OperatableStateMachine.add('ShipmentReady2?2',
										EqualState(),
										transitions={'true': 'IncrementShipIndex', 'false': 'finished'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_products', 'value_b': 'part_index'})

			# x:348 y:230
			OperatableStateMachine.add('SendAGV',
										self.use_behavior(SendAGVSM, 'SendAGV'),
										transitions={'finished': 'OrderReady?', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type'})

			# x:215 y:313
			OperatableStateMachine.add('ShipIndex0',
										EqualState(),
										transitions={'true': 'OrderReady?', 'false': 'SendAGV'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'reset'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
