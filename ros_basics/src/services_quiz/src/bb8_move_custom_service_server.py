#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageResponse
rospy.init_node('bb8_service_server')
vel = Twist()
vel.linear.x = vel.linear.y = vel.linear.z = 0
vel.angular.x = vel.angular.y = vel.angular.z = 0

vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(10)

def turn90():
    vel.angular.z = 0.4
    vel.linear.x = 0.
    turn_time = 2.2
    start_time = time.time()
    while time.time() - start_time < turn_time:
        vel_pub.publish(vel)
        rate.sleep()



def move_straight(_time):
    vel.linear.x = 0.3
    vel.angular.z = 0.
    start_time = time.time()
    while time.time() - start_time < _time:
        vel_pub.publish(vel)
        rate.sleep()

def stop():
    vel.linear.x = 0.
    vel.angular.z = 0.
    vel_pub.publish(vel)

def move_square(side):
    for i in range(4):
        move_straight(side*2)
        # print "turning"
        rospy.sleep(1.)
        turn90()
    stop()

def service_callback(request):
    resp = BB8CustomServiceMessageResponse()
    try:
        for i in range(request.repetitions):
            move_square(request.side)
            rospy.sleep(1.5)
        resp.success = True
    except:
        resp.success = False
    return resp

server = rospy.Service('/move_bb8_in_square_custom', BB8CustomServiceMessage, service_callback)
rospy.spin()