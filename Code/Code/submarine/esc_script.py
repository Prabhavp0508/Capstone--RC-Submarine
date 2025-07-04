import os
import time
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
os.system("sudo pigpiod")  # Launching GPIO library
time.sleep(1)  # As I said it is too impatient and so if this delay is removed you will get an error
import pigpio  # importing GPIO library


ESC = 12 # Connect the ESC in this GPIO pin 

motor_enabled = False

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) 


max_value = 2000  # change this if your ESC's max value is different or leave it be
min_value = 700  # change this if your ESC's min value is different or leave it be


def arm():
    global motor_enabled
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, max_value)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, min_value)
    time.sleep(1)
    motor_enabled = True

arm()
while True:
    motor = r.get('motor')
    motorValue = r.get('motorValue')

    if motorValue == None:
        motorValue = 700

    if motor_enabled and motor == "stop":
        motor_enabled = False
    elif not motor_enabled and motor == "start":
        motor_enabled = True
    
    if motor_enabled:
    	pi.set_servo_pulsewidth(ESC, motorValue)
    else:
        pi.set_servo_pulsewidth(ESC, 700) 
