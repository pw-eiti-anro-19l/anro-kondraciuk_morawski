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


def callback(data):

    x = -data.pose.position.x
    y = data.pose.position.y
    z = data.pose.position.z

    wektor = concatenate_matrices(inverse_matrix(TransMatrix[0]),(x,y,z,1))
    a=wektor[2]
    wektor = concatenate_matrices(inverse_matrix(TransMatrix[1]),wektor)
    b=wektor[1]
    wektor = concatenate_matrices(inverse_matrix(TransMatrix[2]),wektor)
    c=wektor[0]
    positi = JointState()
    positi.name = ["base_to_link1", "link1_to_link2", "link2_to_link3"]
    positi.position=[a+1,c+1,b]
    positi.header.stamp= rospy.get_rostime()
    pub.publish(positi)

TransMatrix= []
if __name__ == '__main__':

    rospy.init_node('IKIN', anonymous=False)
    pub=rospy.Publisher("joint_states", JointState , queue_size=10)
    rospy.Subscriber("Axes", PoseStamped , callback)
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh_data.json', 'r') as file:
        dhJson= json.loads(file.read())
    T = translation_matrix((0, 0, 0));

    TransMatrix.append(translation_matrix((0, 0, 0)))
    TransMatrix.append(translation_matrix((0, 0, 0)))
    TransMatrix.append(translation_matrix((0, 0, 0)))
    i=0
    for instance in dhJson:
        oneInstance= json.loads(json.dumps(instance))
        a = oneInstance["a"]
        d = oneInstance["d"]
        alpha=oneInstance["alpha"]
        theta = oneInstance["theta"]
        xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)
        matrixD= translation_matrix((0, 0, d))
        matrixTheta = rotation_matrix(theta, zaxis)
        matrixA = translation_matrix((a, 0, 0))
        matrixAlpha = rotation_matrix(alpha, xaxis)

        TransMatrix[i] = concatenate_matrices(matrixA,matrixAlpha,matrixTheta, matrixD)
        T=concatenate_matrices(T, TransMatrix[i])
        
        i+=1;
    print("Ready"); 
    
   
  

    
    rospy.spin()
