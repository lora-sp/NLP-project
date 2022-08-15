import preprocessing as pp
from collections import Counter
import json

#???? kritik: verben sind dabei

# Pure Frequency Approach, using only the list of stop words to eliminate frequent words
# Works with preprocessing variant 1 (the whole manifesto saved in a string)

def most_frequent(manifesto_clean):
    """ A function that counts the occurrences of each word and prints the 5 most frequent words.

    Parameters
    ----------
    manifesto_clean: list with lowercase lemmas, excluding stop words

    Return
    ------
    5 most common words occuring in the document and their frequency
    """   
    c = Counter(manifesto_clean)
    return c.most_common(20)


def freq_pipeline(filename):
    """ A function that takes the filename of a csv file and performs all the functions previously introduced.

    Parameters
    ----------
    filename: name of the file in csv format

    Return
    ------
    5 most common words occuring in the document and their frequency
    """ 
    return most_frequent(pp.remove_stopwords_str(pp.lemmatize_str(pp.csv_to_string(filename))))



for filename in pp.filenames: 
    print(freq_pipeline(filename))


for filename in pp.filenames: 
    with open(''+ filename[:-4] +'.json', 'w', encoding='utf-8') as f:
        f.write("01: string frequency")
        json.dump(freq_pipeline(filename), f, ensure_ascii=False)