#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from ros_service.srv import MyCustomServiceMessage, MyCustomServiceMessageResponse  # you import the service message python classes generated from Empty.srv.
import time

rospy.init_node('bb8_move_server')
vel = Twist()
vel.linear.x = vel.linear.y = vel.linear.z = 0
vel.angular.x = vel.angular.y = vel.angular.z = 0
vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

def service_callback(request):
    res = MyCustomServiceMessageResponse()
    print "New request received"
    
    try:
        vel.linear.x = vel.angular.z = 0.4
        vel_pub.publish(vel)
        rospy.sleep(request.duration)
        vel.linear.x = vel.angular.z = 0.
        vel_pub.publish(vel)
        res.success = True
    except:
        res.success = False
    return res
    
my_service = rospy.Service('/move_bb8_in_circle', MyCustomServiceMessage , service_callback) # create the Service called my_service with the defined callback
rospy.spin()