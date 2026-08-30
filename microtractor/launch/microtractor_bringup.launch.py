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
    use_sim_time = LaunchConfiguration("use_sim_time")

    microtractor_diff_controller_pkg = os.path.join(
        get_package_share_directory("microtractor"),
        "launch",
        "microtractor_diff_controller.launch.py"
    )

    microtractor_diff_controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(microtractor_diff_controller_pkg),
        launch_arguments={
            "use_sim_time": use_sim_time
        }.items()
    )

    microtractor_localization_pkg = os.path.join(
            get_package_share_directory("microtractor_localization"),
            "launch",
            "microtractor_localization.launch.py"
    )

    microtractor_localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(microtractor_localization_pkg)
    )

    motor_drivers_pkg = os.path.join(
            get_package_share_directory("motor_drivers"),
            "launch",
            "dual_BTS7960.launch.py"
    )

    motor_drivers_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(motor_drivers_pkg)
    )

    linear_actuator_service_node = Node(
        package="linear_actuator_node",
        executable="linear_actuator_service",
        name="linear_actuator_service",
        output="screen",
        parameters=[{
            "FORWARD_PIN":24,
            "BACKWARD_PIN":25,
            "MAX_DISTANCE": 100,
            "VEL":3
        }]
    )

    teleop_joy_pkg = os.path.join(
        get_package_share_directory("microtractor"),
        "launch",
        "teleop_joy.launch.py"
    )

    teleop_joy_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(teleop_joy_pkg),
        launch_arguments={
            "use_sim_time": use_sim_time
        }.items()
    )

    return LaunchDescription([
        use_sim_time_arg,
        microtractor_diff_controller_launch,
        #microtractor_localization_launch,
        motor_drivers_launch,
        linear_actuator_service_node,
        teleop_joy_launch,
    ])