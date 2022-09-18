import spacy
import json
from collections import Counter
import preprocessing as pp


# Works with preprocessing variant 1 (the whole manifesto saved into a string)


def manifesto_to_ne(manifesto_as_str):
    """ A function that takes manifestos as strings and extracts the 50 most frequent named entites.

    Parameters
    ----------
    manifesto_as_str : str
        Manifesto text without headers and additional information.

    Return
    ------
    most_common_ne: lst of tuples
        50 most common named entities occurring in the document and their frequency.
    """
    nlp = spacy.load("de_core_news_sm")
    nes = []

    manifesto_processed = nlp(manifesto_as_str)
    for ent in manifesto_processed.ents:
            nes.append(ent.text)

    most_common_nes = []
    c = Counter(nes)
    most_common_nes.append(c.most_common(50))

    return most_common_nes


def manifesto_to_ne_eval(manifesto_as_str):
    """ A function that takes manifestos as strings and extracts the 3 most frequent named entites; for evaluation purposes.

    Parameters
    ----------
    manifesto_as_str : str
        Manifesto text without headers and additional information.
    
    Return
    ------
    most_common_ne: lst of tuples
        3 most common named entities occurring in the document and their frequency.
    """
    nlp = spacy.load("de_core_news_sm")
    nes = []

    manifesto_processed = nlp(manifesto_as_str)
    for ent in manifesto_processed.ents:
            nes.append(ent.text)

    most_common_nes = []
    c = Counter(nes)
    most_common_nes.append(c.most_common(3))

    return most_common_nes


# evaluation:
def eval_named_entity_recognition():
    """ A function that stores the 3 most common named entities occurring in the evaluation files and their frequency in a json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """ 
    results = {}
    for filename in pp.filenames:
        data = open('evaluation/eval_' + filename[:-14] + '.json', 'r', encoding='utf8')
        data = ' '.join(data)
        data_nes = manifesto_to_ne_eval(data)
        results[filename[:-14]] = data_nes

    with open('evaluation/evaluation_Named_Entity_Recognition.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)


eval_named_entity_recognition()


# result on the whole dataset:
def named_entity_recognition():
    """ A function that stores the 50 most common named entities occurring in the manifestos and their frequency in a json file.

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
        manifesto_nes = manifesto_to_ne(manifesto_as_str)
        results[filename[:-14]] = manifesto_nes

    with open('results/Named_Entity_Recognition.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)


named_entity_recognition()