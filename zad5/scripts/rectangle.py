import rospy
import math
from sensor_msgs.msg import JointState
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import *

from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped
from zad5.srv import *
from zad5.msg import *

if __name__ == '__main__':

    rospy.init_node('Rectangle', anonymous=False)
    print("Ready"); 

    interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
    interpolate_one_dim( 0,0,0, 2)
    rate = rospy.Rate(0.4) # 0.5hz    
    rate.sleep()  

    rate = rospy.Rate(float(1)/6) # 10hz
    while not rospy.is_shutdown():
        interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
        interpolate_one_dim(1,0,0, 1)
        interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
        interpolate_one_dim(1,2,0, 2)
        interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
        interpolate_one_dim(0,2,0, 1)
        interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
        interpolate_one_dim(0,0,0, 2)

        rate.sleep()
        print ("Done")