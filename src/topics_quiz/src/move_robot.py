#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

rospy.init_node('topics_quiz_node')
laser = LaserScan()
vel = Twist()
vel.linear.x = vel.linear.y = vel.linear.z = 0
vel.angular.x = vel.angular.y = vel.angular.z = 0


pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

def map(val, low_in, high_in, low_op, high_op):
	return (((val-low_in)/(high_in - low_in)) * (high_op - low_op)) + low_op

def callback_laser(laser_msg):
    dist = dict(zip([int(map(x,0., 719., 0., 180.)) for x in range(720)], laser_msg.ranges))
    if dist[90] > 1.0:
        vel.linear.x = 0.2
    else:
        vel.linear.x = 0.
    
    if (dist[90] < 1.0 or dist[0] < 1.0):
        vel.angular.z = 0.2
    elif dist[0] < 1.0:
        vel.angular.z = -0.2
    else:
        vel.angular.z = 0.
    # print 'Front::' + str(dist[90]) + ' Left::' + str(dist[180]) + ' Right::' + str(dist[0])
    # print 'VelX::' + str(vel.linear.x) + ' VelZ::' + str(vel.angular.z)

    pub.publish(vel)
    

sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, callback_laser)
rospy.spin()
# while not rospy.is_shutdown():
#     pass