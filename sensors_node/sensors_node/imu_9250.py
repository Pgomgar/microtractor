import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, MagneticField
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

from math import pi, radians
import yaml

GRAVEDAD_TIERRA = 9.81

# interfaz de MPU9250
class IMU_9250_Publisher(Node):

    def __init__(self):
        super().__init__("imu_9250_node")
        self.declare_parameter("bias_file_path", "no_bias")
        bias_file_path = self.get_parameter("bias_file_path").get_parameter_value().string_value

        self.imu_publisher = self.create_publisher(Imu, "/imu/data_raw", 10)
        self.mag_publisher = self.create_publisher(MagneticField, "/imu/mag", 10)


        self.mpu = MPU9250(
            address_ak=AK8963_ADDRESS, # Dirección de memoria para
            address_mpu_master=MPU9050_ADDRESS_68,
            address_mpu_slave=None,
            bus=1,
            gfs=GFS_1000, #Giroscopio: grados por segundo
            afs=AFS_8G, # Acelerómetro: Veces la aceleración de la gravedad en la Tierra 1G=9.81 m/s² 
            mfs=AK8963_BIT_16, # Magnetómetro: Dirección con respecto al campo magnético de la Tierra
            mode=AK8963_MODE_C100HZ
        )

        if bias_file_path != "no_bias":
            try:
                with open(bias_file_path, 'r') as file:
                    bias = yaml.safe_load(file)
                
                self.mpu.abias = bias["abias"]
                self.mpu.gbias = bias["gbias"]
                self.mpu.mbias = bias["mbias"]
                self.mpu.magScale = bias["magScale"]

                self.get_logger().info("Calibración del IMU cargada correctamente:\n" +
                                       f"- Aceleración: {bias["abias"]}\n" +
                                       f"- Giroscopio: {bias["gbias"]}\n" +
                                       f"- Magnetómetro: {bias["mbias"]}\n" +
                                       f"- Escala magnetómetro: {bias["magScale"]}"
                                       )
                
            except Exception as e:
                self.get_logger().error(f"No se pudo cargar el archivo YAML con la calibración: {e}")

        self.mpu.configure()
        self.get_logger().info("IMU configurado correctamente")
        #self.mpu.calibrateMPU6500()
        #self.mpu.configureMPU6500(self.mpu.gfs, self.mpu.afs)
        self.timer_ = self.create_timer(0.1, self.timer_callback)
    
    def timer_callback(self):
        # Lectura del IMU
        accel = self.mpu.readAccelerometerMaster()
        gyro = self.mpu.readGyroscopeMaster()
        mag = self.mpu.readMagnetometerMaster()

        # Cambio de unidades
        accel_norm = list(map(lambda x: x*GRAVEDAD_TIERRA, accel)) # Pasa los datos del IMU en G/s a m/s²
        gyro_norm = list(map(radians, gyro)) # Pasa los datos del IMU en grados/s a radianes/s
        mag_norm = list(map(lambda x: x/1000000, mag)) # Pasa los datos del Magnetómetro en Microteslas a Teslas

        # Preparación de los mensajes
        imu_msg = Imu()
        mag_msg = MagneticField()

        stamp = self.get_clock().now().to_msg()
        frame_id = "imu_link"

        # Mensaje del IMU
        imu_msg.header.stamp = stamp
        imu_msg.header.frame_id = frame_id

        imu_msg.linear_acceleration.x = accel_norm[0]
        imu_msg.linear_acceleration.y = accel_norm[1]
        imu_msg.linear_acceleration.z = accel_norm[2]

        imu_msg.angular_velocity.x = gyro_norm[0]
        imu_msg.angular_velocity.y = gyro_norm[1]
        imu_msg.angular_velocity.z = gyro_norm[2]

        #imu_msg.orientation_covariance = -1

        # Mensaje del magnetómetro
        mag_msg.header.stamp = stamp
        mag_msg.header.frame_id = frame_id

        mag_msg.magnetic_field.x = mag_norm[0]
        mag_msg.magnetic_field.y = mag_norm[1]
        mag_msg.magnetic_field.z = mag_norm[2]

        #mag_msg.magnetic_field_covariance = -1

        # Publicación de los mensajes
        self.imu_publisher.publish(imu_msg)
        self.mag_publisher.publish(mag_msg)

        # Unir con el filtro de madgwick 
        # sudo apt-get install ros-<YOUR_ROSDISTO>-imu-tools
        # ros2 launch imu_filter_madgwick ...
        # Hay que crear un launch

def main(args=None):
    try:
        rclpy.init(args=args)
        node = IMU_9250_Publisher()
        rclpy.spin(node)
    except Exception as e:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()