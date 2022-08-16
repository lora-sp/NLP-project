from collections import Counter
import preprocessing as pp

# Paragraph approach, using the list of stop words but also considering a minimal length for paragraphs
# Possibility to obtain a representative overview of the most common words per paragraph instead of considering the whole string
# Works with preprocessing variant 2 (manifesto divided into paragraphs)


def most_frequent(paragraphs_clean):
    """ A function that counts the occurrences of each word per paragraph and prints the 3 most frequent ones.

    Parameters
    ----------
    paragraphs_clean: lst of lst of str
        Lowercase lemmatized tokens excluding stop words and punctuation.

    Returns
    -------
    most_common: lst of lsf of tuples
        50 most common words occurring in the document and their frequency.
    """   
    most_common = []
    for paragraph in paragraphs_clean:
        c = Counter(paragraph)
        if c.most_common(1)[0][1] > 1: # otherwise if there is none, it yields [(' ', 1)]
            most_common.append(c.most_common(1))

    return most_common

def paragraph_frequency(filename):
    """ A function that stores the most common word per paragraph and its frequency in a json file.

    Parameters
    ----------
    filename: str
        Name of the csv file.

    Returns
    -------
    None
    """ 
    return most_frequent(pp.remove_stopwords_par(pp.lemmatize_par(pp.csv_to_paragraphs(filename))))

filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']
for filename in pp.filenames:
    print(paragraph_pipeline(filename))

print(paragraph_pipeline('41113_202109.csv'))
