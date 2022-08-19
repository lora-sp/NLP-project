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


def paragraph_frequency():
    """ A function that stores the most common word per paragraph in the manifestos and its frequency in a json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """ 

    results = {}
    for filename in pp.filenames:
        long_paragraphs = pp.csv_to_paragraphs(filename)
        paragraphs_lemmatized = pp.lemmatize_par(long_paragraphs)
        paragraphs_clean = pp.remove_stopwords_par(paragraphs_lemmatized)
        paragraphs_most_frequent = most_frequent(paragraphs_clean)
        results[filename[:-14]] = paragraphs_most_frequent

    with open('results/Paragraph_Frequency.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)

    return


paragraph_frequency()

