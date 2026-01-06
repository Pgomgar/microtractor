from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    map_type_arg = DeclareLaunchArgument('plot', default_value='false', choices=['true', 'false'], description="Escoge 'true' si prefieres que los puntos se muestren en un gráfico o 'false' para mostrarlos en un mapa. La opción por defecto es: 'false'")
    
    land_register_map_node = Node(
        package="land_register",
        executable="land_register_map",
        name="land_register_map",
        output="screen",
        condition=UnlessCondition(LaunchConfiguration('plot'))
    )

    land_register_plot_node = Node(
        package="land_register",
        executable="land_register_plot",
        name="land_register_plot",
        output="screen",
        condition=IfCondition(LaunchConfiguration('plot'))
    )

    combined_rtk_pkg = os.path.join(
        get_package_share_directory("combined_rtk"),
        "combined_nodes.launch.py"
    )

    combined_rtk_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(combined_rtk_pkg)
    )

    return LaunchDescription([
        map_type_arg,
        combined_rtk_launch,
        land_register_map_node,
        land_register_plot_node
    ])