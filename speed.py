import RPi.GPIO as GPIO
import time

# Define GPIO pins
CLK = 22
DT = 27

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to store counts and time
pulse_count = 0
prev_time = time.time()

# Callback function to count pulses
def pulse_callback(channel):
    global pulse_count
    pulse_count += 1

# Setup event detection
GPIO.add_event_detect(CLK, GPIO.RISING, callback=pulse_callback)

try:
    while True:
        time.sleep(1)  # Measure speed every second
        current_time = time.time()
        elapsed_time = current_time - prev_time
        prev_time = current_time
        
        # Calculate RPM (assuming encoder gives one pulse per revolution)
        rpm = (pulse_count / elapsed_time) * 60
        pulse_count = 0  # Reset pulse count for next measurement
      
        print(f'Speed: {rpm} RPM')
except KeyboardInterrupt:
    GPIO.cleanup()
