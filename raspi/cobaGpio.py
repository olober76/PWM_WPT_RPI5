from rpi_hardware_pwm import HardwarePWM
from enum import Enum
import gpiod
import time

# Constants
PWM_FREQUENCY = 1000000  # 100 kHz
DUTY_CYCLE = 50  # 50% duty cycle
LED_PIN = 17  # Sesuaikan dengan pin GPIO yang digunakan untuk LED

# Custom exceptions
class AlreadyStartedException(Exception):
    pass

class ChannelNotFoundException(Exception):
    pass

# Enum untuk Channel PWM
class Channel(Enum):
    GPIO_12 = 0
    GPIO_13 = 1

# Kelas untuk kontrol PWM
class PwmControl:
    _pwms = {}

    def init(self, channel: Channel):
        if channel in self._pwms:
            raise AlreadyStartedException("Already initialized.")
        else:
            print(f"Init {channel}")
            pwm = HardwarePWM(pwm_channel=channel.value, hz=PWM_FREQUENCY, chip=2)
            pwm.start(0)
            self._pwms[channel] = pwm

    def set(self, channel: Channel, value: int):
        pwm = self._pwms[channel]
        if not pwm:
            raise ChannelNotFoundException("Channel not found. Did you init it first?")
        value = min(value, 100)
        value = max(value, 0)
        print(f"Set {channel} {value}% duty cycle")
        pwm.change_duty_cycle(value)

    def stop(self, channel: Channel):
        pwm = self._pwms[channel]
        if not pwm:
            raise ChannelNotFoundException("Channel not found. Should it be stopped?")
        pwm.stop()

# Inisialisasi GPIO menggunakan gpiod untuk LED control
chip = gpiod.Chip('/dev/gpiochip0')
led_line = chip.get_line(LED_PIN)

# Konfigurasi LED sebagai output
led_line.request(consumer="LED_Control", type=gpiod.LINE_REQ_DIR_OUT)

# Membuat instance PwmControl
pwm_control = PwmControl()

# Inisialisasi PWM di GPIO 12
pwm_control.init(Channel.GPIO_12)

# Loop utama untuk mengontrol PWM dan LED
try:
    while True:
        # Set PWM duty cycle ke 50%
        pwm_control.set(Channel.GPIO_12, DUTY_CYCLE)

        # Nyalakan LED
        led_line.set_value(1)

         #time.sleep(0.5)  # Tunggu selama 500ms

        # Matikan PWM
        # pwm_control.set(Channel.GPIO_12, 0)

        # Matikan LED
         #led_line.set_value(0)

         #time.sleep(0.5)  # Tunggu selama 500ms

except KeyboardInterrupt:
    # Matikan PWM dan reset GPIO saat program dihentikan
    pwm_control.stop(Channel.GPIO_12)
    led_line.release()  # Melepas kontrol pin LED
