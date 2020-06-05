#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.get_agv_status_state import GetAgvStatusState
from ariac_support_flexbe_states.equal_state import EqualState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Jun 04 2020
@author: Patrick Verwimp
'''
class CheckAGVSM(Behavior):
	'''
	Checks AGV State
	'''


	def __init__(self):
		super(CheckAGVSM, self).__init__()
		self.name = 'CheckAGV'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:541 y:178, x:142 y:179
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id'])
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.inspection_result = ''
		_state_machine.userdata.succes = 0
		_state_machine.userdata.agv_state = ''
		_state_machine.userdata.agv_ready_state = 'ready_to_deliver'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:354 y:27
			OperatableStateMachine.add('AgvState',
										GetAgvStatusState(),
										transitions={'continue': 'AGVReady', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'agv_state': 'agv_state'})

			# x:340 y:232
			OperatableStateMachine.add('AGVReady',
										EqualState(),
										transitions={'true': 'finished', 'false': 'Wait'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_state', 'value_b': 'agv_ready_state'})

			# x:266 y:130
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=0.2),
										transitions={'done': 'AgvState'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
