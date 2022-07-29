import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter

# Pure Frequency Approach (stop words)
# Gesamten Text in einem String speichern, diesen tokenisieren, Stopwörter entfernen und die häufigsten Lemmata ausgeben lassen

def csv_to_string(filename):
    """ A function that reads a csv file and saves it in a string, excluding headers.

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
            if line[1] != "H" and line[1] != "NA":
                manifesto_as_str = manifesto_as_str + " " + line[0]
            #elif line[1] == "H" or line[1] == "NA":
            #    continue 
    return manifesto_as_str

def lemmatize(manifesto_paragraphs):
    """ A function that lemmatizes the tokens in a given file using spaCy's German model.

    Parameters
    ----------
    manifesto_as_str: string obtained from csv file, excluding paragraphs

    Return
    ------
    manifesto_lemmatized: string lemmatized into lowercase words
    """
    nlp = spacy.load("de_core_news_sm")
    manifesto_lemmatized = []
    for paragraph in manifesto_paragraphs:
        manifesto_processed = nlp(paragraph)
        for token in manifesto_processed:
            manifesto_lemmatized.append(token.lemma_.lower())

    return manifesto_lemmatized


# 3. Stoppwörter und Interpunktion entfernen
STOP_WORDS.add("das")
STOP_WORDS.add("die")
STOP_WORDS.add("wir")
STOP_WORDS.add("für")

punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", " –"]
custom_stop_words = ["der", "die", "das", "für", "grüne", "linke", "afd", "spd", "cdu", "csu", "fdp", "Für"]
STOP_WORDS.update(custom_stop_words)
STOP_WORDS.update(punctuation)


def remove_stopwords(manifesto_tokenized):
    """ A function that removes stop words.

    Parameters
    ----------
    manifesto_lemmatized: list with lowercase lemmas for each token

    Return
    ------
    manifesto_clean: list of lemmas excluding stop words
    """
    manifesto_clean = []
    for token in manifesto_tokenized:
        if token not in STOP_WORDS:
            manifesto_clean.append(token) 
    return manifesto_clean

# 4. Worthäufigkeiten zählen
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
    return most_frequent(remove_stopwords(lemmatize(csv_to_string(filename))))

filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']
for filename in filenames:
    print(freq_pipeline(filename))

print(freq_pipeline('41953_202109.csv'))