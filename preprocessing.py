import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS

punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", "–"] 
custom_stop_words = ["der", "die", "das", "grüne", "linke", "afd", "spd", "cdu", "csu", "fdp", "für", "über", "müssen", "inn", "inne", "vgl", "kapitel", "frei", "demokrat", "beziehungsweise", "anderer"]
STOP_WORDS.update(punctuation)
STOP_WORDS.update(custom_stop_words)

#######################################################################################################################
# variant 1: saving the whole manifesto into one string

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

    return manifesto_as_str

def lemmatize_str(manifesto_as_str):
    """ A function that lemmatizes the tokens in a given file using spaCy's German model.

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


def remove_stopwords_str(manifesto_lemmatized):
    """ A function that removes stop words and punctuation.

    Parameters
    ----------
    manifesto_lemmatized: list with lowercase lemmas for each token

    Return
    ------
    manifesto_clean: list of lemmas excluding stop words
    """
    manifesto_clean = []
    for lemma in manifesto_lemmatized:
        if lemma not in STOP_WORDS:
            manifesto_clean.append(lemma) 

    #manifesto_clean = ' '.join(manifesto_clean) #needed for tf-idf

    return manifesto_clean

#######################################################################################################################
# variant 2: saving the whole manifesto into a list of paragraphs in order to iterate over it


def csv_to_paragraphs(filename):
    """ A function that reads a csv file, separates it into paragraphs and saves the longest paragraphs in a string.

    Parameters
    ----------
    filename: name of the csv-file

    Return
    ------
    longest_paragraphs: a list of strings (text chunks separated by headers ("H")), representing the longest paragraphs
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
                manifesto_paragraphs.append(current_paragraph) #
                current_paragraph = ""

        longest_paragraphs = []
        for paragraph in manifesto_paragraphs:
            if len(paragraph) < 100:
                continue
            longest_paragraph = max(manifesto_paragraphs, key=len)
            longest_paragraphs.append(longest_paragraph)
            manifesto_paragraphs.remove(longest_paragraph)

        
    return  longest_paragraphs 

def lemmatize_par(longest_paragraphs):
    """ A function that lemmatizes the tokens in a given file using spaCy's German model.

    Parameters
    ----------
    longest paragraphs: list of strings (10 longest paragraphs)

    Return
    ------
    paragraphs_lemmatized: list of paragraphs consisting of lists of lowercase, lemmatized words
    """
    nlp = spacy.load("de_core_news_sm")
    paragraphs_lemmatized = []
    for paragraph in longest_paragraphs:
        paragraph_processed = nlp(paragraph)
        current_paragraph_lemmatized = []
        for token in paragraph_processed:
            current_paragraph_lemmatized.append(token.lemma_.lower())

        " ".join(current_paragraph_lemmatized)
        paragraphs_lemmatized.append(current_paragraph_lemmatized)
        current_paragraph_lemmatized = []

    return paragraphs_lemmatized


def remove_stopwords_par(paragraphs_lemmatized):
    """ A function that removes stop words for each paragraph.

    Parameters
    ----------
    paragraph_lemmatized: list of paragraphs consisting of lists of lowercase, lemmatized words

    Return
    ------
    manifesto_clean: list of paragraphs consisting of lists of lemmas excluding stop words
    """
    manifesto_clean = []
    for paragraph in paragraphs_lemmatized:
        current_paragraph_clean = []
        for lemma in paragraph:
            if lemma not in STOP_WORDS:
                current_paragraph_clean.append(lemma)

        manifesto_clean.append(current_paragraph_clean)
        current_paragraph_clean = []

    return manifesto_clean


#######################################################################################################################


filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']