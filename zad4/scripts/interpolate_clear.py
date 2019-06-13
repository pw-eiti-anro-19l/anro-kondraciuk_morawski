#!/usr/bin/env python

from zad5.srv import *
from zad5.msg import *
import rospy

def handle_interpolate_clear(req):
    pub = rospy.Publisher('clearOrder', clearmsg, queue_size=10)
    inter = clearmsg()
    pub.publish(inter)
    return clearResponse()

def interpolate_clear_server():
    rospy.init_node('interpolate_clear_server')
    s = rospy.Service('interpolate_clear', clear, handle_interpolate_clear)
    print "Ready to clear."
    rospy.spin()

if __name__ == "__main__":
    interpolate_clear_server()
