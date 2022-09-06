import spacy
from collections import Counter
import preprocessing as pp
from evaluation.evaluation_data_extraction import eval_files


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
    most_common_nes.append(c.most_common(1))

    return most_common_nes


def manifesto_to_ne2(paragraphs_lemmatized):
    """ A function that takes lemmatized strings and extracts the named entites per paragraph.

    Parameters
    ----------
    paragraphs_lemmatized: lst of lst of str
        Lowercase lemmatized tokens.
    
    Return
    ------
    nes: lst of lst of tuples
        Named entities occurring in each paragraph.
    """
    nlp = spacy.load("de_core_news_sm")
    nes = []
    for paragraph in paragraphs_lemmatized:
        paragraph = ' '.join(paragraph)
        paragraph_processed = nlp(paragraph)
        current_nes = []
        for ent in paragraph_processed.ents:
            current_nes.append(ent.text)

        nes.append(current_nes)
        current_nes = []

    return nes


def most_frequent_nes(nes):
    """ A function that counts the occurrences of each named per paragraph and prints the 3 most frequent ones.

    Parameters
    ----------
    paragraph_nouns: lst of lst of str
        Lowercase lemmatized nouns excluding stop words and punctuation.

    Returns
    -------
    most_common: lst of lst of tuples
        Most common nouns occurring in the document and their frequency.
    """   
    most_common_nes = []
    for paragraph in nes:
        c = Counter(paragraph)
        if c.most_common(1)[0][1] > 1: # otherwise if there is none, it yields [(' ', 1)]
            most_common_nes.append(c.most_common(1))

    return most_common_nes


for file in eval_files:
    print(manifesto_to_ne2(pp.lemmatize_par(file)))


def named_entity_recognition():
    """ A function that stores the 10 most common named entities occurring in the manifestos and their frequency in a json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """ 

    results = {}
    for filename in pp.filenames:
        manifesto_as_str = pp.csv_to_string(filename)
        manifesto_lemmatized = pp.lemmatize_str(manifesto_as_str)
        manifesto_nes = manifesto_to_ne(manifesto_lemmatized)
        results[filename[:-14]] = manifesto_nes

    with open('results/Named_Entity_Recognition.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)

    return 


named_entity_recognition()