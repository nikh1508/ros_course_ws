#! /usr/bin/env python

import rospy                               # Import the Python library for ROS
from geometry_msgs.msg import Twist

rospy.init_node('robot_controller')         # Initiate a Node named 'topic_publisher'
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)    
                                           # Create a Publisher object, that will publish on the /counter topic
                                           # messages of type Int32

# rate = rospy.Rate(5)                       # Set a publish rate of 2 Hz
vel = Twist()
vel.linear.x = vel.linear.y = vel.linear.z = 0
vel.angular.x = vel.angular.y = vel.angular.z = 0


ctr = 0
while not rospy.is_shutdown():             # Create a loop that will go until someone stops the program execution
    # vel.angular.z = 0.4 if ctr%2==0 else -0.4
    vel.angular.z = 0.4
    vel.linear.x = 0.5
    pub.publish(vel)    
    ctr += 1
    rospy.sleep(5)

vel.linear.x = 0.
pub.publish(vel) 