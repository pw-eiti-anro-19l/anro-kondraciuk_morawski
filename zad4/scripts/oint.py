#! /usr/bin/python

import json
import rospy
import PyKDL
import os
from sensor_msgs.msg import JointState
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import *

from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped
from zad4.srv import *
from zad4.msg import *

def interpolate_one_dim(x1, x2, startTime, time):
    currT = rospy.get_rostime().secs+0.000000001*rospy.get_rostime().nsecs 
    if currT>(startTime+time):
        return x2
    resp1 = x1+(x2-x1)/time*(currT-startTime)
    return resp1
x1=0
y1=0
z1=0
x2=0
y2=0
z2=0
time=0
id=0
markerArray=MarkerArray()
def callback(data):
    global x1, x2, y1, y2, z1, z2, time, id, markerArray

    rate = rospy.Rate(40)
    startTime = rospy.get_rostime().secs+0.000000001*rospy.get_rostime().nsecs
    x1=x2
    y1=y2
    z1=z2
    x2=data.x
    y2= data.y
    z2=data.z
    time =data.time

    signx = 1
    signy =1 
    signz =1
    currT = rospy.get_rostime().secs+0.000000001*rospy.get_rostime().nsecs 
    while not currT>(startTime+time):
    	currT = rospy.get_rostime().secs+0.000000001*rospy.get_rostime().nsecs 
        x=interpolate_one_dim(x1,x2,startTime, time)
        y=interpolate_one_dim(y1,y2,startTime, time)
        z=interpolate_one_dim(z1,z2,startTime, time)
       # print(x, " ", y, " ", z)
        pose = PoseStamped()
        pose.header.frame_id = 'base_link'
        pose.header.stamp = rospy.Time.now()

        pose.pose.position.x = x 
        pose.pose.position.y = -y 
        pose.pose.position.z = z 
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.5
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = x 
        marker.pose.position.y = -y 
        marker.pose.position.z = z 
        marker.id = id
        id+=1
        markerArray.markers.append(marker)
        pub2.publish(markerArray)
        rate.sleep()
        pub.publish(pose)

    #rate.sleep()

def clearCallback(data):
    global id, markerArray
    
    markerArray=MarkerArray()
    marker = Marker()
    marker.action = marker.DELETEALL
    marker.id = 0
    markerArray.markers.append(marker)
    pub2.publish(markerArray)

    markerArray=MarkerArray()
    id=0

if __name__ == '__main__':

    rospy.init_node('OINT', anonymous=False)
    pub2 = rospy.Publisher('robo', MarkerArray, queue_size=20)
    pub = rospy.Publisher('Axes', PoseStamped, queue_size=10)
    
    rospy.Subscriber("clearOrder", clearmsg , clearCallback)
    rospy.Subscriber("order", InterpolAtrrib , callback)
    print("Ready"); 
    
    rospy.spin()

