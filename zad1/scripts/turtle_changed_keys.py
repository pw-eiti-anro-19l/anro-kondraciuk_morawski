#!/usr/bin/env python
import click
import rospy
from geometry_msgs.msg import Twist 
rospy.init_node('turtle_changed_keys', anonymous=True)
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

forward = rospy.get_param("turtle_changed_keys/forward")
back = rospy.get_param("turtle_changed_keys/back")
turn_left = rospy.get_param("turtle_changed_keys/turn_left")
turn_right = rospy.get_param("turtle_changed_keys/turn_right")


while not rospy.is_shutdown():

    msg = Twist()
    key = click.getchar()
    if key == forward:
        msg.linear.x = 1
    elif key == turn_left:
        msg.angular.z = 1
    elif key == back:
        msg.linear.x = -1
    elif key == turn_right:
        msg.angular.z = -1
    pub.publish(msg)
