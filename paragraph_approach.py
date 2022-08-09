import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter
from spacy.matcher import Matcher

punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", " –", ">", "<", "%", " "]
custom_stop_words = ["der", "die", "das", "grüne", "linke", "afd", "spd", "cdu", "csu", "fdp", "für", "über", "müssen"]
STOP_WORDS.update(punctuation)
STOP_WORDS.update(custom_stop_words)


# Paragraph Approach (stop words + paragraph length)
# Text in Absätze teilen, die längeren Absätze analysieren und dort die häufigsten Worte ausgeben lassen

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
        
        #print(len(manifesto_paragraphs))

        longest_paragraphs = []
        for paragraph in manifesto_paragraphs:
            if len(paragraph) < 100:
                continue
            longest_paragraph = max(manifesto_paragraphs, key=len)
            longest_paragraphs.append(longest_paragraph)
            manifesto_paragraphs.remove(longest_paragraph)

        #print(len(longest_paragraphs))

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
    for paragraph in longest_paragraphs:
        paragraph_processed = nlp(paragraph)
        current_paragraph_lemmatized = []
        for token in paragraph_processed:
            current_paragraph_lemmatized.append(token.lemma_.lower())

        " ".join(current_paragraph_lemmatized)
        paragraphs_lemmatized.append(current_paragraph_lemmatized)
        current_paragraph_lemmatized = []

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
        current_paragraph_clean = []

    return manifesto_clean


def most_frequent(manifesto_clean):
    """ A function that counts the occurrences of each word per paragraph and prints the 3 most frequent words.

    Parameters
    ----------
    manifesto_clean: list of paragraphs consisting of lists of lowercase lemmas, excluding stop words

    Return
    ------
    most_common: 3 most common words occuring in each paragraph and their frequency
    """   
    most_common = []
    for paragraph in manifesto_clean:
        c = Counter(paragraph)
        most_common.append(c.most_common(3))

    return most_common

def paragraph_pipeline(filename):
    """ A function that takes the filename of a csv file and performs all the functions previously introduced.

    Parameters
    ----------
    filename: name of the csv-file

    Return
    ------
    3 most common words occuring in each of the 10 longest paragraphs of the document and their frequency
    """ 
    return most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs(filename))))

filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']
for filename in filenames:
    print(paragraph_pipeline(filename))


###################################################################################
# Alternativ häufigste named entities für die längsten Abschnitte ausgeben lassen

def paragraphs_to_ne(paragraphs_lemmatized):
    """ A function that takes lemmatized strings and extracts the 10 most frequent named entites.

    Parameters
    ----------
    paragraphs_lemmatized: a list of strings (lemmatized paragraphs)
    
    Return
    ------
    most_common_ne: 10 most frequent named entities
    """
    nlp = spacy.load("de_core_news_sm")
    nes = []

    for paragraph in paragraphs_lemmatized:
        paragraph = ' '.join(paragraph)
        paragraph_processed = nlp(paragraph)
        for ent in paragraph_processed.ents:
                nes.append(ent.text.lower() + " " + ent.label_)

    most_common_nes = []
    c = Counter(nes)
    most_common_nes.append(c.most_common(10))

    return most_common_nes

def named_entity_pipeline(filename):
    """ A function that takes the filename of a csv file and performs all the functions previously introduced.

    Parameters
    ----------
    filename: name of the csv-file

    Return
    ------
    10 most common named entities occuring in each of the longest paragraphs of the document and their frequency
    """ 
    return (paragraphs_to_ne(lemmatize(csv_to_paragraphs(filename))))


###################################################################################
# Alternativ pattern matching

def paragraphs_to_patterns(longest_paragraphs):
    nlp = spacy.load("de_core_news_sm")
    matcher = Matcher(nlp.vocab)

    pattern = [{"TAG": "VMFIN"}, 
               {"OP": "?"},
               {"OP": "?"},
               {"OP": "?"},
               {"POS": "DET", "OP": "?"}, 
               {"POS": "NOUN"}, 
               {"TAG": "VVINF"}]

    matcher.add("modals_pattern", [pattern])

    for paragraph in longest_paragraphs:

        paragraph_processed =  nlp(paragraph)
        matches = matcher(paragraph_processed)

        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  
            span = paragraph_processed[start:end] 
            print(type(match_id), string_id, start, end, span.text)

    return

paragraphs_to_patterns(csv_to_paragraphs('41113_202109.csv'))

#########################################################
#bisschen ungenau daher dependency matching statt pattern matching??
