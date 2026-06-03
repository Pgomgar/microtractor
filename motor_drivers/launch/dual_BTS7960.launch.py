from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    DER_L_EN_arg = DeclareLaunchArgument("DER_L_EN", default_value="23", description="Pin del puerto GPIO para L_EN del lado derecho.")
    DER_R_EN_arg = DeclareLaunchArgument("DER_R_EN", default_value="22", description="Pin del puerto GPIO para R_EN del lado derecho.")
    DER_L_PWM_arg = DeclareLaunchArgument("DER_L_PWM", default_value="12", description="Pin del puerto GPIO para L_PWM del lado derecho.")
    DER_R_PWM_arg = DeclareLaunchArgument("DER_R_PWM", default_value="18", description="Pin del puerto GPIO para R_PWM del lado derecho.")

    IZQ_L_EN_arg = DeclareLaunchArgument("IZQ_L_EN", default_value="27", description="Pin del puerto GPIO para L_EN del lador izquierdo.")
    IZQ_R_EN_arg = DeclareLaunchArgument("IZQ_R_EN", default_value="17", description="Pin del puerto GPIO para R_EN del lador izquierdo.")
    IZQ_L_PWM_arg = DeclareLaunchArgument("IZQ_L_PWM", default_value="13", description="Pin del puerto GPIO para L_PWM del lador izquierdo.")
    IZQ_R_PWM_arg = DeclareLaunchArgument("IZQ_R_PWM", default_value="19", description="Pin del puerto GPIO para R_PWM del lador izquierdo.")

    Frequency_arg = DeclareLaunchArgument("frequency", default_value="10000", description="Frecuencia para PWM. Es el mismo valor para ambos motores.")
    
    izq_motor_driver_node = Node(package="motor_drivers",
        executable="BTS7960_driver",
        name="izq_motor_driver_node",
        output="screen",
        parameters=[{
            "L_EN": LaunchConfiguration("IZQ_L_EN"),
            "R_EN": LaunchConfiguration("IZQ_R_EN"),
            "L_PWM": LaunchConfiguration("IZQ_L_PWM"),
            "R_PWM": LaunchConfiguration("IZQ_R_PWM"),
            "frequency": LaunchConfiguration("frequency")
        }],
        remappings=[("/cmd_vel/motor_relative", "/cmd_vel/PWM/IZQ")]
    )
    
    der_motor_driver_node = Node(package="motor_drivers",
        executable="BTS7960_driver",
        name="der_motor_driver_node",
        output="screen",
        parameters=[{
            "L_EN": LaunchConfiguration("DER_L_EN"),
            "R_EN": LaunchConfiguration("DER_R_EN"),
            "L_PWM": LaunchConfiguration("DER_L_PWM"),
            "R_PWM": LaunchConfiguration("DER_R_PWM"),
            "frequency": LaunchConfiguration("frequency")
        }],
        remappings=[("/cmd_vel/motor_relative", "/cmd_vel/PWM/DER")]
    )

    return LaunchDescription([
        DER_L_EN_arg,
        DER_R_EN_arg,
        DER_L_PWM_arg,
        DER_R_PWM_arg,
        IZQ_L_EN_arg,
        IZQ_R_EN_arg,
        IZQ_L_PWM_arg,
        IZQ_R_PWM_arg,
        Frequency_arg,
        izq_motor_driver_node,
        der_motor_driver_node
    ])