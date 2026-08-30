from .BTS7960_motor import BTS7960_Controller
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor

from std_msgs.msg import Float32

class BTS7960_Driver(Node):
    def __init__(self):
        super().__init__("BTS7960_driver_node")

        self.declare_parameter("L_EN", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Pin del puerto GPIO para L_EN."))
        self.declare_parameter("R_EN", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Pin del puerto GPIO para R_EN."))
        self.declare_parameter("L_PWM", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Pin del puerto GPIO para L_PWM."))
        self.declare_parameter("R_PWM", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Pin del puerto GPIO para R_PWM."))
        self.declare_parameter("frequency", 10000, descriptor=ParameterDescriptor(description="Frecuencia para PWM."))

        L_EN = self.get_parameter("L_EN").get_parameter_value().integer_value
        R_EN = self.get_parameter("R_EN").get_parameter_value().integer_value
        L_PWM = self.get_parameter("L_PWM").get_parameter_value().integer_value
        R_PWM = self.get_parameter("R_PWM").get_parameter_value().integer_value
        frequency = self.get_parameter("frequency").get_parameter_value().integer_value

        self.motor = BTS7960_Controller(L_EN, R_EN, L_PWM, R_PWM, frequency)

        self.subscription = self.create_subscription(Float32, "/cmd_vel/motor_relative", self.motor_driver, 10)
    
    def motor_driver(self, msg):
        vel = msg.data
        #vel debe ser entre 0 y 1
        
        if vel < 0.0:
            #self.get_logger().info(f"Moviendo motor para atrás a velocidad {-1*vel}")
            self.motor.backward(-1*vel)

        elif vel > 0.0:

            if vel > 1.0:
                #self.get_logger().info(f"Moviendo motor para delante a velocidad {vel}")
                self.motor.forward(1.0)
            else:
                #self.get_logger().info(f"Moviendo motor para delante a velocidad {vel}")
                self.motor.forward(vel)

        else: #vel == 0.0
            #self.get_logger().info(f"Parando motor")
            self.motor.stop()
    
def main(args=None):
    rclpy.init(args=args)
    motor_driver = BTS7960_Driver()

    try:
        rclpy.spin(motor_driver)
    except KeyboardInterrupt:
        pass
    finally:
        motor_driver.destroy_node()
        rclpy.shutdown()
