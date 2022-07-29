import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter


# Paragraph Approach (stop words + paragraph length)
# Text in Absätze teilen, die längeren Absätze analysieren und dort die häufigsten Worte ausgeben lassen

def csv_to_paragraphs(filename):
    """ A function that reads a csv file and separates it into paragraphs.

    Parameters
    ----------
    filename: name of the file in csv format

    Return
    ------
    manifesto_paragraphs: a list of paragraphs (text chunks separated by headers ("H"))
    """
    with open(filename, newline='', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        current_paragraph = ""
        manifesto_paragraphs = []
        next(reader)
        for line in reader: 
            if line[1] != "H":
                current_paragraph = current_paragraph + " " + line[0]
            elif line[1] == "H":
                manifesto_paragraphs.append(current_paragraph)
                current_paragraph = ""
    return manifesto_paragraphs

long_paragraphs = []
for paragraph in paragraphs:
    if len(paragraph) < 2000:
        continue
    else:
        long_paragraphs.append(paragraph)
print(len(long_paragraphs)) #268
