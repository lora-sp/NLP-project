# NLP Project: Main Topic Extraction
Dieses Repository enthält den Programmcode zu der Projektarbeit im Rahmen des Kurses "Advanced NLP with Python" zum Thema "Main Topic Extraction anhand deutschsprachiger Wahlprogramme". 


#### Inhaltsverzeichnis
- [Datensatz](#data)
- [Installation](#installation)
- [Ausführung](#usage)


## Datensatz
Der Datensatz wurde dem [Manifesto Project](https://visuals.manifesto-project.wzb.eu/mpdb-shiny/cmp_dashboard_dataset/) entnommen. Dabei wurde zur Eingrenzung als Jahr 2021 und als Land Deutschland ausgewählt. Die sechs übrigen Dateien wurden im annotierten csv-Dateiformat heruntergeladen. 
Als Datenbeispiel können die zufällig generierten und bereinigten Evaluationsausschnitte im Unterordner "evaluation" angesehen werden. Diese tragen die Namen eval_"Parteiname".json. 

## Installation
Alle Dateien im Ordner "project" müssen heruntergeladen werden. 
Für diese Arbeit wurde die Python-Version 3.10.5 benutzt.
Mit `pip install -r requirements.txt` werden alle benötigten Bibliotheken installiert. Die Versionen der Bibliotheken sind jeweils dort aufgeführt. 

## Ausführung
Zunächst wird die Datei "preprocessing.py" ausgeführt. Dort werden die Daten auf zwei verschiedene Arten bereinigt. In der ersten Variante der Datenbereinigung wird der gesamte Fließtext der Wahlprogramme in einem String gespeichert. In der zweiten Variante wird der Text in Absätze geteilt und in einer Liste von Strings gespeichert. Dabei werden die Überschriften nicht miteinbezogen. 