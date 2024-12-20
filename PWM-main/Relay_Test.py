#!/usr/bin/python3
# coding=utf-8
import RPi.GPIO as GPIO
import time

# Updated GPIO pins
in1 = 7
in2 = 8
in3 = 11
in4 = 25

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# GPIO.output(in1, False)
# GPIO.output(in2, False)
# GPIO.output(in3, False)
# GPIO.output(in4, False)

GPIO.output(in1, True)
GPIO.output(in2, True)
GPIO.output(in3, True)
GPIO.output(in4, True)

try:
    while True:
        for x in range(5):
            GPIO.output(in2, True)
            GPIO.output(in1, True)
            GPIO.output(in3, True)
            GPIO.output(in4, True)
            time.sleep(2)
            GPIO.output(in1, False)
            GPIO.output(in2, False)
            GPIO.output(in3, False)
            GPIO.output(in4, False)
            time.sleep(2)
            # GPIO.output(in1
            # , False)
            # GPIO.output(in2, True)
            # time.sleep(1)
            # GPIO.output(in2, False)

except KeyboardInterrupt:
    GPIO.cleanup()
