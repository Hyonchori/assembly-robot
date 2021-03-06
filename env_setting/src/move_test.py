#!/usr/bin/env python
import sys, random, copy
import rospy, tf, rospkg, argparse, actionlib
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import *
from std_msgs.msg import *
import control_msgs.msg

from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from gazebo_ros_link_attacher.srv import Attach, AttachRequest, AttachResponse


import moveit_commander
import moveit_msgs.msg
from moveit_commander.conversions import pose_to_list


def gripper_control(close):

    # Create an action client
    client = actionlib.SimpleActionClient(
        'simul_robot1/gripper_controller/gripper_cmd',  # namespace of the action topics
        control_msgs.msg.GripperCommandAction # action type
    )
    client.wait_for_server()
    goal = control_msgs.msg.GripperCommandGoal()
    if(close == True):
        goal.command.position = 0.7   # From 0.0 to 0.8
    else:
        goal.command.position = 0.0

    goal.command.max_effort = 1.0  # Do not limit the effort
    client.send_goal(goal)
    client.wait_for_result()
    return client.get_result()


rospy.init_node("move_test")
'''

moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()

group_name1 = "arm"
group1 = moveit_commander.MoveGroupCommander(group_name1)
scene = moveit_commander.PlanningSceneInterface()
print(scene)

group1.set_named_target("ready")
plan1 = group1.plan()
group1.execute(plan1, wait=True)
'''

joint_state_topic = ['joint_states:=/simul_robot1/joint_states']
m1 = moveit_commander
m1.roscpp_initialize(joint_state_topic)
robot = m1.RobotCommander("/simul_robot1/robot_description")
group_name1 = "arm"
group1 = m1.MoveGroupCommander(group_name1,"/simul_robot1/robot_description","simul_robot1")

group1.set_named_target("ready")
plan1 = group1.plan()
group1.execute(plan1,wait=True)


gripper_control(True)

rospy.sleep(2)

joint_state_topic = ['joint_states:=/simul_robot2/joint_states']
m2 = moveit_commander
m2.roscpp_initialize(joint_state_topic)
robot = m2.RobotCommander("/simul_robot2/robot_description")
group_name2 = "arm"
group1 = m2.MoveGroupCommander(group_name2,"/simul_robot2/robot_description","simul_robot2")

group1.set_named_target("ready")
plan1 = group1.plan()
group1.execute(plan1,wait=True)