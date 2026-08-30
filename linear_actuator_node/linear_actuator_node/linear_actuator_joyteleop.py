import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rcl_interfaces.msg import ParameterDescriptor
from microtractor_interfaces.srv import LinearActuator
from sensor_msgs.msg import Joy

class LinearActuatorJoyTeleop(Node):
    def __init__(self):
        super().__init__("linear_actuator_joyteleop_node")

        callback_group = ReentrantCallbackGroup()

        self.declare_parameter("MAX_DISTANCE", rclpy.Parameter.Type.INTEGER, ParameterDescriptor(description="Máxima distancia en milimetros a la que se puede estirar el actuador lineal"))
        self.declare_parameter("AUTO_DISTANCE", rclpy.Parameter.Type.INTEGER, ParameterDescriptor(description="Distancia en milímetros al que el actuador lineal se moverá automáticamente al pulsar el botón 2."))
        self.declare_parameter("STEP_SIZE", rclpy.Parameter.Type.INTEGER, ParameterDescriptor(description="Tamaño en milímetros del avance que puede hacer el actuador lineal al pulsar el botón 0."))

        self.MAX_DISTANCE = self.get_parameter("MAX_DISTANCE").get_parameter_value().integer_value
        self.AUTO_DISTANCE = self.get_parameter("AUTO_DISTANCE").get_parameter_value().integer_value
        self.STEP_SIZE = self.get_parameter("STEP_SIZE").get_parameter_value().integer_value

        self.currrent_distance = 0
        self.ocuapdo = False

        self.linear_actuator_client = self.create_client(LinearActuator, "linear_actuator", callback_group=callback_group)
        while not self.linear_actuator_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Esperando al servicio linear_actuator...")

        self.joy_subcriber = self.create_subscription(Joy, "/joy", self.joy_petition, 10, callback_group=callback_group)

    def joy_petition(self, msg: Joy):
        if self.ocuapdo:
            return
        
        if len(msg.buttons) < 4:
            self.get_logger().warn("No hay botnones suficientes")
            return
        
        if msg.buttons[0] == 1:
            future_distance = 0
            self.ocuapdo = True

            if self.currrent_distance + self.STEP_SIZE  >= self.MAX_DISTANCE:
                future_distance = self.MAX_DISTANCE
            else:
                future_distance = self.currrent_distance + self.STEP_SIZE

            self.send_petition(future_distance)

        elif msg.buttons[1] == 1:
            future_distance = 0
            self.ocuapdo = True

            if self.currrent_distance - self.STEP_SIZE  <= 0:
                future_distance = 0
            else:
                future_distance = self.currrent_distance - self.STEP_SIZE

            self.send_petition(future_distance)

        elif msg.buttons[2] == 1:
            self.ocuapdo = True

            self.send_petition(self.AUTO_DISTANCE)

        elif msg.buttons[3] == 1:
            self.ocuapdo = True
            
            self.send_petition(0)

    def send_req(self, future_distance):
        req = LinearActuator.Request()

        req.distance = future_distance

        future = self.linear_actuator_client.call(req)

        #self.spin_until_future_complete(self,future=future)

        return future

    def send_petition(self, future_distance):
        respuesta = self.send_req(future_distance)

        if respuesta.success:
            self.currrent_distance = future_distance
        else:
            self.get_logger().warn("El servicio ha fallado")

        self.ocuapdo = False

def main(args=None):
    rclpy.init()

    linear_actuator_teleop_node = LinearActuatorJoyTeleop()

    executor = MultiThreadedExecutor()
    executor.add_node(linear_actuator_teleop_node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        linear_actuator_teleop_node.destroy_node()
        rclpy.shutdown()