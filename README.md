# README.md

This is a placeholder! Wow!

tiago launcher:
find ~/tiago_public_ws/src -path '*/tiago_description/launch/robot_state_publisher.launch.py'
replace with the version of that file in the repo
rebuild
launch the file with exactly this:
env -i HOME="$HOME" USER="$USER" PATH=/usr/bin:/bin:/usr/sbin:/sbin DISPLAY="$DISPLAY" XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}" bash --noprofile --norc -c '
source /opt/ros/humble/setup.bash &&
source "$HOME/tiago_public_ws/install/setup.bash" &&
ros2 launch "$HOME/tiago_public_ws/multi_tiago.launch.py"
'
