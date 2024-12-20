#!/usr/bin/python3
# coding=utf-8
import RPi.GPIO as GPIO
import pigpio
import time
import smbus
import Adafruit_SSD1306  # For OLED
import csv
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
from ina219 import INA219, DeviceRangeError
from PIL import Image, ImageDraw, ImageFont
import subprocess
import serial

# pigpio.pi('wpt', 8888)

# Recv data nano
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
ser.reset_input_buffer()

# Set the PWM frequency in Hz
PWM_FREQUENCY =200000 #default start frequency
PWM_PIN = 18                                                                                           
DUTY_CYCLE = 500000

#ina219
SHUNT_OHM = 0.115
MAX_EXPECTED_AMPS=2.0

#sweeping step
DEBOUNCE_DELAY = 0.01  # debounce delay
step = 2000
HOLD_DELAY = 0.5 #for up and down hold state
SWEEP_RANGE = 50000 #range of sweeping 

# Button pins
BUTTON_UP_PIN = 9
BUTTON_DOWN_PIN = 10             
BUTTON_SWEEP_PIN = 24
BUTTON_CHANGE_COIL = 22

# Define the LCD display size (16x2)
lcd_columns = 16
lcd_rows = 2

# Updated GPIO pins
in1 = 7
in2 = 8
in3 = 11
in4 = 25

#Coil
COIL_SIZE = 0 

# Initialize variables
current_frequency = PWM_FREQUENCY

## GPIO SETUP
#COIL
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

GPIO.output(in1, False)
GPIO.output(in2, False)
GPIO.output(in3, False)
GPIO.output(in4, False)

# Set up GPIO mode and pull-up resistors for buttons
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_SWEEP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_CHANGE_COIL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##initialize library
# Initialize the pigpio library
pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to the Pi. Make sure pigpiod is running.")
    exit()

#Initialize the INA219 
bus=smbus.SMBus(1)
time.sleep(1)
ina219 = INA219(SHUNT_OHM,MAX_EXPECTED_AMPS)
ina219.configure(ina219.RANGE_32V, ina219.GAIN_AUTO, ina219.ADC_9BIT)

# Initialize I2C bus and LCD object
lcd = LCD()
def safe_exit(signum, frame):
    exit(1)

# Initialize the OLED display
oled = Adafruit_SSD1306.SSD1306_128_64(rst=None)
oled.begin()
oled.clear()
oled.display()
width = oled.width
height = oled.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Initialize variables to track button state and last button press time
button_up_last_state = GPIO.input(BUTTON_UP_PIN)
button_down_last_state = GPIO.input(BUTTON_DOWN_PIN)
button_step_last_state = GPIO.input(BUTTON_SWEEP_PIN)
button_coil_last_state = GPIO.input(BUTTON_CHANGE_COIL)

last_button_up_time = time.time()
last_button_down_time = time.time()
last_button_step_time = time.time()
last_button_coil_time = time.time()

button_up_pressed = False
button_down_pressed = False

#functions
def update_display():
    global current_frequency
    global step
    # Clear the LCD screen
    if COIL_SIZE == 0:
        COIL_USED = 'KECIL'
    else:
        COIL_USED = 'BESAR'
    lcd.clear()
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.text("Freq:{}".format(current_frequency), 1)
    lcd.text("COIL %s " % (COIL_USED), 2)

def update_oled_display():
    global voltage
    global current
    global power
    voltage = ina219.voltage() 
    # raw_current = ina219.current()
    current = ina219.current()
    # current = current_conversion(raw_current,1,220)

    power = voltage * current
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0,0),"INA219",font=font, fill=255)
    draw.text((0,16),"V: %.2f V" % voltage, font=font, fill=255)
    draw.text((0,32),"I: %.6f mA" % current, font=font, fill=255)
    draw.text((0,48),"P: %.2f mW" % power, font=font, fill=255)
    oled.image(image)
    oled.display()

def current_conversion(adjusted_current, shunt_resistor, added_resistor):
    original_current = adjusted_current *1000* (shunt_resistor / (shunt_resistor + added_resistor))
    return original_current

def change_frequency(current_frequency):
    # global current_frequency
    global DUTY_CYCLE                                 
    if current_frequency < 0:
        current_frequency = 0
    if current_frequency > 1000000:
        current_frequency = 1000000
    
    # Set the new PWM frequency
    pi.hardware_PWM(PWM_PIN, current_frequency, DUTY_CYCLE)
    
