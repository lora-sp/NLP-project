import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter

# 1. Den Text in Absätze teilen
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
        for line in reader: 
            if line[1] != "H":
                current_paragraph = current_paragraph + " " + line[0]
            elif line[1] == "H":
                manifesto_paragraphs.append(current_paragraph)
                current_paragraph = ""
    return manifesto_paragraphs
# SPÄTER: 1. Zelle weg!

##### maybe remove this part
paragraphs_long = []
for paragraph in paragraphs:
    if len(paragraph) < 2000:
        continue
    else:
        paragraphs_long.append(paragraph)
print(len(paragraphs_long)) #268

# 2. Lemmatisieren mit spaCy 
def lemmatize(manifesto_paragraphs):
    """ A function that lemmatizes the tokens in a given file using spaCy's German package.

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

lemmatize(csv_to_paragraphs('41113_202109.csv'))

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