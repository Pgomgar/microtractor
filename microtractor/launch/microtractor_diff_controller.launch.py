from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessStart
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
    microtractor_controllers = os.path.join(pkg_path, "config", "microtractor_controllers.yaml")

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

    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[microtractor_controllers],
        output="screen"
    )

#    joint_state_spawner = Node(
#        package="controller_manager",
#        executable="spawner",
#        arguments=["joint_state_broadcaster"],
#        output="screen"
#    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
        output="screen"
    )

    ros2_control_node_delay = RegisterEventHandler(
        OnProcessStart(
            target_action=node_robot_state_publisher,
            on_start=[ros2_control_node]
        )
    )

    diff_drive_delay = RegisterEventHandler(
        OnProcessStart(
            target_action=ros2_control_node,
            on_start=[diff_drive_spawner]
        )
    )

    return LaunchDescription([
        use_sim_time_arg,
        node_robot_state_publisher,
        ros2_control_node_delay,
        #joint_state_spawner,
        diff_drive_delay
    ])