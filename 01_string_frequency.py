from collections import Counter

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
    return most_frequent(remove_stopwords(lemmatize(csv_to_string(filename))))

filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']

for filename in filenames: 
    print(freq_pipeline(filename))




