#! /usr/bin/env python

import rospy
from services_quiz.srv import BB8CustomServiceMessage, BB8CustomServiceMessageRequest
rospy.init_node('bb8_service_client')
rospy.wait_for_service('/move_bb8_in_square_custom')
service_proxy = rospy.ServiceProxy('/move_bb8_in_square_custom', BB8CustomServiceMessage)

req = BB8CustomServiceMessageRequest()

req.side = 1
req.repetitions = 2
res = service_proxy(req)

req.side = 1.5
req.repetitions = 1
res = service_proxy(req)