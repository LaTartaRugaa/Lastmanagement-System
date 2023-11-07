# Import der benötigten Bibliotheken
import RPi.GPIO as GPIO
import time
import os

import components_setup as comp
from github_update import *
from api import *
from load_control import *
#------------------------------




while local_parameters["device_on"] == True:
    if check_timer(local_parameters["update_interval"], local_parameters["update_interval_start"]):
        local_parameters["update_interval_start"] = time.time()


        github_update = GithubUpdate()
        github_update.update_wattpilot_data()
        github_update.update_standby_state()
        
        github_update.db_pi["p_grid"] = input("p_grid")

        local_parameters["relay_state"] = github_update.db_pi["relay_state"] = GPIO.input(comp.relay[1])

        if local_parameters["relay_state"] == comp.relay_config[0]:
            offset_voltage = current_sensor.calibrate_offset_voltage()
            github_update.db_pi["p_device"] = 0

        elif local_parameters["relay_state"] == comp.relay_config[1]:
            local_parameters["p_device"] = github_update.db_pi["p_device"] = current_sensor.get_max_voltage().calculate_power(offset_voltage)
            local_parameters["p_device"] = input("p_device")
            github_update.update_battery_state()

        print(local_parameters["p_device"])


        github_update.update_load_control()
        

            
            
        github_update.update_log()
        github_update.update_interval()

        

        github_db.put_data(github_update.db_pi, "raspberry")


    if GPIO.input(comp.button[1]) == True:
        print("button: ", GPIO.input(comp.button[1]))
        time.sleep(1)
        local_parameters["device_on"] = not GPIO.input(comp.button[1])
    elif github_update.db_mb["device_on"] == False:
        print("db_mb device off")
        local_parameters["device_on"] = False



    
GPIO.output(comp.led[1], True)


github_update.db_pi["device_on"] = False
github_update.db_pi["p_device"] = 0
github_db.put_data(github_update.db_pi, "raspberry")
github_db.put_data(True, "mobile", sub_key = "device_on")


print("shutdown")

GPIO.output(comp.led[1], False)
#os.system("sudo shutdown -h now")