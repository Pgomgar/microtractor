from gpiozero import PWMOutputDevice, DigitalOutputDevice
from gpiozero.pins.lgpio import LGPIOFactory
from time import sleep

class BTS7960_Controller:
    def __init__(self, L_en, R_en, L_pwm, R_pwm, frequency=10000):
        lgpio_factory = LGPIOFactory()
        self.L_en = DigitalOutputDevice(L_en, pin_factory=lgpio_factory)
        self.R_en = DigitalOutputDevice(R_en, pin_factory=lgpio_factory)
        self.L_pwm = PWMOutputDevice(L_pwm, frequency=frequency, pin_factory=lgpio_factory)
        self.R_pwm = PWMOutputDevice(R_pwm, frequency=frequency, pin_factory=lgpio_factory)
    
    def forward(self, vel):
        self.L_en.on()
        self.R_en.on()

        self.L_pwm.value = 0.0
        self.R_pwm.value = vel

    def backward(self, vel):
        self.R_en.on()
        self.L_en.on()

        self.R_pwm.value = 0.0
        self.L_pwm.value = vel


    def stop(self):
        self.R_pwm.value = 0.0
        self.L_pwm.value = 0.0
        self.R_en.off()
        self.L_en.off()



if __name__=="__main__":
    DER_L_EN = 23
    DER_R_EN = 22
    DER_L_PWM = 12
    DER_R_PWM = 18

    IZQ_L_EN = 27
    IZQ_R_EN = 17
    IZQ_L_PWM = 13
    IZQ_R_PWM = 19

    izq_motor = BTS7960_Controller(IZQ_L_EN, IZQ_R_EN, IZQ_L_PWM, IZQ_R_PWM)
    der_motor = BTS7960_Controller(DER_L_EN, DER_R_EN, DER_L_PWM, DER_R_PWM)
    vel = 1.0

    try:

        print("### Comenzando prueba de velocidad ###")

        sleep(5)

        print("Moviendo adelante... ")
        izq_motor.forward(0.5)
        der_motor.forward(0.5)

        sleep(2)

        izq_motor.forward(vel)
        der_motor.forward(vel)

        sleep(10)

        print("Deteniendo ...")

        izq_motor.stop()
        der_motor.stop()

        #sleep(2)

        #print("Moviendo para atrás ...")

        #izq_motor.backward(vel)
        #der_motor.backward(vel)

        #sleep(3)

    finally:
        print("### Parando ###")
        izq_motor.stop()
        der_motor.stop()
