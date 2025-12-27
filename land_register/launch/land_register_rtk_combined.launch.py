from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    land_register_node = Node(
        package="land_register",
        executable="land_register",
        name="land_register",
        output="screen"
    )

    combined_rtk_pkg = os.path.join(
        get_package_share_directory("combined_rtk"),
        "combined_nodes.launch.py"
    )

    combined_rtk_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(combined_rtk_pkg)
    )

    return LaunchDescription([
        combined_rtk_launch,
        land_register_node
    ])