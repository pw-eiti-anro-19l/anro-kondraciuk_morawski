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
from zad5.srv import *
from zad5.msg import *

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
def callback(data):
    global x1, x2, y1, y2, z1, z2, time, id


    rate = rospy.Rate(40) # 10hz
    startTime = rospy.get_rostime().secs+0.000000001*rospy.get_rostime().nsecs
    x1=x2
    y1=y2
    z1=z2
    x2=data.x
    y2= data.y
    z2=data.z
    time =data.time
    
    currT = rospy.get_rostime().secs+0.000000001*rospy.get_rostime().nsecs 
    while not currT>(startTime+time):
    	currT = rospy.get_rostime().secs+0.000000001*rospy.get_rostime().nsecs 
        print ("he")
        x=interpolate_one_dim(x1,x2,startTime, time)
        y=interpolate_one_dim(y1,y2,startTime, time)
        z=interpolate_one_dim(z1,z2,startTime, time)
       # print(x, " ", y, " ", z)
        positi = JointState()
        positi.name = ["base_to_link1", "link1_to_link2", "link2_to_link3"]
        positi.position=[y, x ,z]
        
        marker = Marker()
        marker.header.frame_id = "base_link"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.5
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = z
        marker.pose.position.y = -x
        marker.pose.position.z = y
        marker.id = id
        markerArray.markers.append(marker)
        
        
        id += 1
        pub2.publish(markerArray)
        positi.header.stamp= rospy.get_rostime()
        
        pub.publish(positi)
        rate.sleep()


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

    rospy.init_node('JINT', anonymous=False)
    pub2 = rospy.Publisher('robo', MarkerArray, queue_size=20)
    pub=rospy.Publisher("joint_states", JointState , queue_size=10)
        
    rospy.Subscriber("clearOrder", clearmsg , clearCallback)
    rospy.Subscriber("order", InterpolAtrrib , callback)
    print("Ready"); 
  
   
    rospy.spin()
