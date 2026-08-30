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

    joy_config_file = os.path.join(
            get_package_share_directory("microtractor"),
            "config",
            "joy_config.yaml"
    )

    joy_node = Node(
        package="joy",
        executable="joy_node",
        parameters=[{
            "use_sim_time": use_sim_time
        },
        joy_config_file
        ]
    )
# ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_drive_controller/cmd_vel -p stamped:=true

    teleop_node = Node(
        package="teleop_twist_joy",
        executable="teleop_node",
        name="teleop_node",
        parameters=[{
            "use_sim_time": use_sim_time
        },
        joy_config_file
        ],
        remappings={("/cmd_vel", "/diff_drive_controller/cmd_vel")}
    )

    return LaunchDescription([
        use_sim_time_arg,
        joy_node,
        teleop_node,
    ])
