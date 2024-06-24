import RPi.GPIO as GPIO
import spidev
import time
import csv
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase setup
cred = credentials.Certificate("path/to/your/firebase/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Sensor GPIO Pins
encoder_pin = 22  # Optical encoder
monostable_voltage_pin = 23  # Monostable multivibrator for voltage
monostable_current_pin = 24  # Monostable multivibrator for current

# SPI setup for ADC
SPI_CHANNEL = 0
SPI_SPEED = 1000000

spi = spidev.SpiDev()
spi.open(0, SPI_CHANNEL)
spi.max_speed_hz = SPI_SPEED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(encoder_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(monostable_voltage_pin, GPIO.IN)
GPIO.setup(monostable_current_pin, GPIO.IN)

# CSV logging setup
csv_file = "sensor_data.csv"

# Initialize CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Voltage (V)', 'Current (A)', 'Speed (RPM)', 'Power Factor'])

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def read_voltage():
    adc_value = read_adc(0)  # channel 0 for voltage
    voltage = (adc_value * 5.0) / 1023.0  # Convert ADC value to voltage
    voltage = (voltage - 2.5) * (230 / 2.5)  # Adjust to actual voltage range
    return voltage

def read_current():
    adc_value = read_adc(1)  # channel 1 for current
    current = (adc_value * 5.0) / 1023.0  # Convert ADC value to voltage
    current = (current - 2.5) * (5 / 2.5)  # Adjust to actual current range
    return current

def calculate_speed():
    encoder_ticks = 0

    def encoder_callback(channel):
        nonlocal encoder_ticks
        encoder_ticks += 1

    GPIO.add_event_detect(encoder_pin, GPIO.FALLING, callback=encoder_callback)

    start_time = time.time()
    time.sleep(1)  # Measure for 1 second
    end_time = time.time()
    elapsed_time = end_time - start_time

    speed_rpm = (encoder_ticks / elapsed_time) * 60  # Convert to RPM
    GPIO.remove_event_detect(encoder_pin)
    return speed_rpm

def read_power_factor():
    while GPIO.input(monostable_voltage_pin) == 0:
        voltage_time = time.time()

    while GPIO.input(monostable_current_pin) == 0:
        current_time = time.time()

    time_difference = abs(current_time - voltage_time)
    power_factor = np.cos(2 * np.pi * time_difference)
    return power_factor

def log_data_to_csv(timestamp, voltage, current, speed, power_factor):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, voltage, current, speed, power_factor])

def send_data_to_firebase(timestamp, voltage, current, speed, power_factor):
    data = {
        'timestamp': timestamp,
        'voltage': voltage,
        'current': current,
        'speed': speed,
        'power_factor': power_factor
    }
    db.collection('sensor_data').add(data)

try:
    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        voltage = read_voltage()
        current = read_current()
        speed = calculate_speed()
        power_factor = read_power_factor()

        log_data_to_csv(timestamp, voltage, current, speed, power_factor)
        send_data_to_firebase(timestamp, voltage, current, speed, power_factor)

        time.sleep(5)  # Adjust as needed

except KeyboardInterrupt:
    GPIO.cleanup()
    spi.close()
