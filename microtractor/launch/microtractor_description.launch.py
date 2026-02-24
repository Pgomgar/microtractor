from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os
import xacro

def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value="false", description="Para usar el reloj de la simulación. Por defecto es False.")

    pkg_path = os.path.join(get_package_share_directory("microtractor"))
    urdf_file = os.path.join(pkg_path, "description", "microtractor.urdf.xacro")
    microtractor_description = xacro.process_file(urdf_file)

    use_sim_time = LaunchConfiguration("use_sim_time")

    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{
            "robot_description": microtractor_description.toxml(),
            "use_sim_time": use_sim_time
        }]
    )

    return LaunchDescription([
        use_sim_time_arg,
        node_robot_state_publisher
    ])

