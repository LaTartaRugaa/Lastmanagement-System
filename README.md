# Entwicklung eines Lastmanagementsystems zur optimierten Nutzung von Photovoltaik-Energie
Maturitätsarbeit 2023 / 2024  
Kantonsschule Rychenberg  
Michael Enderli

## Informationen
### [Diagramme](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Diagramme)
Hier finden Sie die im Rahmen dieser Maturitätsarbeit entstandenen Diagramme mit den dazugehörigen Datensätzen.  


### [Code](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code)

#### [Lastmanagement-App](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code/Lastmanagement-App)
Dieser Ordner beinhaltet den Code für die Lastmanagement-App. Allerdings fehlt zur Ausführung der App noch die Datei credentials.py. Diese beinhaltet allerdings das Access-Token zu diesem Github-Repository und wurde daher weggelassen. Um die App dennoch demonstrieren zu können, wurde ein weiteres Github-Repository mit einem separaten Access-Token erstellt.
#### [Raspberry Pi Zero W](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code/Raspberry%20Pi%20Zero%20W)
Der hier vorhandene Code wird vom Raspberry Pi Zero W ausgeführt. Hier fehlt ebenfalls die Datei credentials.py.
#### [Weitere Skripte](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code/Weitere%20Skripte)
Das Skript [hardware_test.py](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Code/Weitere%20Skripte/hardware_test.py) wurde beim Funktionstest ausgeführt und speicherte die Messwerte in einer CSV-Datei ab. Aus diesen Messwerten wurde das Diagramm [Kennlinie des Stromsensors Debo Sens 20 A.xlsx](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Diagramme/Kennlinie%20des%20Stromsensors%20Debo%20Sens%2020%20A.xlsx) erstellt.
Damit aus den Daten in der Log-Datei [data_log (18.11.2023 - 19.11.2023).json](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/data_log%20(18.11.2023%20-%2019.11.2023).json) die Diagramme in der Datei [Lastmanagementsystem - Aufzeichnung (18.11.2023-19.11.2023).xlsx](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Diagramme/Lastmanagementsystem%20-%20Aufzeichnung%20(18.11.2023-19.11.2023).xlsx) erstellt werden konnten, wurden das Python-Skript [data_log_to_csv.py](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Code/Weitere%20Skripte/data_log_to_csv.py) entwickelt. Mit diesem Skript wurden die jeweiligen Datenpunkte aus der JSON-Datei extrahiert und in eine CSV-datei übertragen.


Die Datei [data_log_to_csv.py](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Code/Weitere%20Skripte/data_log_to_csv.py) im Ordner [Weitere Skripte](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code/Weitere%20Skripte) wurde entwickelt, um die Logging-Daten aus der JSON-Datei in eine CSV-Datei zu übertragen, wodurch die Diagramme in der Datei [Lastmanagementsystem - Aufzeichnung (18.11.2023-19.11.2023).xlsx](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Diagramme/Lastmanagementsystem%20-%20Aufzeichnung%20(18.11.2023-19.11.2023).xlsx) generiert werden konnten. Die Datei [Kennlinie des Stromsensors Debo Sens 20 A.xlsx](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Diagramme/Kennlinie%20des%20Stromsensors%20Debo%20Sens%2020%20A.xlsx)
