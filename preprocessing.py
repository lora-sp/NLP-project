import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS

punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", "–", "%", "*"] 
custom_stop_words = ["grüne", "linke", "afd", "spd", "cdu", "csu", "fdp", "für", "über", "müssen", "inn", "inne", "vgl.", "kapitel", "frei", "demokrat", "beziehungsweise", "anderer", "vieler", "insbesondere", "dafür"]
STOP_WORDS.update(punctuation)
STOP_WORDS.update(custom_stop_words)

# variant 1: Saving the whole manifesto text into one string.

def csv_to_string(filename):
    """ A function that reads a csv file and saves the text in a string, excluding headers and additional information (marked by "H" and "NA" in the second column).

    Parameters
    ----------
    filename: str
        Name of the csv file.

    Returns
    -------
    manifesto_as_str : str
        Manifesto text without headers and additional information.
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
    """ A function that lemmatizes each token in a string using spaCy's German model.

    Parameters
    ----------
    manifesto_as_str: str
        Manifesto text without headers and additional information.

    Returns
    -------
    manifesto_lemmatized: lst of str
        Lowercase lemmatized tokens.
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
    manifesto_lemmatized: lst of str
        Lowercase lemmatized tokens.

    Returns
    -------
    manifesto_clean: lst of str
        Lowercase lemmatized tokens excluding stop words and punctuation.
    """
    manifesto_clean = []
    for lemma in manifesto_lemmatized:
        if lemma not in STOP_WORDS:
            manifesto_clean.append(lemma) 

    #manifesto_clean = ' '.join(manifesto_clean) #needed for tf-idf

    return manifesto_clean

# variant 2: Splitting the whole manifesto into a list of paragraphs in order to iterate over them.


def csv_to_paragraphs(filename):
    """ A function that reads a csv file and saves the text in a list of paragraphs, excluding headers and additional information (marked by "H" and "NA" in the second column).

    Parameters
    ----------
    filename: str
        Name of the csv file.

    Returns
    -------
    long_paragraphs: lst of str
        Manfesto text without headers and additional information, separated into paragraphs that are longer than 100 words.
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

        long_paragraphs = []
        for paragraph in manifesto_paragraphs:
            if len(paragraph) < 100:
                continue
            #long_paragraph = max(manifesto_paragraphs, key=len)
            long_paragraphs.append(paragraph)
            #manifesto_paragraphs.remove(long_paragraph)
        
    return  long_paragraphs 

def lemmatize_par(long_paragraphs):
    """ A function that lemmatizes each token in a string using spaCy's German model.

    Parameters
    ----------
    long_paragraphs: lst of str
        Manfesto text without headers and additional information, separated into paragraphs that are longer than 100 words.

    Returns
    -------
    paragraphs_lemmatized: lst of lsf of str 
        Lowercase lemmatized tokens.
    """
    nlp = spacy.load("de_core_news_sm")
    paragraphs_lemmatized = []
    for paragraph in long_paragraphs:
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
    paragraphs_lemmatized: lst of lsf of str 
        Lowercase lemmatized tokens.

    Returns
    -------
    paragraphs_clean: lst of lst of str
        Lowercase lemmatized tokens excluding stop words and punctuation.
    """
    paragraphs_clean = []
    for paragraph in paragraphs_lemmatized:
        current_paragraph_clean = []
        for lemma in paragraph:
            if lemma not in STOP_WORDS:
                current_paragraph_clean.append(lemma)

        paragraphs_clean.append(current_paragraph_clean)
        current_paragraph_clean = []

    return paragraphs_clean


filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']