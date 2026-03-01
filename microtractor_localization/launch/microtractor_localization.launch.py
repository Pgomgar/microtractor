from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    combined_rtk_pkg = os.path.join(
        get_package_share_directory("combined_rtk"),
        "combined_nodes.launch.py"
    )

    combined_rtk_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(combined_rtk_pkg)
    )

    imu_pkg = os.path.join(
        get_package_share_directory("sensors_node"), 
        "launch",
        "imu_mpu9250.launch.py"
    )

    imu_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(imu_pkg)
    )

    microtractor_description_pkg = os.path.join(
        get_package_share_directory("microtractor"), 
        "launch",
        "microtractor_description.launch.py"
    )

    microtractor_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(microtractor_description_pkg)
    )

    localization_pkg = os.path.join(
        get_package_share_directory("microtractor_localization"), 
        "launch",
        "localization.launch.py"
    )

    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(localization_pkg)
    )

    return LaunchDescription([
        microtractor_description_launch,
        combined_rtk_launch,
        imu_launch,
        localization_launch
    ])

