# README.md

This is a placeholder! Wow!

tiago launcher:
find ~/tiago_public_ws/src -path '*/tiago_description/launch/robot_state_publisher.launch.py'
replace with the versionof that file in the repo
rebuild
source with:
source /opt/ros/humble/setup.bash &&
source "$HOME/tiago_public_ws/install/setup.bash"

(ensure office_small.world is in the folder)
launch with (assumes you are in the right folder and world is in same folder):
ros2 launch multi_tiago_launcher.py
