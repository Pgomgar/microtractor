from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os
import xacro

def generate_launch_description():

    pkg_path = os.path.join(get_package_share_directory("microtractor"))
    urdf_file = os.path.join(pkg_path, "description", "microtractor.urdf.xacro")
    microtractor_description = xacro.process_file(urdf_file)

    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{"robot_description": microtractor_description.toxml()}],
        output="screen"
    )

    joint_state_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen"
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
        output="screen"
    )

    return LaunchDescription([
        ros2_control_node,
        joint_state_spawner,
        diff_drive_spawner
    ])