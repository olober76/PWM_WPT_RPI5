from rpi_hardware_pwm import HardwarePWM
from enum import Enum
import gpiod
import time

# Constants
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

    def init(self, channel: Channel, frequency: int):
        if channel in self._pwms:
            raise AlreadyStartedException("Already initialized.")
        else:
            print(f"Init {channel} with frequency {frequency} Hz")
            pwm = HardwarePWM(pwm_channel=channel.value, hz=frequency, chip=2)
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

    def change_frequency(self, channel: Channel, frequency: int):
        pwm = self._pwms[channel]
        if not pwm:
            raise ChannelNotFoundException("Channel not found. Did you init it first?")
        print(f"Changing frequency to {frequency} Hz")
        pwm.change_frequency(frequency)

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

# Inisialisasi PWM di GPIO 12 dengan frekuensi awal
initial_frequency = 100000  # 100 kHz
pwm_control.init(Channel.GPIO_12, initial_frequency)

# Loop utama untuk mengontrol PWM dan LED
try:
    while True:
        # Set PWM duty cycle ke 50%
        pwm_control.set(Channel.GPIO_12, DUTY_CYCLE)

        # Nyalakan LED
        led_line.set_value(1)

        # Meminta input untuk frekuensi baru
        user_input = input("Enter new frequency in Hz (or 'q' to quit): ")

        if user_input.lower() == 'q':
            break

        try:
            new_frequency = int(user_input)
            pwm_control.change_frequency(Channel.GPIO_12, new_frequency)
        except ValueError:
            print("Please enter a valid integer for the frequency.")

except KeyboardInterrupt:
    pass
finally:
    # Matikan PWM dan reset GPIO saat program dihentikan
    pwm_control.stop(Channel.GPIO_12)
    led_line.release()  # Melepas kontrol pin LED
    print("Program terminated.")

