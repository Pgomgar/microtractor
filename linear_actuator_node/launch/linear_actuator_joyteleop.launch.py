from launch import LaunchDescription
from launch.actions import TimerAction
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os
import xacro

def generate_launch_description():
    MAX_DISTANCE = 100

    linear_actuator_service_node = Node(
        package="linear_actuator_node",
        executable="linear_actuator_service",
        name="linear_actuator_service",
        output="screen",
        parameters=[{
            "FORWARD_PIN":24,
            "BACKWARD_PIN":25,
            "MAX_DISTANCE": MAX_DISTANCE,
            "VEL":3
        }]
    )

    linear_actuator_joyteleop_node = Node(
        package="linear_actuator_node",
        executable="linear_actuator_joyteleop",
        name="linear_actuator_joyteleop",
        output="screen",
        parameters=[{
            "MAX_DISTANCE": MAX_DISTANCE,
            "AUTO_DISTANCE": 50,
            "STEP_SIZE": 5,
        }]
    )

    linear_actuator_joyteleop_node_delay = TimerAction(
        period=20.0,
        actions=[
            linear_actuator_joyteleop_node
        ]
    )

    return LaunchDescription([
        linear_actuator_service_node,
        linear_actuator_joyteleop_node_delay
    ])