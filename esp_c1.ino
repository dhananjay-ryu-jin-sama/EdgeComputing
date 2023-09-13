#include <WiFi.h>

const int voltagePin = 2;  // Digital pin connected to the voltage square wave
const int currentPin = 3;  // Digital pin connected to the current square wave

const float frequency = 50.0;  // Frequency of the power supply (in Hz)

volatile unsigned long voltageTime;   // Variable to store the time of voltage zero-crossing
volatile unsigned long currentTime;   // Variable to store the time of current zero-crossing
volatile bool voltageCrossed = false; // Flag indicating voltage zero-crossing event
volatile bool currentCrossed = false; // Flag indicating current zero-crossing event

void IRAM_ATTR voltageInterrupt() {
  voltageTime = micros();
  voltageCrossed = true;
}

void IRAM_ATTR currentInterrupt() {
  currentTime = micros();
  currentCrossed = true;
}

void setup() {
  Serial.begin(9600);
  pinMode(voltagePin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(voltagePin), voltageInterrupt, FALLING);
  pinMode(currentPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(currentPin), currentInterrupt, FALLING);
}

void loop() {
  if (voltageCrossed && currentCrossed) {
    voltageCrossed = false;
    currentCrossed = false;
   
    unsigned long voltagePeriod = currentTime - voltageTime;
    float voltageFrequency = 1000000.0 / voltagePeriod;  // Frequency in Hz
   
    float powerFactor = voltageFrequency / frequency;
   
    // Print or process the power factor value as needed
    Serial.print("Power Factor: ");
    Serial.println(powerFactor, 4);
  }
 
  // Additional tasks or measurements can be performed here
 
  delay(100);  // Adjust delay as needed for your specific application
}