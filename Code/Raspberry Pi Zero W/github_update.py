# Import der benötigten Bibliotheken
import RPi.GPIO as GPIO
import time
import credentials
import components as comp
from api import *
from load_control import *


# Instanzen der Klassen "Github" und "Wattpilot" erstellen
github_db = Github(credentials.github_username, credentials.github_repository, credentials.github_db_file_path, credentials.github_token)
github_log_data = Github(credentials.github_username, credentials.github_repository, credentials.github_log_file_path, credentials.github_token)
wattpilot = Wattpilot(credentials.wattpilot_ip, credentials.wattpilot_password)

mb = "mobile"
pi = "raspberry"


# Stromsensor initialisieren
current_sensor_period = 0.1
current_sensor = comp.CurrentSensor(current_sensor_period)
offset_voltage = current_sensor.calibrate_offset_voltage(forced = True)


# Parameter initialisieren
local_parameters = {"relay_state" : GPIO.input(comp.relay[1]),
                    "battery_fully_charged_check" : False,
                    "delay_on" : False,
                    "device_on" : True,
                    "update_interval" : 0,
                    "update_interval_start" : 0,
                    "wattpilot_interval_start" : 0,
                    "log_update_interval_start" : 0,
                    "delay_start" : 0,
                    "p_device" : 0,
                    "log_time" : time.localtime().tm_min}
                    

car_values = {"car_mode" : "mode",
              "car_p" : "power",
              "car_battery_level" : "energyCounterSinceStart"}




class GithubUpdate:
    def __init__(self):
        self.github_request = github_db.get_data("content")
        self.db_mb = self.github_request[mb]
        self.db_pi = self.github_request[pi]

        self.db_pi["device_on"] = True
        self.db_pi["relay_config"] = comp.relay_config
        self.db_pi["p_grid"] = Fronius().get_data("P_Grid")


    def update_wattpilot_data(self):
        # Bei Ablauf des Timers werden die Wattpilot-Daten aktualisiert.
        if check_timer(self.db_mb["wattpilot_interval"] * self.db_mb["update_interval"], local_parameters["wattpilot_interval_start"]):
            self.db_pi["car_connected"] = wattpilot.get_data("carConnected")
            if self.db_pi["car_connected"] != "no car":
                for value in car_values:
                    self.db_pi[value] = wattpilot.get_data(car_values[value])

            local_parameters["wattpilot_interval_start"] = time.time()
            
        
    def update_load_control(self):
        load_control = LoadControl(self.db_pi["p_grid"], local_parameters["p_device"], self.db_mb["pv_mode"], comp.relay_config, local_parameters["relay_state"])
        load_control = load_control.set_preference(self.db_pi["car_mode"], self.db_pi["car_p"], self.db_mb["preference"])
        
        # Überprüfen, ob Timer aktiviert ist
        delay_on = load_control.set_delay(self.db_mb["delay"] * self.db_mb["update_interval"], local_parameters["delay_start"], local_parameters["delay_on"])
        local_parameters["delay_on"] = delay_on

        # Ausführung der Lastregelung bei Erfüllung der Bedingungen
        if local_parameters["delay_on"] == local_parameters["battery_fully_charged_check"] == self.db_pi["standby"] == self.db_mb["standby"] == False:
            GPIO.output(comp.relay[1], load_control.update_relay())
            print("relay_update -- relay state: ", GPIO.input(comp.relay[1]))

            local_parameters["delay_start"] = time.time()

            
    def update_standby_state(self):
        # Aktualisierung des Standby-Status
        if self.db_mb["standby"] == True:
            self.db_pi["standby"] = True
            print("db_mb standby true")
        elif self.db_pi["standby"] == True:
            self.db_pi["standby"] = False
            local_parameters["battery_fully_charged_check"] = False
        

    def update_battery_state(self):
        # Aktualisierung des Batteriestatus und des Standby-Status

        if self.db_pi["p_device"] >= self.db_mb["p_standby_range"] and self.db_mb["standby"] == False:
            self.db_pi["battery_fully_charged"] = local_parameters["battery_fully_charged_check"] = False

        elif local_parameters["battery_fully_charged_check"] == True:
            GPIO.output(comp.relay[1], comp.relay_config[0])
            self.db_pi["battery_fully_charged"] = True
            self.db_pi["standby"] = True
            self.db_mb["standby"] = True
            github_db.put_data(True, "mobile", sub_key = "standby")
            print("standby true")

            local_parameters["battery_fully_charged_check"] = False
            
        elif local_parameters["battery_fully_charged_check"] == False:
            local_parameters["battery_fully_charged_check"] = True
            print("battery_fully_charged_check: True")
    

    def update_log(self):
        # Aktualisierung der Log-Datei im Github-Repository
        current_time_min = time.time()
        current_time = time.localtime(current_time_min)
        update = False

        if current_time.tm_min >= local_parameters["log_time"]:
            print("log", local_parameters["log_time"])
            local_parameters["log_time"] = current_time.tm_min + self.db_mb["log_interval"]
            update = True
        elif current_time.tm_min < self.db_mb["log_interval"] and local_parameters["log_time"] == (60 or 0):
            print("log 0s", local_parameters["log_time"])
            local_parameters["log_time"] = self.db_mb["log_interval"]
            update = True

        if update == True:
            date_key = "{}.{}.{}".format(current_time.tm_mday, current_time.tm_mon, current_time.tm_year)
            time_key = "{}:{}".format(current_time.tm_hour, current_time.tm_min)
            self.db_pi["p_grid"] = Fronius().get_data("P_Grid")
            github_log_data.put_data(self.github_request, date_key, time_key)


    def update_interval(self):
        # Aktualisierung des Update-Intervalls
        if self.db_pi["standby"] == self.db_mb["standby"] == True:
            GPIO.output(comp.relay[1], comp.relay_config[0])
            local_parameters["update_interval"] = self.db_mb["update_interval"] * self.db_mb["standby_interval"]
            print("standby", "\n")
        elif local_parameters["battery_fully_charged_check"] == True:
            local_parameters["update_interval"] = self.db_mb["update_interval"] * self.db_mb["standby_interval"]
        else:
            local_parameters["update_interval"] = self.db_mb["update_interval"]

    
    def update_energy_flow(self):
        # Aktualisierung des Energieflusses
        t = time.localtime()
        current_date = "{}.{}.{}".format(t.tm_mday, t.tm_mon, t.tm_year)

        if list(self.db_pi["energy_flow"].keys())[0] == current_date:
            duration = time.time() - local_parameters["update_interval_start"]
            energy_flow = self.db_pi["p_device"] * duration
            self.db_pi["energy_flow"][current_date] += energy_flow
            print("energy_flow_duration: ", duration)
        else:
            self.db_pi["energy_flow"] = {current_date : 0}