#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_behaviors.waitstate_sm import WaitstateSM
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.gripper_control import GripperControl
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 03 2020
@author: Wouter Lax
'''
class Pick_Blue_PartSM(Behavior):
	'''
	Program to pick the blue parts from the belt
[Version 1]
	'''


	def __init__(self):
		super(Pick_Blue_PartSM, self).__init__()
		self.name = 'Pick_Blue_Part'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(WaitstateSM, 'Waitstate')
		self.add_behavior(WaitstateSM, 'Waitstate_2')
		self.add_behavior(WaitstateSM, 'Waitstate_3')
		self.add_behavior(WaitstateSM, 'Waitstate_5')
		self.add_behavior(WaitstateSM, 'Waitstate_6')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:

		# O 52 206 
		# Arm1 above belt

		# O 236 18 
		# Beweging naar part berekenen

		# O 460 24 
		# Bewegen naar part

		# O 672 32 
		# Grpper aan

		# O 836 28 
		# Terug naar pregrasp

		# O 1038 26 
		# Terug naar home

		# O 30 26 
		# Check current location part



	def create(self):
		# x:1230 y:65, x:642 y:465
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.move_group = ''
		_state_machine.userdata.move_group_prefix = '/ariac/gantry'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.arm_id = 'Left_Arm'
		_state_machine.userdata.tool_link = 'left_ee_link'
		_state_machine.userdata.pose = []
		_state_machine.userdata.offset = 0.020
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.camera_topic = '/ariac/logical_camera_belt'
		_state_machine.userdata.camera_frame = 'logical_camera_belt_frame'
		_state_machine.userdata.home = 'Gantry_Home'
		_state_machine.userdata.part = 'piston_rod_part_red'
		_state_machine.userdata.belt = 'Gantry_Belt_Left'
		_state_machine.userdata.bin = 'Gantry_Bin_Blue'
		_state_machine.userdata.full_home = 'Full_Home'
		_state_machine.userdata.clearance = 0.1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:29 y:50
			OperatableStateMachine.add('Detect_Blue_Part',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'Move_Belt', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:234 y:142
			OperatableStateMachine.add('Waitstate',
										self.use_behavior(WaitstateSM, 'Waitstate'),
										transitions={'finished': 'Move_Belt', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:240 y:46
			OperatableStateMachine.add('Compute_Pick',
										ComputeGraspAriacState(),
										transitions={'continue': 'Move_to_Pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:454 y:50
			OperatableStateMachine.add('Move_to_Pick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Gripper_On', 'planning_failed': 'Waitstate_2', 'control_failed': 'Gripper_On'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:453 y:144
			OperatableStateMachine.add('Waitstate_2',
										self.use_behavior(WaitstateSM, 'Waitstate_2'),
										transitions={'finished': 'Move_to_Pick', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:671 y:56
			OperatableStateMachine.add('Gripper_On',
										GripperControl(enable=True),
										transitions={'continue': 'Move_Belt_2', 'failed': 'failed', 'invalid_id': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_id': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:838 y:52
			OperatableStateMachine.add('Move_Belt_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Add_Clearance', 'planning_failed': 'Waitstate_3', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'belt', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:823 y:142
			OperatableStateMachine.add('Waitstate_3',
										self.use_behavior(WaitstateSM, 'Waitstate_3'),
										transitions={'finished': 'Move_Belt_2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:50 y:152
			OperatableStateMachine.add('Move_Belt',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Compute_Pick', 'planning_failed': 'Waitstate', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'belt', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1046 y:358
			OperatableStateMachine.add('Left_Arm_Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Waitstate_5', 'control_failed': 'Left_Arm_Home', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'full_home', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1047 y:436
			OperatableStateMachine.add('Waitstate_5',
										self.use_behavior(WaitstateSM, 'Waitstate_5'),
										transitions={'finished': 'Left_Arm_Home', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1041 y:144
			OperatableStateMachine.add('Compute_Grasp',
										ComputeGraspAriacState(),
										transitions={'continue': 'Move_Clearance', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'arm_id', 'move_group_prefix': 'move_group_prefix', 'pose': 'pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1013 y:50
			OperatableStateMachine.add('Add_Clearance',
										AddNumericState(),
										transitions={'done': 'Compute_Grasp'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'clearance', 'value_b': 'offset', 'result': 'offset'})

			# x:1039 y:226
			OperatableStateMachine.add('Move_Clearance',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Left_Arm_Home', 'planning_failed': 'Waitstate_6', 'control_failed': 'Move_Clearance'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'arm_id', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:821 y:270
			OperatableStateMachine.add('Waitstate_6',
										self.use_behavior(WaitstateSM, 'Waitstate_6'),
										transitions={'finished': 'Move_Clearance', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
