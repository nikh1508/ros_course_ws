#! /usr/bin/env python

import rospy
import actionlib
from actions_quiz.msg import CustomActionMsgAction, CustomActionMsgFeedback, CustomActionMsgResult
from std_msgs.msg import Empty

class CustomActionClass(object):
    _feedback = CustomActionMsgFeedback()
    _result = CustomActionMsgResult()
    _empty_msg = Empty()

    def __init__(self):
        self._as = actionlib.SimpleActionServer('action_custom_msg_as', CustomActionMsgAction, self.goal_callback, False)
        self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
        self._as.start()
    
    def goal_callback(self, goal):
        action = goal.goal
        success = True
        r = rospy.Rate(1)

        if action == 'TAKEOFF':
            self._feedback.feedback = 'TAKING OFF'
            for i in range(3):
                self._pub_takeoff.publish(self._empty_msg)
                self._as.publish_feedback(self._feedback)
                r.sleep()
        elif action == 'LAND':
            self._feedback.feedback = 'LANDING'
            for i in range(3):
                self._pub_land.publish(self._empty_msg)
                self._as.publish_feedback(self._feedback)
                r.sleep()
        else:
            success = False
        
        if success:
            self._as.set_succeeded()

if __name__ == '__main__':
    rospy.init_node('action_custom_node')
    CustomActionClass()
    rospy.loginfo('Action Server started...')
    rospy.spin()