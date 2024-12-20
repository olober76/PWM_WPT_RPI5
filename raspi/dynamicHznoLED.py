# dynamicHz.py (Refactored as a module)
from rpi_hardware_pwm import HardwarePWM
from enum import Enum
import gpiod
import time

DUTY_CYCLE = 50  # 50% duty cycle
LED_PIN = 17  # Adjust this to your LED pin

class AlreadyStartedException(Exception):
    pass

class ChannelNotFoundException(Exception):
    pass

class Channel(Enum):
    GPIO_12 = 0
    GPIO_13 = 1

class PwmControl:
    _pwms = {}

    def init(self, channel: Channel, frequency: int):
        if channel in self._pwms:
            raise AlreadyStartedException("Already initialized.")
        else:
            pwm = HardwarePWM(pwm_channel=channel.value, hz=frequency, chip=2)
            pwm.start(0)
            self._pwms[channel] = pwm

    def set(self, channel: Channel, value: int):
        pwm = self._pwms.get(channel)
        if not pwm:
            raise ChannelNotFoundException("Channel not found. Did you init it first?")
        pwm.change_duty_cycle(min(max(value, 0), 100))

    def change_frequency(self, channel: Channel, frequency: int):
        pwm = self._pwms.get(channel)
        if not pwm:
            raise ChannelNotFoundException("Channel not found. Did you init it first?")
        pwm.change_frequency(frequency)

    def stop(self, channel: Channel):
        pwm = self._pwms.get(channel)
        if not pwm:
            raise ChannelNotFoundException("Channel not found.")
        pwm.stop()

chip = gpiod.Chip('/dev/gpiochip0')
led_line = chip.get_line(LED_PIN)
led_line.request(consumer="LED_Control", type=gpiod.LINE_REQ_DIR_OUT)

pwm_control = PwmControl()
pwm_control.init(Channel.GPIO_12, 100000)  # Init with 100 kHz frequency

def set_frequency(frequency):
    pwm_control.change_frequency(Channel.GPIO_12, frequency)
