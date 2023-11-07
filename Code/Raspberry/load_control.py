import time

def check_timer(duration, start_time):
    if (time.time() - start_time) >= duration:
        return True
    else:
        return False

class LoadControl:
    def __init__(self, p_grid, p_device, pv_mode, relay_config, relay_state):
        self.p_grid = p_grid
        self.p_device = p_device
        self.pv_mode = pv_mode
        self.relay_config = relay_config
        self.relay_state = relay_state

        self.mode_1 = "max_self_consumption"
        self.mode_2 = "no_power_purchase"
        self.mode_3 = "always_on"
        self.mode_4 = "load_schedule"

    def set_preference(self, car_mode, car_p, preference):
        if car_mode == "Eco" and preference == "car":
            self.p_grid = self.p_grid - car_p

        return self

    def set_delay(self, delay, delay_counter_start, delay_on):
        max_self_consumption = self.p_grid > self.p_device and self.pv_mode == self.mode_1 and self.relay_state == self.relay_config[1]
        only_self_consumption = self.p_grid <= (-1 * self.p_device) and self.pv_mode == self.mode_2 and self.relay_state == self.relay_config[0]
        delay_condition = max_self_consumption or only_self_consumption
        
        if delay_condition and delay_on == False:
            delay_on = True
            print("delay start")
        elif delay_on:
            print(time.time() - delay_counter_start)
            if check_timer(delay, delay_counter_start):
                print("delay end")
                delay_on = False

        return delay_on
            
    def update_relay(self):
        print("p_grid", self.p_grid)
        if self.pv_mode == self.mode_1:
            if self.relay_state == self.relay_config[0]:
                if self.p_grid <= 0: return self.relay_config[1]
                else: return self.relay_config[0]
            elif self.relay_state == self.relay_config[1]:
                if self.p_grid > self.p_device: return self.relay_config[0]
                else: return self.relay_config[1]
            else: return self.relay_config[0]

        elif self.pv_mode == self.mode_2:
            if self.relay_state == self.relay_config[0]:
                if self.p_grid <= (-1 * self.p_device): return self.relay_config[1]
                else: return self.relay_config[0]
            elif self.relay_state == self.relay_config[1]:
                if self.p_grid >= 0: return self.relay_config[0]
                else: return self.relay_config[1]

        elif self.pv_mode == self.mode_3: return self.relay_config[1]

        elif self.pv_mode == self.mode_4:
            pass