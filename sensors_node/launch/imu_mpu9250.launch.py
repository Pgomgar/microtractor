from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    bias_file_path = "/home/pgomgar/Desktop/rtk_ws/src/sensors_node/config/mpu9250_bias_2026-02-14.yaml"
    
    bias_file_path_arg = DeclareLaunchArgument(
        "bias_file_path",
        default_value=bias_file_path,
        description='Ruta al archivo de calibración del IMU6666'
    )

    mpu_9250_node = Node(package="sensors_node",
        executable="imu_mpu_9250",
        name="imu_node",
        output="screen",
        parameters=[{
            "bias_file_path": LaunchConfiguration("bias_file_path")
            }])
    
    imu_filter_pkg = os.path.join(
        get_package_share_directory("imu_filter_madgwick"),
        "launch",
        "imu_filter.launch.py"
    )

    imu_filter_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(imu_filter_pkg)
    )

    return LaunchDescription([
        bias_file_path_arg,
        mpu_9250_node,
        imu_filter_launch
    ])
    
