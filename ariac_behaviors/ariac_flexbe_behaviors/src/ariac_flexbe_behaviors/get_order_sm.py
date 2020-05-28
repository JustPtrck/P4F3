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

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1142 y:195, x:672 y:189
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

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:260 y:295
			OperatableStateMachine.add('ShipmentReady?',
										EqualState(),
										transitions={'true': 'ResetPartIndex', 'false': 'GetLeftPartPose'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_products', 'value_b': 'part_index'})

			# x:442 y:38
			OperatableStateMachine.add('GetShipment',
										GetProductsFromShipmentState(),
										transitions={'continue': 'GetLeftPartPose', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'shipment_index', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:658 y:37
			OperatableStateMachine.add('GetLeftPartPose',
										GetPartFromProductsState(),
										transitions={'continue': 'IncrementPartIndex', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'part_index', 'type': 'part_type_L', 'pose': 'part_pose_L'})

			# x:853 y:181
			OperatableStateMachine.add('GetRightPartPose',
										GetPartFromProductsState(),
										transitions={'continue': 'IncrementPartIndex_2', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'part_index', 'type': 'part_type_R', 'pose': 'part_pose_R'})

			# x:853 y:37
			OperatableStateMachine.add('IncrementPartIndex',
										AddNumericState(),
										transitions={'done': 'ShipmentReady2?'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'part_index', 'value_b': 'add_one', 'result': 'part_index'})

			# x:261 y:166
			OperatableStateMachine.add('OrderReady?',
										EqualState(),
										transitions={'true': 'ResetShipmentIndex', 'false': 'GetShipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_shipments', 'value_b': 'shipment_index'})

			# x:853 y:253
			OperatableStateMachine.add('IncrementPartIndex_2',
										AddNumericState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'part_index', 'value_b': 'add_one', 'result': 'part_index'})

			# x:853 y:111
			OperatableStateMachine.add('ShipmentReady2?',
										EqualState(),
										transitions={'true': 'finished', 'false': 'GetRightPartPose'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_products', 'value_b': 'part_index'})

			# x:260 y:230
			OperatableStateMachine.add('ResetPartIndex',
										ReplaceState(),
										transitions={'done': 'OrderReady?'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'reset', 'result': 'part_index'})

			# x:261 y:103
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


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
