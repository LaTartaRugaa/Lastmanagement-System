# Entwicklung eines Lastmanagementsystems zur optimierten Nutzung von Photovoltaik-Energie
Maturitätsarbeit 2023 / 2024  
Kantonsschule Rychenberg  
Michael Enderli

## Informationen
### [Diagramme](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Diagramme)
Hier finden Sie die im Rahmen dieser Maturitätsarbeit entstandenen Diagramme mit den dazugehörigen Datensätzen.  


### [Code](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code)

#### [Lastmanagement-App](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code/Lastmanagement-App)
Dieser Ordner beinhaltet den Code für die Lastmanagement-App.
#### [Raspberry Pi Zero W](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code/Raspberry%20Pi%20Zero%20W)
Der hier vorhandene Code wird vom Raspberry Pi Zero W ausgeführt.
#### [Weitere Skripte](https://github.com/LaTartaRugaa/Lastmanagement-System/tree/main/Code/Weitere%20Skripte)
Das Skript [hardware_test.py](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Code/Weitere%20Skripte/hardware_test.py) wurde beim Funktionstest ausgeführt und speicherte die Messwerte in einer CSV-Datei ab. Aus diesen Messwerten wurde das Diagramm [Kennlinie des Stromsensors Debo Sens 20 A.xlsx](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Diagramme/Kennlinie%20des%20Stromsensors%20Debo%20Sens%2020%20A.xlsx) erstellt.  
Damit aus den Daten in der Log-Datei [data_log (18.11.2023 - 19.11.2023).json](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/data_log%20(18.11.2023%20-%2019.11.2023).json) die Diagramme in der Datei [Lastmanagementsystem - Aufzeichnung (18.11.2023-19.11.2023).xlsx](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Diagramme/Lastmanagementsystem%20-%20Aufzeichnung%20(18.11.2023-19.11.2023).xlsx) erstellt werden konnten, wurde das Python-Skript [data_log_to_csv.py](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Code/Weitere%20Skripte/data_log_to_csv.py) entwickelt. Mit diesem Skript wurden die jeweiligen Datenpunkte aus der JSON-Datei extrahiert und in eine CSV-Datei übertragen.

## Anmerkungen
Da die Datei credentials.py, die sich sowohl im Ordner [Lastmanagement-App](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Code/Lastmanagement-App/credentials.py) als auch im Ordner [Raspberry Pi Zero W](https://github.com/LaTartaRugaa/Lastmanagement-System/blob/main/Code/Raspberry%20Pi%20Zero%20W/credentials.py) befindet, vertrauliche Informationen enthält, wurden diese im Github-Repository entfernt und durch leere Strings ersetzt.
