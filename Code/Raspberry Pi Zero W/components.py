# Import der benötigten Bibliotheken
import RPi.GPIO as GPIO
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import math

class CurrentSensor:
    def __init__(self, logging_period):
        self.logging_period = logging_period
    

    def log_voltage(self, noise = 0.011):
        analog_voltage_list = []
        period_start = time.time()

        # Messung der Stromstärke
        while True:
            analog_voltage_list.append(current_sens.voltage)
            if (time.time() - period_start) >= self.logging_period:
                break

        # Auf kleinste auflösbare analoge Ausgangsspannung runden
        for i in range(len(analog_voltage_list)):
            analog_voltage_list[i] = (round(analog_voltage_list[i] / noise)) * noise

        return analog_voltage_list
    

    def calibrate_offset_voltage(self, forced = False):
        # Öffnen des Relais
        if forced == True:
            GPIO.output(relay[1], relay_config[0])
            time.sleep(0.5)
       
        # Berechnung der Offset-Spannung 
        offset_voltage_list = self.log_voltage()
        offset_voltage = sum(offset_voltage_list) / len(offset_voltage_list)

        return offset_voltage
        
    
    def get_max_voltage(self):
        analog_voltage_list = self.log_voltage()

        # Bestimmung der maximalen analogen Ausgangsspannung
        self.max_analog_voltage = max(analog_voltage_list)
        print("max analog voltage ", self.max_analog_voltage)

        return self
    

    def calculate_power(self, offset_voltage, eff_voltage = 230):
        # Berechnung der Wirkleistung
        max_current = 10 * abs(self.max_analog_voltage - offset_voltage)
        eff_current = (1 / math.sqrt(2)) * max_current
        power = round(eff_current * eff_voltage, 1)

        print("max current: ", max_current)
        print("real power: ", power, "\n")

        return power




# Initialisierung der elektronischen Bauteile

GPIO.setmode(GPIO.BCM)

bcm = {"button" : [GPIO.IN, 5],
       "relay" : [GPIO.OUT, 9],
       "led" : [GPIO.OUT, 13]}

for i in bcm:
    GPIO.setup(bcm[i][1], bcm[i][0])
    print("bcm", bcm[i][1], "initialized")
print("\n")

button = bcm["button"]
relay = bcm["relay"]
led = bcm["led"]

i2c = busio.I2C(3, 2)
ads = ADS.ADS1115(i2c)
current_sens = AnalogIn(ads, ADS.P0)

relay_config = [1, 0]