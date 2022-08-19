import preprocessing as pp
from collections import Counter
import json
import evaluation_data_extraction as ev
import random


#???? kritik: verben sind dabei

# Pure Frequency Approach, using only the list of stop words to eliminate frequent words
# Works with preprocessing variant 1 (the whole manifesto saved in a string)


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
    return c.most_common(3)


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
    
    return 


string_frequency()