import serial
from time import sleep
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
#ser = serial.Serial("/dev/ttyS0", 115200)  # Open port with baud rate
ser = serial.Serial("/dev/ttyAMA4", 115200)
COM = 0x55
buffer_RTT = [0] * 4

def calculate_distance(buffer):
    CS = buffer[1] + buffer[2]
    print(f"{buffer}")
    print(f"buffer 0: {buffer[0]} buffer 1: {buffer[1]} buffer 2: {buffer[2]} buffer 3: {buffer[3]} CS: {CS}")

    distance = (buffer[1] << 8) + buffer[2]
    return distance

while True:
    ser.write(bytes([COM]))
    print("Writing bytes")
    sleep(0.1)
    
    print(ser.inWaiting())
    if ser.inWaiting() > 0:
        print("waiting")
        sleep(0.004)
        val = ser.read()
        if val == b'\xff':
            print(f"Reading {ord(val)}")
            buffer_RTT[0] = 0xff
            for i in range(1, 4):
                buffer_RTT[i] = ord(ser.read())
            distance = calculate_distance(buffer_RTT)
            print(distance)
            if distance is not None:
                print(f"Distance: {distance}mm")
                r.set('bottom_distance', distance)
