#! /usr/bin/env python

import rospy
import rospkg
from iri_wam_reproduce_trajectory.srv import ExecTraj, ExecTrajRequest

rospack = rospkg.RosPack()
rospy.init_node('manipulator_control')
rospy.wait_for_service('/execute_trajectory')

srv_proxy = rospy.ServiceProxy('/execute_trajectory', ExecTraj)
traj = ExecTrajRequest()
def get_path(pos):
    return rospack.get_path('iri_wam_reproduce_trajectory')+'/config/' + pos + '.txt'
traj.file = get_path('get_food')
# print traj
print "Getting Food"
res = srv_proxy(traj)
print "Releasing Food"
traj.file = get_path('release_food')
res = srv_proxy(traj)