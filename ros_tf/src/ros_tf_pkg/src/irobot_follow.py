import sys
import rospy
from geometry_msgs.msg import Twist
import tf
import math

rospy.init_node('irobot_follow')
tf_listener = tf.TransformListener()

if(len(sys.argv) < 2):
    print "Usage: rosrun ros_pkg_tf irobot_follow.py {model_to_follow}"
else:
    model_to_follow = sys.argv[1]

irobot_vel = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    try:
        (trans,rot) = tf_listener.lookupTransform('turtle2', model_to_follow, rospy.Time(0))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        continue

    angular = 4 * math.atan2(trans[1], trans[0])
    linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
    cmd = Twist()
    cmd.linear.x = linear
    cmd.angular.z = angular
    irobot_vel.publish(cmd)  

    rate.sleep()