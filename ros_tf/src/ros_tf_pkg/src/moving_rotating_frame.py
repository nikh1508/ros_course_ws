#!/usr/bin/env python

import rospy
import math
import tf

rospy.init_node('moving_and_rotating_frame')
br = tf.TransformBroadcaster()
rate = rospy.Rate(10)
rotation_speed = 0.1    # rad/sec
revolution_speed = 0.1  # rad/sec
radius = 1.0
while not rospy.is_shutdown():
    time_now = rospy.Time.now().to_sec()
    _x = math.sin(time_now * rotation_speed) * radius
    _y = math.cos(time_now * rotation_speed) * radius
    _yaw = (time_now % (2 * math.pi)) - math.pi
    _yaw *= -1.0
    quaternion = tf.transformations.quaternion_from_euler(0.0,0.0,_yaw)
    # print quaternion
    br.sendTransform((_x, _y, 0), 
                    quaternion, 
                    rospy.Time.now(), 
                    'moving_nd_rotating', 
                    'coke_can')
    rate.sleep()