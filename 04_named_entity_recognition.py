import spacy
from collections import Counter

#?????? hier vielleicht doch noch stopwords, idk, ja doch weil dann ist es wie bei string frequency aber ohne verben halt ne

# Works with preprocessing variant 2 (manifesto divided into paragraphs)

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

