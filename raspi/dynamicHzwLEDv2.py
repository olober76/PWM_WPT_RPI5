from rpi_hardware_pwm import HardwarePWM
from enum import Enum

# Constants
DUTY_CYCLE = 50  # Start with a 50% duty cycle
PWM_PIN = 12     # GPIO pin for PWM (control both LED and frequency)

class AlreadyStartedException(Exception):
    pass

class ChannelNotFoundException(Exception):
    pass

class Channel(Enum):
    GPIO_12 = 0  # Assuming GPIO 12 is connected to the LED

class PwmControl:
    _pwms = {}

    def init(self, channel: Channel, frequency: int):
        if channel in self._pwms:
            raise AlreadyStartedException("Already initialized.")
        else:
            pwm = HardwarePWM(pwm_channel=channel.value, hz=frequency, chip=2)
            pwm.start(DUTY_CYCLE)  # Start with a 50% duty cycle
            self._pwms[channel] = pwm
            print(f"PWM initialized on {channel} with frequency {frequency} Hz")

    def set(self, channel: Channel, value: int):
        pwm = self._pwms.get(channel)
        if not pwm:
            raise ChannelNotFoundException("Channel not found. Did you init it first?")
        pwm.change_duty_cycle(min(max(value, 0), 100))  # Adjust duty cycle between 0 and 100%

    def change_frequency(self, channel: Channel, frequency: int):
        pwm = self._pwms.get(channel)
        if not pwm:
            raise ChannelNotFoundException("Channel not found. Did you init it first?")
        pwm.change_frequency(frequency)
        print(f"Frequency changed to {frequency} Hz")

    def stop(self, channel: Channel):
        pwm = self._pwms.get(channel)
        if not pwm:
            raise ChannelNotFoundException("Channel not found.")
        pwm.stop()
        print("PWM stopped.")

pwm_control = PwmControl()
pwm_control.init(Channel.GPIO_12, 1000)  # Initialize with 1 kHz frequency for GPIO 12

def set_frequency(frequency):
    pwm_control.change_frequency(Channel.GPIO_12, frequency)

def set_led_brightness(duty_cycle):
    pwm_control.set(Channel.GPIO_12, duty_cycle)  # Set duty cycle for brightness control
