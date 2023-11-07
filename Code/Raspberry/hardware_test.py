import RPi.GPIO as GPIO
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os
import csv

GPIO.setmode(GPIO.BCM)

# Initialisierung der GPIO-Pins
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.OUT)

# Initialisierung des I2C-Bus
i2c = busio.I2C(3, 2, frequency=100000)
# Erstellen des ADC-Objekts über den I2C-Bus
ads = ADS.ADS1115(i2c)
# Eingang auf Kanal 0 erstellen
chan0 = AnalogIn(ads, ADS.P0)

# Initialisierung der csv-Datei
f = open("Diagramm_Stromsensor_I-U.csv", "w")
header = ["Stromstärke [A]", "Analoge Ausgangsspannung [V]"]
writer = csv.writer(f)
writer.writerow(header)

# Relais schliessen
GPIO.output(23, True)

current = 0

while True:
    if GPIO.input(24) == True:
        analog_voltage = chan0.voltage
        time.sleep(1)
        if GPIO.input(24) == False:
            # Daten-Sicherung in der csv-Datei
            writer.writerow([current, analog_voltage])
            print("chan0 voltage: ", analog_voltage)
            print("current: ", current)
            current += 0.1
        else:
            # LED bleibt an bis der Raspberry komplett heruntergefahren ist
            f.close()
            GPIO.output(25, True)
            os.system("sudo poweroff")