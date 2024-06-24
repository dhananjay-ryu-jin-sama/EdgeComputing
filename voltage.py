import spidev
import time
import RPi.GPIO as GPIO

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    if channel > 7 or channel < 0:
        return -1
    # Perform SPI transaction and store returned bits
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    # Construct single integer out of the returned bits
    adc_out = ((r[1] & 3) << 8) + r[2]
    return adc_out

def convert_to_voltage(adc_value, v_ref=3.3, adc_resolution=1024):
    # Convert ADC value to voltage
    return (adc_value / float(adc_resolution)) * v_ref

try:
    while True:
        adc_value = read_adc(0)  # Read from channel 0
        voltage = convert_to_voltage(adc_value)
        print("ADC Value: {}, Voltage: {:.2f}V".format(adc_value, voltage))
        time.sleep(1)
except KeyboardInterrupt:
    pass

spi.close()
GPIO.cleanup()
