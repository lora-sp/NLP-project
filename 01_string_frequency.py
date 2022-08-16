import preprocessing as pp
from collections import Counter
import json

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
    return c.most_common(50)


def string_frequency(filename):
    """ A function that stores the 50 most common words occurring in the document and their frequency in a json file.

    Parameters
    ----------
    filename: str
        Name of the csv file.

    Returns
    -------
    None
    """ 
    with open(''+ filename[:-4] +'.json', 'w', encoding='utf-8') as f:
        #f.write("01: string frequency")
        json.dump({"01: string freqency": most_frequent(pp.remove_stopwords_str(pp.lemmatize_str(pp.csv_to_string(filename))))(filename)}, f, ensure_ascii=False)
    
    return 


for filename in pp.filenames: 
    string_frequency(filename)