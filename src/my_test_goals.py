#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseResult
import numpy as np

rospy.init_node('nav')


def goal_point(point):
    goals = MoveBaseGoal()
    goals.target_pose.header.frame_id = 'odom'
    goals.target_pose.pose.position.x = point[0]
    goals.target_pose.pose.position.y = point[1]
    goals.target_pose.pose.position.z = 0
    goals.target_pose.pose.orientation.x = 0
    goals.target_pose.pose.orientation.y = 0
    goals.target_pose.pose.orientation.z = 0
    goals.target_pose.pose.orientation.w = 1
    return goals

client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()

#we need to sort goals before we send to move_base  
#goal_position = [[-0.57, 1.06],[-0.399, 0.399],[1.652, -0.635],[0.7444, 0.444]]
#mujib goal_position = [[0.7166, 0.4659],[1.6470, 1.57328],[0.13643, 1.87091],[-0.95811, -1.08635]]

#random goals for testing

goal_position = [[1.130908, 0.37930],[2.30643, 1.295715],[0.780431, 2.0228958],[-0.5595047, -1.04665052],[-0.25635, -2.225545],[0.6310444, -1.085432]]

for i in range(len(goal_position)): 
    while not rospy.is_shutdown():
        goal = goal_point(goal_position[i])
        client.send_goal(goal)
        client.wait_for_result()
        if client.get_state() == 3:
	    print("goal %d reached", i)
            break
