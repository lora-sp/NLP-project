import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter

# 1. Frequency Methode
# Gesamten Text in einem String speichern, diesen tokenisieren, Stopwörter entfernen und die häufigsten Lemmata ausgeben lassen
def csv_to_string(filename):
    """ A function that reads a csv file and saves it in a string, excluding paragraphs.

    Parameters
    ----------
    filename: name of the file in csv format

    Return
    ------
    manifesto_as_str: string containing text chunks excluding headers ("H")
    """
    with open(filename, newline='', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        manifesto_as_str = ""
        next(reader)
        for line in reader: 
            if line[1] != "H":
                manifesto_as_str = manifesto_as_str + " " + line[0]
            elif line[1] == "H":
                continue 
    return manifesto_as_str

custom_stop_words = ["der", "die", "das", "für", "grüne", "linke", "afd", "spd", "cdu", "csu", "fdp", "Für"]

def tokenize(manifesto_as_str):
    """ A function that tokenizes the tokens in a given file using spaCy's German model.

    Parameters
    ----------
    manifesto_as_str: string obtained from csv file, excluding paragraphs

    Return
    ------
    manifesto_tokenized: string tokenized into lowercase words
    """
    nlp = spacy.load("de_core_news_sm")
    manifesto_processed = nlp(manifesto_as_str)
    manifesto_tokenized = []
    for token in manifesto_tokenized:
        if token.text not in STOP_WORDS:
            if token.pos == "ADP":
                custom_stop_words.append(token.text)
            elif token.pos == "PUNCT":
                custom_stop_words.append(token.text)
            elif token.pos == "NUM":
                custom_stop_words.append(token.text)
    for token in manifesto_processed:
        manifesto_tokenized.append(token.text.lower())
    return manifesto_tokenized

#punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", " –"]
STOP_WORDS.update(custom_stop_words)
#STOP_WORDS.update(punctuation)

def remove_stopwords(manifesto_tokenized):
    """ A function that removes stop words and punctuation.

    Parameters
    ----------
    manifesto_tokenized: list with lowercase tokens for each token

    Return
    ------
    manifesto_clean: list of lemmas excluding stop words and punctuation
    """
    manifesto_clean = []
    for token in manifesto_tokenized:
        if token not in STOP_WORDS:
            manifesto_clean.append(token) 
    return manifesto_clean


def most_frequent(manifesto_clean):
    """ A function that counts the occurrences of each word and prints the 5 most frequent words.

    Parameters
    ----------
    manifesto_clean: list with lowercase tokens

    Return
    ------
    5 most common words occuring in the document and their frequency
    """   
    c = Counter(manifesto_clean)
    return c.most_common(5)

def freq_pipeline(filename):
    """ A function that takes the filename of a csv file and performs the operations previously introduced as a pipeline.

    Parameters
    ----------
    filename: name of the file in csv format

    Return
    ------
    5 most common words occuring in the document and their frequency
    """ 
    return most_frequent(remove_stopwords(tokenize(csv_to_string(filename))))

filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']
for filename in filenames:
    print(freq_pipeline(filename))

print(freq_pipeline('41953_202109.csv'))

# bei frequency approach: Häufigste Dep-Rel "wir fordern/sagen/wollen" etc # EIGENNAMEN? geopolitische sachen

# 3. tf-idf approach TF-IDF im Vergleich zu allen Wahlprogrammen


