#! /usr/bin/env python

import rospy
from std_srvs.srv import Empty, EmptyRequest
rospy.init_node('move_bb8_client')
rospy.wait_for_service('/move_bb8_in_circle')
service_proxy = rospy.ServiceProxy('/move_bb8_in_circle', Empty)

emp_req = EmptyRequest()
res = service_proxy(emp_req)