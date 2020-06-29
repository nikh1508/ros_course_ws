import rospy
from std_msgs.msg import Int32

rospy.init_node('counter_publisher')
pub = rospy.Publisher('/counter', Int32, queue_size=1)
rate = rospy.Rate(1)

var = Int32()
var.data = 0

while not rospy.is_shutdown():
    pub.publish(var)
    var.data += 1
    rate.sleep()