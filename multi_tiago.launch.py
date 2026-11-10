import os
from pathlib import Path

from ament_index_python.packages import get_package_prefix, get_package_share_directory
from launch import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node, PushRosNamespace, SetRemap


def include(package, filename, args):
    path = Path(get_package_share_directory(package)) / 'launch' / filename
    return IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(path)), launch_arguments=args.items())


def robot(name, x, y, nav_params):
    bringup = GroupAction([
        PushRosNamespace(name),
        SetRemap('/tf', 'tf'),
        SetRemap('/tf_static', 'tf_static'),
        include('tiago_bringup', 'tiago_bringup.launch.py', {
            'namespace': name, 'is_public_sim': 'True', 'use_sim_time': 'True',
            'gazebo_version': 'classic', 'arm_type': 'tiago-arm',
            'end_effector': 'pal-hey5',
        }),
        Node(package='gazebo_ros', executable='spawn_entity.py', output='screen',
             arguments=['-topic', 'robot_description', '-entity', name,
                        '-robot_namespace', name, '-x', str(x), '-y', str(y),
                        '-z', '0.0']),
        Node(package='tiago_gazebo', executable='tuck_arm.py', output='screen',
             remappings=[('/play_motion2/is_motion_ready',
                          'play_motion2/is_motion_ready')]),
    ])

    navigation = GroupAction([
        PushRosNamespace(name),
        SetRemap('/tf', 'tf'),
        SetRemap('/tf_static', 'tf_static'),
        include('nav2_bringup', 'navigation_launch.py', {
            'namespace': name, 'params_file': nav_params, 'use_sim_time': 'True',
        }),
        include('nav2_bringup', 'slam_launch.py', {
            'namespace': name, 'params_file': nav_params, 'use_sim_time': 'True',
        }),
    ])

    rviz = Node(
        package='rviz2', executable='rviz2', namespace=name,
        arguments=['-d', str(Path(get_package_share_directory('nav2_bringup')) /
                             'rviz' / 'nav2_default_view.rviz')],
        parameters=[{'use_sim_time': True}],
        remappings=[('/map', 'map'), ('/tf', 'tf'), ('/tf_static', 'tf_static'),
                    ('/robot_description', 'robot_description'),
                    ('/goal_pose', 'goal_pose'), ('/clicked_point', 'clicked_point'),
                    ('/initialpose', 'initialpose')],
        output='screen',
    )
    return [bringup, navigation, rviz]


def generate_launch_description():
    world = str(Path(__file__).resolve().with_name('office_small.world'))
    packages = ['tiago_description', 'pmb2_description', 'pal_hey5_description',
                'pal_gripper_description', 'pal_robotiq_description',
                'omni_base_description', 'pal_urdf_utils']
    gazebo_models = [str(Path(get_package_prefix(pkg)) / 'share') for pkg in packages]
    gazebo_models.append(str(Path(get_package_share_directory('pal_gazebo_worlds')) / 'models'))
    if os.environ.get('GAZEBO_MODEL_PATH'):
        gazebo_models.append(os.environ['GAZEBO_MODEL_PATH'])

    nav_params = str(Path(get_package_share_directory('pmb2_2dnav')) /
                     'config' / 'nav_public_sim.yaml')
    actions = [
        SetEnvironmentVariable('LC_NUMERIC', 'C'),
        SetEnvironmentVariable('GAZEBO_MODEL_PATH', os.pathsep.join(gazebo_models)),
        include('pal_gazebo_worlds', 'pal_gazebo.launch.py', {
            'world_name': world, 'gazebo_version': 'classic', 'gzclient': 'True',
        }),
    ]
    for name, x, y in [('tiago1', 1.4, -0.7), ('tiago2', 1.4, 0.7)]:
        actions += robot(name, x, y, nav_params)
    return LaunchDescription(actions)
