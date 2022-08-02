import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter

# Paragraph Approach (stop words + paragraph length)
# Text in Absätze teilen, die längeren Absätze analysieren und dort die häufigsten Worte ausgeben lassen

def csv_to_paragraphs(filename):
    """ A function that reads a csv file, separates it into paragraphs and saves the 10 longest paragraphs in a string.

    Parameters
    ----------
    filename: name of the csv-file

    Return
    ------
    longest_paragraphs: a list of strings (text chunks separated by headers ("H")), representing the 10 longest paragraphs
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
        for i in range(10):
            longest_paragraph = max(manifesto_paragraphs, key=len)
            longest_paragraphs.append(longest_paragraph)
            manifesto_paragraphs.remove(longest_paragraph)

    return  longest_paragraphs 



def lemmatize(longest_paragraphs):
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
    for paragraph in manifesto_paragraphs:
        manifesto_processed = nlp(paragraph)
        current_paragraph_lemmatized = []
        for token in manifesto_processed:
            current_paragraph_lemmatized.append(token.lemma_.lower())

        paragraphs_lemmatized.append(current_paragraph_lemmatized)
        current_paragraph_lemmatized = []

    return paragraphs_lemmatized

punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", " –"]
custom_stop_words = ["der", "die", "das", "für", "grüne", "linke", "afd", "spd", "cdu", "csu", "fdp", "Für", "über", "neu"]
STOP_WORDS.update(custom_stop_words)
STOP_WORDS.update(punctuation)

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
        current_paragraph_clean = []

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
    most_common = []
    for paragraph in manifesto_clean:
        c = Counter(paragraph)
        #current_most_common = []
        #current_most_common.append(c.most_common(3))
        most_common.append(c.most_common(3))
    return most_common

print('##############################')
print(most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs('41113_202109.csv'))))) #grün
print('##############################')
print(most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs('41223_202109.csv'))))) #linke
print('##############################')
print(most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs('41320_202109.csv'))))) #spd
print('##############################')
print(most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs('41420_202109.csv'))))) #fdp
print('##############################')
print(most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs('41521_202109.csv'))))) #cdu
print('##############################')
print(most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs('41953_202109.csv'))))) #afd