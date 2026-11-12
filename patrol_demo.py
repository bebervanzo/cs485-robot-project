# heavily inspired by a simple_commander demo in the nav2 repository

from copy import deepcopy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.duration import Duration

def main():
	rclpy.init()
	nav = BasicNavigator()

	# list of waypoints. eventually read from file but this is just a demo
	# question: what is the range of values that the waypoints should fall within?
	# TODO: add more waypoints lmao
	waypoints = [
	[1.000, 1.000],
	[-1.000, -1.000],
	[-1.000, 1.000],
	[1.000, -1.000]
	]

	initial_pose = PoseStamped()
    nav.setInitialPose(initial_pose)

    nav.waitUntilNav2Active()

    # loop until you can't
    while rclpy.ok():
    	route_poses = []
    	pose = PoseStamped()
    	for wp in waypoints:
    		pose.pose.position.x = wp[0]
    		pose.pose.position.y = wp[1]
    		route_poses.append(deepcopy(pose))
    	nav.goThroughPoses(route_poses)

    	# once goThroughPoses() finishes, check status
    	result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print('Route complete! Restarting...')
        elif result == TaskResult.CANCELED:
            print('Security route was canceled, exiting.')
            exit(1)
        elif result == TaskResult.FAILED:
            print('Security route failed! Restarting from other side...')

        # and now go back to the first waypoint and repeat ad nauseam
    exit(0)


main()