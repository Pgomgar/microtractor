import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor
from microtractor_interfaces.srv import LinearActuator

from .LinearActuatorDriver import LinearActuatorDriver

class LinearActuatorService(Node):
    def __init__(self):
        super().__init__("linear_actuator_service")
        self.CURRENT_DISTANCE = 0

        self.declare_parameter("FORWARD_PIN", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Pin del puerto GPIO para mover el actuador hacia delante."))
        self.declare_parameter("BACKWARD_PIN", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Pin del puerto GPIO para mover el actuador hacia atrás."))
        self.declare_parameter("MAX_DISTANCE", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Máxima distancia en milimetros a la que se puede estirar el actuador lineal"))
        self.declare_parameter("VEL", rclpy.Parameter.Type.INTEGER, descriptor=ParameterDescriptor(description="Velocidad en milimetros por segundo con la que se mueve el actuaor lineal."))

        self.srv = self.create_service(LinearActuator, "linear_actuator", self.callback)

        FORWARD_PIN = self.get_parameter("FORWARD_PIN").get_parameter_value().integer_value
        BACKWARD_PIN = self.get_parameter("BACKWARD_PIN").get_parameter_value().integer_value
        self.MAX_DISTANCE = self.get_parameter("MAX_DISTANCE").get_parameter_value().integer_value
        self.VEL = self.get_parameter("VEL").get_parameter_value().integer_value

        self.linear_actuator_driver = LinearActuatorDriver(FORWARD_PIN, BACKWARD_PIN)
        self.linear_actuator_driver.stop()
        self.get_logger().info("Moviendo actuador lineal a su posición inicial")
        self.linear_actuator_driver.backward(self.MAX_DISTANCE / self.VEL) # Volver al punto de inicio, por si estuviese abierto
        self.get_logger().warn("Servicio activo")

    def callback(self, request, response):
        if request.distance > self.MAX_DISTANCE:
            response.success = False

            return response

        dis = request.distance - self.CURRENT_DISTANCE

        if dis == 0:
            self.get_logger().warn("El actuador lineal no se ha movido")
            response.success = True
            return response
        
        time_active = abs(round((dis / self.VEL)*1.10, 1)) # 10% de error y un solo decimal

        
        try:
            if dis > 0.0:
                self.linear_actuator_driver.forward(time_active)
            elif dis < 0.0:
                self.linear_actuator_driver.backward(time_active)
            else:
                self.get_logger().warn("El actuador lineal no se ha movido")

            response.success = True
            self.CURRENT_DISTANCE = request.distance

        except Exception as e:
            response.success = False
            self.get_logger().error(f'Error en el servicio del actuador lineal: {e}')

        finally:
            self.get_logger().info(f"La distancia actual es de {self.CURRENT_DISTANCE} mm")
            return response



def main(args=None):
    try:
        rclpy.init(args=args)
        la_srv = LinearActuatorService()

        rclpy.spin(la_srv)
    except (KeyboardInterrupt):
        pass