from re import L
import preprocessing as pp
from collections import Counter
import json
from evaluation.evaluation_data_extraction import eval_files


# Pure Frequency Approach, using only the list of stop words to eliminate frequent words
# Works with preprocessing variant 1 (the whole manifesto saved into a continuous string)


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
results = {}
for filename in pp.filenames:
    data = open('manifestos/' + filename[:-14] + '_eval.json', 'r', encoding='utf8')
    data = ' '.join(data)
    data_lemmatized = pp.lemmatize_str(data)
    data_clean = pp.remove_stopwords_str(data_lemmatized)
    data_most_frequent = most_frequent_eval(data_clean)
    results[filename[:-14]] = data_most_frequent

with open('evaluation/eval_String_Frequency.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=3)

#def accuracy(most_frequent_strings):
data = open('results/eval_String_Frequency.json', 'r', encoding='utf8')
data2 = open('evaluation/evaluation_expected_outcomes.json', 'r', encoding='utf8')
data = json.load(data)
data2 = json.load(data2)
print(data)
print(data2)   
print(data["grüne"])
print(data2["grüne"])
lst = [] 
lst.append(data2["grüne"]["1"])
lst.append(data2["grüne"]["2"])
print(lst)
for i in range(len(data2["grüne"]["1"])):
    lst.append(data2["grüne"]["1"][i])#
for i in range(len(data2["grüne"]["2"])):
    lst.append(data2["grüne"]["2"][i])
print(lst)
counter = 0
for word in lst:
    for tuple in data["grüne"]:
        print(tuple[0], word)
        if tuple[0] == word:
            counter += 1
print(counter)
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
    
    return 


string_frequency()