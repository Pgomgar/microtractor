from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

import yaml
from datetime import datetime

# interfaz de MPU9250

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, # Dirección de memoria para
    address_mpu_master=MPU9050_ADDRESS_68,
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ
)
print("Calibrando el IMU, por favor, no lo mueva ...")
mpu.calibrate()
print("Calibración concluida")
mpu.configure()

bias = {
    "abias": mpu.abias,
    "gbias":mpu.gbias,
    "mbias":mpu.mbias,
    "magScale":mpu.magScale
}

ruta = f"mpu9250_bias_{datetime.now().date()}.yaml"

with open(ruta, 'w') as file:
    yaml.dump(bias, file, default_flow_style=False, allow_unicode=True)

print(f"Sesgos guardados correctamente en: {ruta}")