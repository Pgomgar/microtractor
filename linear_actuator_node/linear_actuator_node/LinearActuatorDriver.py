import time

from gpiozero import DigitalOutputDevice
from gpiozero.pins.lgpio import LGPIOFactory



class LinearActuatorDriver:
    def __init__(self, pin_forward, pin_backward):
        lgpio_factory = LGPIOFactory()
        self.forward_out = DigitalOutputDevice(pin_forward, pin_factory=lgpio_factory)
        self.backward_out = DigitalOutputDevice(pin_backward, pin_factory=lgpio_factory)

        self.stop()

    def forward(self, t):
        self.forward_out.off()
        self.backward_out.on()
        time.sleep(t)

        self.stop()

    def backward(self, t):
        self.forward_out.on()
        self.backward_out.off()
        time.sleep(t)

        self.stop()

    def stop(self):
        self.forward_out.on()
        self.backward_out.on()

if __name__=="__main__":

    FORWARD = 24
    BACKWARD = 25

    la = LinearActuatorDriver(FORWARD, BACKWARD)
    la.forward(10.0)
    la.stop()
    time.sleep(5.0)
    la.backward(10.0)
    la.stop()