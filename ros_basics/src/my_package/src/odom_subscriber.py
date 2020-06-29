import rospy
from nav_msgs.msg import Odometry

rospy.init_node('Odom_Subscriber')
odom = Odometry()

def callback(msg):
    print msg.pose.pose.position.x
    print msg.pose.pose.position.y
    print msg.pose.pose.position.z
    print '------------'

sub = rospy.Subscriber('/odom', Odometry, callback)
rospy.spin()