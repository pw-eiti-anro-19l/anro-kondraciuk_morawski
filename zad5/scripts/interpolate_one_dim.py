#!/usr/bin/env python

from zad5.srv import *
from zad5.msg import *
import rospy

def handle_interpolate_one_dim(req):
    #print "Returning [%s + %s +%s = %s]"%(req.a, req.b, req.c, (req.a + req.b+req.c))
	pub = rospy.Publisher('order', InterpolAtrrib, queue_size=10)
	inter = InterpolAtrrib()
	inter.x=req.x
	inter.y=req.y
	inter.z=req.z
	inter.time=req.time
	pub.publish(inter)
	return InterpolationResponse()

def interpolate_one_dim_server():
    rospy.init_node('interpolate_one_dim_server')
    s = rospy.Service('interpolate_one_dim', Interpolation, handle_interpolate_one_dim)
    print "Ready."
    rospy.spin()

if __name__ == "__main__":
    interpolate_one_dim_server()
