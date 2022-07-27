import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter

# 1. Ganzen Text ohne Überschriften in einem String speichern
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
        for line in reader: 
            if line[1] != "H":
                manifesto_as_str = manifesto_as_str + " " + line[0]
            elif line[1] == "H":
                continue 
    return manifesto_as_str

# 2. Tokenisieren mit spaCy 
def lemmatize(manifesto_as_str):
    """ A function that lemmatizes the tokens in a given file using spaCy's German package.

    Parameters
    ----------
    manifesto_as_str: string obtained from csv file, excluding paragraphs

    Return
    ------
    manifesto_lemmatized: string lemmatized into lowercase words
    """
    nlp = spacy.load("de_core_news_sm")
    manifesto_processed = nlp(manifesto_as_str)
    manifesto_lemmatized = []
    for token in manifesto_processed:
        manifesto_lemmatized.append(token.lemma_.lower())
    return manifesto_lemmatized

# 3. Stoppwörter und Interpunktion entfernen
STOP_WORDS.add("das")
STOP_WORDS.add("die")
STOP_WORDS.add("wir")
STOP_WORDS.add("für")

punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", " –"]

def remove_stopwords_and_punct(manifesto_tokenized):
    """ A function that removes stop words and punctuation.

    Parameters
    ----------
    manifesto_lemmatized: list with lowercase lemmas for each token

    Return
    ------
    manifesto_clean: list of lemmas excluding stop words and punctuation
    """
    manifesto_clean = []
    for token in manifesto_tokenized:
        if token in STOP_WORDS:
            continue
        if token in punctuation:
            continue
        else:
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


def pipeline(filename):
    """ A function that takes the filename of a csv file and performs the operations previously introduced as a pipeline.

    Parameters
    ----------
    filename: name of the file in csv format

    Return
    ------
    5 most common words occuring in the document and their frequency
    """ 
    return most_frequent(remove_stopwords_and_punct(lemmatize(csv_to_string(filename))))

filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']
for filename in filenames:
    print(pipeline(filename))

print(pipeline('41953_202109.csv'))