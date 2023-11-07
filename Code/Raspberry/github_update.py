# Import der benötigten Bibliotheken
import RPi.GPIO as GPIO
import time

import credentials
import components_setup as comp
from api import *
from load_control import *
#------------------------------




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
                    "delay_start" : 0,
                    "p_device" : 0,
                    "p_device_last_log" : time.time(),
                    "p_device_log" : 0,
                    "log_time" : 0}

car_values = {"car_mode" : "mode",
              "car_p" : "power",
              "car_battery_level" : "energyCounterSinceStart"}


#
class GithubUpdate:
    def __init__(self):
        self.db_mb = github_db.get_data("content")[mb]
        self.db_pi = github_db.get_data("content")[pi]

        self.db_pi["device_on"] = True
        self.db_pi["relay_config"] = comp.relay_config
        self.db_pi["p_grid"] = Fronius().get_data("P_Grid")

    def update_wattpilot_data(self):
        if check_timer(self.db_mb["wattpilot_interval"] * self.db_mb["update_interval"], local_parameters["wattpilot_interval_start"]):
            self.db_pi["car_connected"] = wattpilot.get_data("carConnected")
            if self.db_pi["car_connected"] != "no car":
                for value in car_values:
                    self.db_pi[value] = wattpilot.get_data(car_values[value])

            local_parameters["wattpilot_interval_start"] = time.time()
            
           
        
    def update_load_control(self):
        load_control = LoadControl(self.db_pi["p_grid"], local_parameters["p_device"], self.db_mb["pv_mode"], comp.relay_config, local_parameters["relay_state"])
        load_control = load_control.set_preference(self.db_pi["car_mode"], self.db_pi["car_p"], self.db_mb["preference"])
        delay_on = load_control.set_delay(self.db_mb["delay"] * self.db_mb["update_interval"], local_parameters["delay_start"], local_parameters["delay_on"])
        
        print(local_parameters["delay_on"], local_parameters["battery_fully_charged_check"], self.db_pi["standby"], self.db_mb["standby"])

        local_parameters["delay_on"] = delay_on
        
        if local_parameters["delay_on"] == local_parameters["battery_fully_charged_check"] == self.db_pi["standby"] == self.db_mb["standby"] == False:
            GPIO.output(comp.relay[1], load_control.update_relay())
            print("relay_update -- relay state: ", GPIO.input(comp.relay[1]))

            local_parameters["delay_start"] = time.time()

            

    def update_standby_state(self):
        if self.db_mb["standby"] == True:
            self.db_pi["standby"] = True
            print("db_mb standby true")
        elif self.db_pi["standby"] == True:
            self.db_pi["standby"] = False
            local_parameters["battery_fully_charged_check"] = False
        
    def update_battery_state(self):
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
            print("battery fully charged true")
    
    def update_log(self):
        local_parameters["p_device_log"] += local_parameters["p_device"] * (time.time() - local_parameters["p_device_last_log"]) / 3600
        
        print("p_device_log", local_parameters["p_device_log"])

        t = time.localtime()
        if t.tm_min >= local_parameters["log_time"]:
            if t.tm_min >= 55:
                local_parameters["log_time"] = 5
            else:
                while True:
                    local_parameters["log_time"] += 5
                    if local_parameters["log_time"] > t.tm_min:
                        break
            print(local_parameters["log_time"], t.tm_min)

            main_key = "{}.{}.{}".format(t.tm_mday, t.tm_mon, t.tm_year)
            sub_key = "{}:{}".format(t.tm_hour, t.tm_min)
            github_log_data.put_data([local_parameters["p_device_log"], self.db_pi["standby"], self.db_pi["relay_state"], self.db_pi["battery_fully_charged"], self.db_mb["pv_mode"]], main_key, sub_key)

            local_parameters["p_device_log"] = 0

        local_parameters["p_device_last_log"] = time.time()
    
    def update_interval(self):
        if self.db_pi["standby"] == self.db_mb["standby"] == True:
            GPIO.output(comp.relay[1], comp.relay_config[0])
            local_parameters["update_interval"] = self.db_mb["update_interval"] * self.db_mb["standby_interval"]
            print("standby", "\n")
        elif local_parameters["battery_fully_charged_check"] == True:
            local_parameters["update_interval"] = self.db_mb["update_interval"] * self.db_mb["standby_interval"]
        else:
            local_parameters["update_interval"] = self.db_mb["update_interval"]