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
    manifesto_paragraphs: a list of strings (text chunks separated by headers ("H"))
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
        for paragraph in manifesto_paragraphs:
            if len(paragraph) < 3000:
                manifesto_paragraphs.remove(paragraph)
    return manifesto_paragraphs

def lemmatize(manifesto_paragraphs):
    """ A function that lemmatizes the tokens in a given file using spaCy's German model.

    Parameters
    ----------
    manifesto_parargaphs: list of strings (paragraphs)

    Return
    ------
    paragraphs_lemmatized: list of paragraphs consisting of lists of lowercase, lemmatized words
    """
    nlp = spacy.load("de_core_news_sm")
    current_paragraph_lemmatized = []
    paragraphs_lemmatized = []
    for paragraph in manifesto_paragraphs:
        manifesto_processed = nlp(paragraph)
        for token in manifesto_processed:
            current_paragraph_lemmatized.append(token.lemma_.lower())

        paragraphs_lemmatized.append(current_paragraph_lemmatized)
        current_manifesto_lemmatized = []

    return paragraphs_lemmatized

def remove_stopwords(paragraphs_lemmatized):
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
    
    return manifesto_clean

#STOP WORDS aktualisieren

def most_frequent(manifesto_clean):
    """ A function that counts the occurrences of each word per paragraph and prints the 3 most frequent words.

    Parameters
    ----------
    manifesto_clean: list of paragraphs consisting of lists of lowercase lemmas, excluding stop words

    Return
    ------
    3 most common words occuring in each paragraph and their frequency
    """   
    c = Counter(paragraph)
    most_common = []
    for paragraph in manifesto_clean:
        #current_most_common = []
        #current_most_common.append(c.most_common(3))
        most_common.append(c.most_common(3))
    return most_common


print(most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs('41113_202109.csv')))))