def change_frequency_sweep(current_frequency):
    # global current_frequency
    global DUTY_CYCLE
    global voltage
    global current
    global power                                 
    if current_frequency < 0:
        current_frequency = 0
    if current_frequency > 1000000:
        current_frequency = 1000000
    
    # Set the new PWM frequency
    pi.hardware_PWM(PWM_PIN, current_frequency, DUTY_CYCLE)
    for i in range (5):
        update_oled_display()
        ser.reset_input_buffer()
        line = ser.readline().decode('utf-8').rstrip()
        temp = line.split(",")
        Receiver_voltage= float(temp[0])
        Receiver_current= float(temp[1])
        Receiver_power = Receiver_voltage * Receiver_current
        voltage = ina219.voltage()
        current = ina219.current()
        generate_csv(current_frequency,voltage,current,power)
        R_generate_csv(current_frequency,Receiver_voltage,Receiver_current,Receiver_power)
        time.sleep(0.15)

    lcd.clear()
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)
    lcd.text("Freq:{}".format(current_frequency), 1)
    lcd.text("Freq Sweeping..." , 2)

def generate_csv(frequency, voltage, current, power):
    # Define the CSV file name
    csv_file = "/home/wpt/PWM/CSV_data/T_power_data.csv"

    # Create or open the CSV file in append mode
    with open(csv_file, 'a', newline='') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # If the file is empty, write the header row
        if file.tell() == 0:
            csv_writer.writerow(["Frequency (Hz)", "Voltage (V)", "Current (mA)", "Power (mW)"])

        # Write the data to the CSV file
        csv_writer.writerow([frequency, voltage, current, power])

def R_generate_csv(frequency, voltage, current, power):
    csv_file = "/home/wpt/PWM/CSV_data/R_power_data.csv"

    # Create or open the CSV file in append mode
    with open(csv_file, 'a', newline='') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        # If the file is empty, write the header row
        if file.tell() == 0:
            csv_writer.writerow(["Frequency (Hz)", "Voltage (V)", "Current (mA)", "Power (mW)"])


        # Write the data to the CSV file
        csv_writer.writerow([frequency, voltage, current, power])


#Run Code and Buttons
try:
    while True:
        change_frequency(current_frequency)
        update_oled_display()
        update_display()

        current_time = time.time()

        if not GPIO.input(BUTTON_UP_PIN):
            if not button_up_pressed:
                button_up_pressed = True
                last_button_up_time = current_time
            if current_time - last_button_up_time > HOLD_DELAY:
                current_frequency += 10000
            else:
                current_frequency += 1000

        else:
            button_up_pressed = False

        # # Check and debounce BUTTON_DOWN_PIN
        if not GPIO.input(BUTTON_DOWN_PIN):
            if not button_down_pressed:
                button_down_pressed = True
                last_button_down_time = current_time
            if current_time - last_button_down_time > HOLD_DELAY:
                current_frequency -= 10000
            else:
                current_frequency -= 1000
        else:
            button_down_pressed = False

        if not GPIO.input(BUTTON_SWEEP_PIN):
            if current_time - last_button_step_time > DEBOUNCE_DELAY:
                Real_current_frequency= current_frequency
                # sweep_start_frequency = current_frequency - SWEEP_RANGE
                sweep_start_frequency = 0
                # sweep_end_frequency = current_frequency + SWEEP_RANGE
                sweep_end_frequency =250000
                # sweep_direction = 1  # Start sweeping in the increasing direction
                current_frequency=sweep_start_frequency
                #Clear old csv file
                csv_file = "/home/wpt/PWM/CSV_data/T_power_data.csv"
                with open(csv_file, 'w', newline=''):
                    pass

                csv_file = "/home/wpt/PWM/CSV_data/R_power_data.csv"
                with open(csv_file, 'w', newline=''):
                    pass

                while True:
                    current_frequency += step
                    change_frequency_sweep(current_frequency)
                    if current_frequency <= 150500:
                        GPIO.output(in1, False)
                        GPIO.output(in2, False)
                    else:
                        GPIO.output(in1, True)
                        GPIO.output(in2, True)
                    if current_frequency >sweep_end_frequency:
                        shell_script_path= "/home/wpt/PWM/.git/hooks/autoPush"
                        try:
                            subprocess.run(shell_script_path, shell=True, check=True)
                            print("CSV successfully updated to github repo.")
                        except:
                            print(f"CSV failed to push to github repo: (e)")
                        break
                current_frequency=Real_current_frequency
                last_button_step_time = current_time
        
        if not GPIO.input(BUTTON_CHANGE_COIL):
            if current_time - last_button_coil_time > DEBOUNCE_DELAY:
                COIL_SIZE = 1 - COIL_SIZE  # Toggle between 0 and 1
                last_button_coil_time = current_time

        # Relay Coil
        GPIO.output(in4, COIL_SIZE == 0)  # Small Coil
        GPIO.output(in3, COIL_SIZE == 1)  # Big Coil --> function

        # Relay Capacitor
        if current_frequency <= 115000:
            GPIO.output(in1, False)
            GPIO.output(in2, False)
        else:
            GPIO.output(in1, True)
            GPIO.output(in2, True)
        time.sleep(0.2)

except KeyboardInterrupt:
    pass
finally:
    pi.hardware_PWM(PWM_PIN, 0, 0)  # Turn off PWM on exit
    pi.stop()
    GPIO.cleanup()