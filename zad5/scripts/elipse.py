#! /usr/bin/python

import rospy
import math
from sensor_msgs.msg import JointState
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import *

import PyKDL

from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped
from zad5.srv import *
from zad5.msg import *

if __name__ == '__main__':

    speed=0.05
    rospy.init_node('Circle', anonymous=False)
#    i=0
#    angle = float(i*4*math.pi)/180
#    interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
#    interpolate_one_dim((math.cos(angle)+1)/2+(math.sin(angle)+1)/6,(math.sin(angle)+1)/2+(math.cos(angle)+1)/10,0, 2)
#    rate = rospy.Rate(0.5) # 0.5hz    
#    rate.sleep()  

    for i in range(10):
        try:
            rospy.wait_for_service('interpolate_one_dim')
            interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
            break
        except:
            rospy.sleep(0.5)
    print("Ready"); 

    # ellispe transform 
    tr = PyKDL.Frame( PyKDL.Rotation.RotX(math.pi/6)*PyKDL.Rotation.RotY(math.pi/4), PyKDL.Vector(0.5,-0.5,0.5) )

    rx = 0.6
    ry = 0.3
    rate = rospy.Rate(1/(speed*130))
    while not rospy.is_shutdown():
        for i in range(90):
            angle = float(i*4*math.pi)/180
            #pt = tr*PyKDL.Vector( (math.cos(angle)+1)/2+(math.sin(angle)+1)/6,(math.sin(angle)+1)/2+(math.cos(angle)+1)/10,0 )
            pt = tr*PyKDL.Vector( math.cos(angle)*rx, math.sin(angle)*ry,0 )
            interpolate_one_dim(pt.x(), pt.y(), pt.z(), speed)
        rate.sleep()
        print ("Done")

