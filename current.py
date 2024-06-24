import spidev
import time

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)  # (bus, device)

# read ADC channel
def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

adc_channel = 0

try:
    while True:
        # Read the ADC value
        adc_value = read_adc(adc_channel)
        current = adc_value * (5.0 / 1023.0) 
      
        print(f"Current: {current} A")
        
        time.sleep(1)
        
except KeyboardInterrupt:
    spi.close()
