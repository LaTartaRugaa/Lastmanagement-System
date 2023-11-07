from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder
from kivy.clock import Clock

from threading import Thread

from github_requests import Github
import credentials


Builder.load_file("elements.kv")
github = Github(credentials.github_username, credentials.github_repository, credentials.github_file_path, credentials.github_token)

battery_fully_charged_text = "Der Akku ist vollgeladen"
p_device_text = "Aktuelle Leistung Lastmanagement-System: "
device_on_text = "Abschalten"
device_off_text = "Abgeschaltet"
standby_on_text = "Standby On"
standby_off_text = "Standby Off"

modes = 3
standard_color = [0.3, 0.3, 0.3, 1]
active_mode_color = [0, 0.7, 0, 1]
turned_off_color = [1, 0.2, 0.2, 0.8]


class LabelText:
    def __init__(self, base_url):
        self.base_url = base_url

    def bool_to_text(self, sub_key, text_true, text_false = ""):
        if self.base_url[sub_key] == True:
            return text_true
        else:
            return text_false
    
    def int_to_text(self, sub_key, text):
        return (text + str(self.base_url[sub_key]))


class UI(MDFloatLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pv_mode_buttons =  {"max_self_consumption" : self.ids.max_self_consumption,
                                 "no_power_purchase" : self.ids.no_power_purchase,
                                 "always_on" : self.ids.always_on}

        self.device_state_buttons = {"btn_4" : self.ids.btn_4,
                                     "btn_5" : self.ids.btn_5}
        

    def update(self, sub_key = None, updated_data_mobile = None, *args):
        if updated_data_mobile == None:
            request_data = github.get_data("content")
            l_pi = LabelText(request_data["raspberry"])

            self.ids.battery_level.text = l_pi.bool_to_text("battery_fully_charged", battery_fully_charged_text)
            self.ids.p_device.text = l_pi.int_to_text("p_device", p_device_text)

            device_state = l_pi.bool_to_text("device_on", device_on_text, device_off_text)

            if device_state == device_off_text:
                self.ids.btn_4.text = device_off_text
                self.ids.btn_4.md_bg_color = turned_off_color
            

            elif device_state == device_on_text:
                self.ids.btn_4.text = device_on_text
                if request_data["mobile"]["device_on"] == False:
                    self.ids.btn_4.md_bg_color = turned_off_color
                elif request_data["mobile"]["device_on"] == True:
                    self.ids.btn_4.md_bg_color = standard_color
            


            standby_text = l_pi.bool_to_text("standby", standby_on_text, standby_off_text)

            if standby_text == standby_off_text:
                self.ids.btn_5.text = standby_off_text
                if request_data["mobile"]["standby"] == False:
                    self.ids.btn_5.md_bg_color = standard_color
                elif request_data["mobile"]["standby"] == True:
                    self.ids.btn_5.md_bg_color = active_mode_color


            elif standby_text == standby_on_text:
                self.ids.btn_5.text = standby_on_text
                if request_data["mobile"]["standby"] == False:
                    self.ids.btn_5.md_bg_color = standard_color
                if request_data["mobile"]["standby"] == True:
                    self.ids.btn_5.md_bg_color = active_mode_color


            current_pv_mode = request_data["mobile"]["pv_mode"]

            for pv_mode in self.pv_mode_buttons:
                if current_pv_mode == pv_mode:
                    self.pv_mode_buttons[pv_mode].md_bg_color = active_mode_color
                else:
                    self.pv_mode_buttons[pv_mode].md_bg_color = standard_color
                    

        else:
            data_mobile = github.get_data("content")["mobile"]
            data_mobile[sub_key] = updated_data_mobile
            github.put_data(data_mobile, "mobile")

    def start_update_thread(self, sub_key = None, updated_data_mobile = None):
        Thread(target = self.update, args = (sub_key, updated_data_mobile)).start()
    

    def set_mode(self, id):
        for btn in self.pv_mode_buttons:
            if btn == id:
                if self.pv_mode_buttons[id].md_bg_color != active_mode_color:
                    self.pv_mode_buttons[btn].md_bg_color = active_mode_color
                    self.start_update_thread("pv_mode", id)
            else:
                self.pv_mode_buttons[btn].md_bg_color = standard_color

        


    def set_device_state(self):
        previous_color = self.ids.btn_4.md_bg_color

        if previous_color == standard_color:
            self.start_update_thread("device_on", False)
            self.ids.btn_4.md_bg_color = turned_off_color

    def set_standby(self):
        previous_color = self.ids.btn_5.md_bg_color
        previous_text = self.ids.btn_5.text
        if previous_color == standard_color and previous_text == standby_off_text:
            self.start_update_thread("standby", True)
            self.ids.btn_5.md_bg_color = active_mode_color

        elif previous_color == active_mode_color and previous_text == standby_on_text:
            self.start_update_thread("standby", False)
            self.ids.btn_5.md_bg_color = standard_color

class App(MDApp):
    def build(self):

        self.theme_cls.theme_style = "Light"
        ui = UI()
        ui.update()
        Clock.schedule_interval(ui.start_update_thread, 5)
        
        return ui
App().run()