#! /usr/bin/env python

import rospy
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneResult, ArdroneFeedback
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
import time

rospy.init_node('ardrone_action_client')
action_server_name = '/ardrone_action_server'
client = actionlib.SimpleActionClient(action_server_name, ArdroneAction)

# waits until the action server is up and running
rospy.loginfo('Waiting for action Server '+action_server_name)
client.wait_for_server()
rospy.loginfo('Action Server Found...'+action_server_name)
vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

vel = Twist()
vel.linear.x = vel.linear.y = vel.linear.z = 0.
vel.angular.x = vel.angular.y = vel.angular.z = 0. 

nImage = 1
def feedback_cb(feedback):
    global nImage
    print 'Received Image::'+str(nImage)
    nImage += 1

PENDING = 0
ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

goal = ArdroneGoal()
goal.nseconds = 10

### TakeOff
# take_off = rospy.Publisher('/drone/takeoff', Empty)
# empty_msg = Empty()
# take_off.publish(empty_msg)
# print "Drone Taking Off..."
# rospy.sleep(1.5)
###

flag = {'y_axis': True, 'pos': True}
rate = rospy.Rate(10)
step_time = 2.0
speed = 0.5

client.send_goal(goal, feedback_cb = feedback_cb)

print "Entering the loop and waiting for result"
last_time = time.time() - step_time
while client.get_state() < DONE:
    if time.time() - last_time > step_time:
        if flag['y_axis']:
            vel.linear.x = 0
            vel.linear.y = speed if flag['pos'] else -speed
        else:
            vel.linear.y = 0
            vel.linear.x = speed if flag['pos'] else -speed
            flag['pos'] = not flag['pos']
        flag['y_axis'] = not flag['y_axis']
        last_time = time.time()
    vel_pub.publish(vel)
    # print client.get_state()
    rate.sleep()

vel.angular.x = vel.angular.y = 0
vel_pub.publish(vel)
print 'Action Completed'
print 'State::'+str(client.get_state())