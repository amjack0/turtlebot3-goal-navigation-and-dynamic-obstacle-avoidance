#!/usr/bin/env python

import rospy
from goal_publisher.msg import PointArray
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseResult
from nav_msgs.srv import GetPlan, GetPlanRequest, GetPlanResponse
import time
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import numpy as np
from operator import itemgetter

rospy.init_node('goal_navigation')
reach = list()
pos_goal = list()
pos_curr = PoseWithCovarianceStamped()

"""
Getting current position.
"""


def amcl_mycallback(msg):
    global pos_curr
    pos_curr = msg


"""Sorting goal positions in descending order. Note that, by changing the reverse = false , goals can be sorted 
in ascending order. """


def goal_sorting(point):
    b = sorted(point, key=itemgetter(2), reverse=True)
    b[0], b[len(b) - 1] = b[len(b) - 1], b[0]
    return b


"""move base goals"""


def goal_point(point):
    goals = MoveBaseGoal()

    # goals.target_pose.header.frame_id = 'odom'
    goals.target_pose.header.frame_id = 'map'
    goals.target_pose.pose.position.x = point[0]
    goals.target_pose.pose.position.y = point[1]
    goals.target_pose.pose.position.z = 0
    goals.target_pose.pose.orientation.x = 0
    goals.target_pose.pose.orientation.y = 0
    goals.target_pose.pose.orientation.z = 0
    goals.target_pose.pose.orientation.w = 1
    return goals


"""
Reading the goal parameters and storing it in a global variable.
"""


def goal_mycallback(self):
    global pos_goal

    pos_goal = [[self.goals[0].x, self.goals[0].y, self.goals[0].reward],
                [self.goals[1].x, self.goals[1].y, self.goals[1].reward],
                [self.goals[2].x, self.goals[2].y, self.goals[2].reward],
                [self.goals[3].x, self.goals[3].y, self.goals[3].reward],
                [self.goals[4].x, self.goals[4].y, self.goals[4].reward],
                [self.goals[5].x, self.goals[5].y, self.goals[5].reward],
                [self.goals[6].x, self.goals[6].y, self.goals[6].reward]]


def get_length(start_point, end_point):
    rospy.wait_for_service('/move_base/make_plan')
    srv_proxy = rospy.ServiceProxy('/move_base/make_plan', GetPlan)
    srv_request = GetPlanRequest()
    point_stamp1, point_stamp2 = PoseStamped(), PoseStamped()
    point_stamp1.header.frame_id, point_stamp2.header.frame_id = 'map', 'map'
    point_stamp1.pose.position.x, point_stamp1.pose.position.y = start_point[0], start_point[1]
    point_stamp2.pose.position.x, point_stamp2.pose.position.y = end_point[0], end_point[1]
    srv_request.start = point_stamp1
    srv_request.goal = point_stamp2
    srv_response = srv_proxy(srv_request)
    goal_dist = 0

    # for i in range(0, len(srv_response.plan.poses)):
    for i in range(len(srv_response.plan.poses) - 1):
        position_a_X = srv_response.plan.poses[i].pose.position.x
        position_a_Y = srv_response.plan.poses[i].pose.position.y
        position_b_X = srv_response.plan.poses[i + 1].pose.position.x
        position_b_y = srv_response.plan.poses[i + 1].pose.position.y

        goal_dist += np.sqrt(np.power((position_b_X - position_a_X), 2) + np.power((position_b_y - position_a_Y), 2))
    return goal_dist


""" Subscribing to /goals topic and amcl_pose """

rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, amcl_mycallback)
rospy.Subscriber('goals', PointArray, goal_mycallback)
client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
client.wait_for_server()
time.sleep(2)
goals_sorted = goal_sorting(pos_goal)

for goal_no in range(len(goals_sorted)):
    if goal_no <= 3:
        for l in range(4 - goal_no):
            reach.append(
                get_length([pos_curr.pose.pose.position.x, pos_curr.pose.pose.position.y], goals_sorted[goal_no + l]))
        index_min = reach.index(min(filter(lambda i: i > 0, reach)))
        print(reach, index_min)
        goal = goal_point(goals_sorted[goal_no + index_min])
    else:
        goal = goal_point(goals_sorted[goal_no])
    while not rospy.is_shutdown():
        client.send_goal(goal)
        client.wait_for_result()
        if client.get_state() == 3:
            if goal_no <= 3:
                goals_sorted[goal_no], goals_sorted[goal_no + reach.index(min(reach))] = goals_sorted[
                                                                                             goal_no + reach.index(
                                                                                                 min(reach))], \
                                                                                         goals_sorted[goal_no]
                reach = []
                print(goals_sorted)
            print("goal %d reached", goal_no)
            break
