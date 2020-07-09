#! /usr/bin/env python

import rospy
from std_msgs.msg import Float64

rospy.init_node('custom_controller')

position = Float64()
position.data = -0.785398

pub = rospy.Publisher('/ur5/shoulder_lift_joint_position_controller/command', Float64, queue_size=1)
while pub.get_num_connections() < 1:
    pass

pub.publish(position)
rospy.spin()