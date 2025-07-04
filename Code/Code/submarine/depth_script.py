import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
#chan = AnalogIn(ads, ADS.P0, ADS.P1)

CURRENT_INIT = 0.004
RANGE = 5000
DENSITY_WATER = 1
VREF = 3300


r = redis.Redis(host='localhost', port=6379, decode_responses=True)



while True:
    dataCurrent = chan.voltage / 120.0
    depth = (dataCurrent - CURRENT_INIT) * (RANGE / DENSITY_WATER /  16.0)
	r.set('depth', depth)	
	time.sleep(1)
