import preprocessing as pp
from collections import Counter
import json
from evaluation.evaluation_data_extraction import eval_files


# Works with preprocessing variant 1 (the whole manifesto saved into a string)


def most_frequent(manifesto_clean):
    """ A function that counts the occurrences of each word and prints the 50 most frequent words.

    Parameters
    ----------
    manifesto_clean: lst
        Lowercase lemmatized tokens excluding stop words and punctuation.

    Returns
    -------
    most_common: lst of tuples
        50 most common words occurring in the document and their frequency.
    """   
    c = Counter(manifesto_clean)
    most_common = c.most_common(50) 
    return most_common


def most_frequent_eval(manifesto_clean):
    """ A function that counts the occurrences of each word and prints the 3 most frequent words; for evaluation purposes.

    Parameters
    ----------
    manifesto_clean: lst
        Lowercase lemmatized tokens excluding stop words and punctuation.

    Returns
    -------
    most_common: lst of tuples
        3 most common words occurring in the document and their frequency.
    """   
    c = Counter(manifesto_clean)
    most_common = c.most_common(3) 
    return most_common


# evaluation:
def eval_string_frequency():
    """ A function that stores the 3 most common words occurring in the evaluation files and their frequency in a json file.

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
        data_lemmatized = pp.lemmatize_str(data)
        data_clean = pp.remove_stopwords_str(data_lemmatized)
        data_most_frequent = most_frequent_eval(data_clean)
        results[filename[:-14]] = data_most_frequent

    with open('evaluation/evaluation_String_Frequency.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)


eval_string_frequency()


# result on the whole dataset:
def string_frequency():
    """ A function that stores the 50 most common words occurring in the manifestos and their frequency in a json file.

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
        manifesto_clean = pp.remove_stopwords_str(manifesto_lemmatized)
        manifesto_most_frequent = most_frequent(manifesto_clean)
        results[filename[:-14]] = manifesto_most_frequent

    with open('results/String_Frequency.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)


string_frequency()