# NLP Project: Main Topic Extraction
Dieses Repository enthält den Programmcode zu der Projektarbeit im Rahmen des Kurses "Advanced NLP with Python" zum Thema "Main Topic Extraction anhand deutschsprachiger Wahlprogramme". 


#### Inhaltsverzeichnis
- [Datensatz](#datensatz)
- [Installation](#installation)
- [Ausführung](#ausführung)


## Datensatz
Der Datensatz wurde dem [Manifesto Project](https://visuals.manifesto-project.wzb.eu/mpdb-shiny/cmp_dashboard_dataset/) entnommen. Dabei wurde zur Eingrenzung als Jahr 2021 und als Land Deutschland ausgewählt. Die sechs übrigen Dateien wurden im annotierten csv-Dateiformat heruntergeladen. 
Als Datenbeispiel können die zufällig generierten und bereinigten Evaluationsausschnitte im Unterordner "evaluation" angesehen werden. Diese tragen die Namen eval_"Parteiname".json. 

## Installation
Alle Dateien im Ordner "project" müssen heruntergeladen werden. 
Für diese Arbeit wurde die Python-Version 3.10.5 benutzt.
Mit `pip install -r requirements.txt` werden alle benötigten Bibliotheken installiert. Die Versionen der Bibliotheken sind jeweils dort aufgeführt. 

## Ausführung
Zunächst wird die Datei "preprocessing.py" ausgeführt. Dort werden die Daten auf zwei verschiedene Arten bereinigt. In der ersten Variante der Datenbereinigung wird der gesamte Fließtext der Wahlprogramme in einem String gespeichert. In der zweiten Variante wird der Text in Absätze geteilt und in einer Liste von Strings gespeichert. Dabei werden die Überschriften nicht miteinbezogen. Zur Bereinigung wird jeweils der Text aus der ersten Spalte der csv-Datei gespeichert, woraufhin die Wörter lemmatisiert und Stoppwörter entfernt werden. 

### Häufigste Wörter pro Text
Hierbei wird die Datei "string_frequency.py" benötigt. Dort werden die im vorherigen Schritt bereinigten Daten (Variante 1) weiterverarbeitet. Dabei sollen die häufigsten 50 Wörter in einer json-Datei gespeichert werden. Um dasselbe Ziel auf den Evaluationsausschnitten zu erreichen, wurde die Funktion entsprechend modifiziert, um anstatt die häufigsten 50 nur die häufigsten 3 Wörter auszugeben. 

### TF-IDF
Hierbei wird die Datei "tf_idf.py" benötigt. Dort werden die im vorherigen Schritt bereinigten Daten (Variante 1) weiterverarbeitet. Dabei sollen die Wörter mit den 20 höchsten TF-IDF-Scores in einer json-Datei gespeichert werden. Um dasselbe Ziel auf den Evaluationsausschnitten zu erreichen, wurde die Funktion entsprechend modifiziert, um anstatt die Wörter mit den höchsten 20 nur die Wörter mit den höchsten 3 TF-IDF-Scores auszugeben. 

### Named Entity Recognition
Hierbei wird die Datei "named_entity_recognition.py" benötigt. Dort werden die im vorherigen Schritt bereinigten Daten (Variante 1) weiterverarbeitet. Dabei sollen die häufigsten 50 Eigennamen in einer json-Datei gespeichert werden. Um dasselbe Ziel auf den Evaluationsausschnitten zu erreichen, wurde die Funktion entsprechend modifiziert, um anstatt die häufigsten 50 nur die häufigsten 3 Eigennamen auszugeben. 


### Häufigste Wörter pro Abschnitt
Hierbei wird die Datei "paragraph_frequency.py" benötigt. Dort werden die im vorherigen Schritt bereinigten Daten weiterverarbeitet. Dabei sollen die häufigsten 3 Wörter pro Abschnitt in einer json-Datei gespeichert werden. Um dasselbe Ziel auf den Evaluationsausschnitten zu erreichen, wurde die Funktion entsprechend modifiziert, um anstatt die häufigsten 3 nur das eine häufigste Wort pro Abschnitt auszugeben. 

