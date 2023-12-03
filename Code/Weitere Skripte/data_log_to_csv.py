
# Import der benötigten Bibliotheken
import json
import csv


log_data_file_name = "data_log (18.11.2023-19.11.2023)"

log_data_file = open(log_data_file_name + ".json", "r")
log_data_json = log_data_file.read()
log_data_dict = json.loads(log_data_json)

log_data_csv = open(log_data_file_name + ".csv", "w", newline = "")
header = ["time", "pv_mode", "battery_fully_charged", "p_grid", "relay_state", "p_device", "energy_flow"]

writer = csv.writer(log_data_csv)
writer.writerow(header)


# Extrahierung der Daten aus der JSON-Datei und Übertragung in die CSV-Datei
for day in log_data_dict:
    for time in log_data_dict[day]:
        data_list = []
        data_list.append(time)

        for device in log_data_dict[day][time]:
            for data in log_data_dict[day][time][device]:
                if data in header:
                    data_value = log_data_dict[day][time][device][data]
                    if type(data_value) is dict:
                        data_value = data_value[list(data_value.keys())[0]]
                    
                    data_list.append(data_value)
        print(data_list)
        writer.writerow(data_list)

log_data_csv.close()