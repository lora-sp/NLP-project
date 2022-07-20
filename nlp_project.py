import spacy
import csv

# Wahlprogramm als csv-Datei öffnen und in einem String speichern
with open('41113_202109.csv', newline='', encoding='utf8') as csv_file:
    reader = csv.reader(csv_file)
    manifesto_as_str = ""
    for line in reader:
        manifesto_as_str = manifesto_as_str + " " + line[0]
print(manifesto_as_str)

# 1. Den Text in Absätze teilen
## da wo der cmp code "H" ist sind Überschriften, also vorher und nachher schauen
with open('41113_202109.csv', newline='', encoding='utf8') as csv_file:
    reader = csv.reader(csv_file)
    current_paragraph = ""
    paragraphs = []
    for line in reader: 
        if line[1] != "H":
            current_paragraph = current_paragraph + " " + line[0]
        elif line[1] == "H":
            paragraphs.append(current_paragraph)
            current_paragraph = ""
print(paragraphs)
# FEINSCHLIFF: 1. Zelle weg!

# 2. Tokenisieren mit spaCy
# das spaCy-Package für Deutsch laden (?)
# nlp = spacy.load("de_core_news_sm")



    



      








