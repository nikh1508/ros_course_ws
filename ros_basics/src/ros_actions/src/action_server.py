import rospy
import actionlib
from ros_actions.msg import DroneAction, DroneFeedback, DroneResult
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import time

class DroneClass(object):
    _feedback = DroneFeedback()
    _result = DroneResult()
    _vel = Twist()

    def __init__(self):
        self._as = actionlib.SimpleActionServer('drone_square_as', DroneAction, self.goal_callback, False)
        self._pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self._pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
        self._as.start()

    def takeoff(self):
        rospy.loginfo('Taking off...')
        msg = Empty()
        for i in range(2):
            self._pub_takeoff.publish(msg)
            rospy.sleep(1)
    
    def land(self):
        rospy.loginfo('Landing...')
        msg = Empty()
        for i in range(2):
            self._pub_land.publish(msg)
            rospy.sleep(1)

    def stop_drone(self):
        self._vel.angular.x = self._vel.angular.y = self._vel.angular.z = 0.
        self._vel.linear.x = self._vel.linear.y = self._vel.linear.z = 0.
        for i in range(4):
            self._pub_vel.publish(self._vel)
            rospy.sleep(.25)
    
    def move(self, comp, speed, _time):
        self._vel.linear.x = comp[0] * speed; self._vel.linear.y = comp[1] * speed; self._vel.linear.z = comp[2] * speed;
        self._vel.angular.x = 0; self._vel.angular.y = 0; self._vel.angular.z = comp[3] * speed;
        rate = rospy.Rate(10)
        start_time = time.time()
        while True:
            if time.time() - start_time > _time:
                break
            self._pub_vel.publish(self._vel)
            rate.sleep()

    def goal_callback(self, goal):
        side_length = goal.goal
        success = True
        _dir = {
            'fwd':(1, 0, 0, 0),
            'bkd':(-1, 0, 0, 0),
            'left':(0, -1, 0, 0),
            'right':(0, 1, 1, 0)
            }
        path = ('fwd', 'right', 'bkd', 'left')
        
        start_time = time.time()
        self.takeoff()
        for i in range(4):
            if self._as.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                self._as.set_preempted()
                success = False
                break
            
            self._feedback.feedback = i+1
            self._as.publish_feedback(self._feedback)
            self.move(_dir[path[i]], 0.5, side_length)
            self.stop_drone()
        self.land()
        if success:
            rospy.loginfo('Action completed successfully.')
            self._result.result = time.time() - start_time
            self._as.set_succeeded(self._result)
    
if __name__ == '__main__':
    rospy.init_node('drone_move_square')
    rospy.loginfo('Action server started...')
    DroneClass()
    rospy.spin()