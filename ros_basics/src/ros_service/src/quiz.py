#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion

rospy.init_node('rotate_bb8')

vel = Twist()
vel.linear.x = vel.linear.y = vel.linear.z = 0
vel.angular.x = vel.angular.y = vel.angular.z = 0

vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
rate = rospy.Rate(10)

roll = pitch = yaw = 0.0

def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

sub = rospy.Subscriber ('/odom', Odometry, get_rotation)

rad2deg = lambda x : 57.29577951308232 * x
def get_yaw():
    _yaw = rad2deg(yaw)
    _yaw += 0 if _yaw > 0 else 360.
    return _yaw

def angle_diff(_inp, _set):
    tmp = abs(_inp - _set)
    diff = min(tmp, abs(360 - tmp))
    if (_set + diff) != _inp and (_set - diff) != _inp:
        if (_inp + diff) >= 360.:
            return -diff
        else:
            return diff
    else:
        return (_inp - _set)

def turn(deg):
    angle_to_achieve = (get_yaw() + deg)
    angle_to_achieve -= 360. if angle_to_achieve > 360. else 0.
    vel.linear.x = 0
    vel.angular.z =0.4
    rate = rospy.Rate(5)
    print "Target::" + str(angle_to_achieve)
    rospy.sleep(.5)
    while not rospy.is_shutdown() and abs(angle_diff(get_yaw(), angle_to_achieve)) > 0.5:
        vel_pub.publish(vel)
        print "yaw_now::"+ str(get_yaw())
        rate.sleep()
    vel.angular.z = 0
    vel_pub.publish(vel)


# while not rospy.is_shutdown():
#     vel.angular.z = 0.4
#     vel_pub.publish(vel)
#     print "YAW:: " + str(get_yaw())
#     rate.sleep()

print "YAW1:: " + str(get_yaw())
rospy.sleep(2.)
print "YAW1:: " + str(get_yaw())
turn(90)
print "YAW2:: " + str(get_yaw())
rospy.sleep(2.)
turn(180)
print "YAW1:: " + str(get_yaw())