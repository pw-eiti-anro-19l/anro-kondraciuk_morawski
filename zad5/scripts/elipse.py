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

    speed=0.05
    rospy.init_node('Circle', anonymous=False)
    print("Ready"); 
    i=0
    angle = float(i*4*math.pi)/180
    interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
    interpolate_one_dim((math.cos(angle)+1)/2+(math.sin(angle)+1)/6,(math.sin(angle)+1)/2+(math.cos(angle)+1)/10,0, 2)
    rate = rospy.Rate(0.5) # 0.5hz    
    rate.sleep()  

    rate = rospy.Rate(1/(speed*130)) # 10hz
    while not rospy.is_shutdown():
        for i in range(90):
            rospy.wait_for_service('interpolate_one_dim')
            angle = float(i*4*math.pi)/180
            try:
                interpolate_one_dim = rospy.ServiceProxy('interpolate_one_dim', Interpolation)
                interpolate_one_dim((math.cos(angle)+1)/2+(math.sin(angle)+1)/6,(math.sin(angle)+1)/2+(math.cos(angle)+1)/10,0, speed)
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
        rate.sleep()
        print ("Done")