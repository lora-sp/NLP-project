from collections import Counter

# Paragraph approach, using the list of stop words but also considering a minimal length for paragraphs
# Possibility to obtain a representative overview of the most common words per paragraph instead of considering the whole string
# Works with preprocessing variant 2 (manifesto divided into paragraphs)


def most_frequent(manifesto_clean):
    """ A function that counts the occurrences of each word per paragraph and prints the 3 most frequent words.

    Parameters
    ----------
    manifesto_clean: list of paragraphs consisting of lists of lowercase lemmas, excluding stop words

    Return
    ------
    most_common: 3 most common words occuring in each paragraph and their frequency
    """   
    most_common = []
    for paragraph in manifesto_clean:
        c = Counter(paragraph)
        most_common.append(c.most_common(3))

    return most_common

def paragraph_pipeline(filename):
    """ A function that takes the filename of a csv file and performs all the functions previously introduced.

    Parameters
    ----------
    filename: name of the csv-file

    Return
    ------
    3 most common words occuring in each of the 10 longest paragraphs of the document and their frequency
    """ 
    return most_frequent(remove_stopwords(lemmatize(csv_to_paragraphs(filename))))

filenames = ['41113_202109.csv', '41223_202109.csv', '41320_202109.csv', '41420_202109.csv', '41521_202109.csv', '41953_202109.csv']
for filename in filenames:
    print(paragraph_pipeline(filename))

