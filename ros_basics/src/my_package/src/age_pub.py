import rospy
from my_package.msg import Age

rospy.init_node('age')
age = Age()
pub = rospy.Publisher('/age', Age, queue_size=1)
rate = rospy.Rate(1)

age.years = 5.0
age.months = 6.0
age.days = 12.3

while not rospy.is_shutdown():
    pub.publish(age)
    rate.sleep()