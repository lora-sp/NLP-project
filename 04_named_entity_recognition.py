import spacy
from collections import Counter
import preprocessing as pp

#?????? hier vielleicht doch noch stopwords drinlassen, idk, ja doch weil dann ist es wie bei string frequency aber ohne verben halt ne

# Works with preprocessing variant 1 (manifesto as one continuous string)

def manifesto_to_ne(manifesto_lemmatized):
    """ A function that takes lemmatized strings and extracts the 10 most frequent named entites.

    Parameters
    ----------
    manifesto_lemmatized: lst of str
        Lowercase lemmatized tokens.
    
    Return
    ------
    most_common_ne: lst of tuples
        10 most common named entities occurring in the document and their frequency.
    """
    nlp = spacy.load("de_core_news_sm")
    nes = []

    manifesto_lemmatized = ' '.join(manifesto_lemmatized)
    manifesto_processed = nlp(manifesto_lemmatized)
    for ent in manifesto_processed.ents:
            nes.append(ent.text)

    most_common_nes = []
    c = Counter(nes)
    most_common_nes.append(c.most_common(10))

    return most_common_nes

def named_entity_recognition(filename):
    """ A function that stores the 10 most common named entities occurring in the document and their frequency in a json file.

    Parameters
    ----------
    filename: str
        Name of the csv file.

    Returns
    -------
    None
    """ 
    return (paragraphs_to_ne((pp.lemmatize_str(pp.csv_to_string(filename)))))

print(named_entity_pipeline('41113_202109.csv'))