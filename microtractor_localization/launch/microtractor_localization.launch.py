from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    pkg_path = os.path.join(get_package_share_directory("microtractor_localization"))
    ekf_file_path = os.path.join(pkg_path, "config", "ekf_navsat_transform.yaml")

    ekf_node = Node(package="robot_localization",
                    executable="ekf_node",
                    name="ekf_filter_node",
                    output="screen",
                    parameters=[ekf_file_path])
    
    navsat_trans_node = Node(package="robot_localization",
                            executable="navsat_transform_node", 
                            name="navsat_transform",
                            output="screen",
                            parameters=[ekf_file_path],
                            remappings=[("imu/data", "imu/data"),
                                        ("gps/fix", "ublox_gps_node/fix"),
                                        ("odometry/filtered", "odometry/filtered")])
    
    return LaunchDescription([
        ekf_node,
        navsat_trans_node
    ])
