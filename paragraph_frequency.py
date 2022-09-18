from collections import Counter
import preprocessing as pp
import spacy


# Works with preprocessing variant 2 (manifesto divided into paragraphs)


# optional:
def nouns_only(paragraphs_clean):
    """ A function that filters out nouns for each paragraph.

    Parameters
    ----------
    paragraphs_clean: lst of lsf of str
        Lowercase lemmatized tokens excluding stop words and punctuation.

    Returns
    -------
    paragraphs_clean: lst of lst of str
        Lowercase lemmatized nouns excluding stop words and punctuation.
    """
    nlp = spacy.load("de_core_news_sm")    
    paragraphs_nouns = []
    for paragraph in paragraphs_clean:
        paragraph = ' '.join(paragraph)
        paragraphs_processed = nlp(paragraph)
        current_paragraph_nouns = []
        for token in paragraphs_processed:
            if token.pos_ == "NOUN":
                current_paragraph_nouns.append(token.text)

        paragraphs_nouns.append(current_paragraph_nouns) 
        current_paragraph_nouns = []

    return paragraphs_nouns


def most_frequent(paragraphs_nouns):
    """ A function that counts the occurrences of each noun per paragraph and prints the 3 most frequent ones.

    Parameters
    ----------
    paragraphs_nouns: lst of lst of str
        Lowercase lemmatized nouns excluding stop words and punctuation.

    Returns
    -------
    most_common: lst of lst of tuples
        Most common nouns occurring in the document and their frequency.
    """   
    most_common = []
    for paragraph in paragraphs_nouns:
        c = Counter(paragraph)
        if c.most_common(3)[0][1] > 1: # otherwise if there is none, it yields [(' ', 1)]
            most_common.append(c.most_common(3))

    return most_common


def most_frequent_eval(paragraphs_nouns):
    """ A function that counts the occurrences of each noun per paragraph and prints the most frequent one; for evaluation purposes.

    Parameters
    ----------
    paragraphs_nouns: lst of lst of str
        Lowercase lemmatized nouns excluding stop words and punctuation.

    Returns
    -------
    most_common: lst of lst of tuples
        Most common nouns occurring in the document and their frequency.
    """   
    most_common = []
    for paragraph in paragraphs_nouns:
        c = Counter(paragraph)
        if c.most_common(3)[0][1] > 1: # otherwise if there is none, it yields [(' ', 1)]
            most_common.append(c.most_common(1))

    return most_common


# evaluation:
def eval_paragraph_frequency():
    """ A function that stores the most common noun per evaluation file and its frequency in a json file.

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
        data_lemmatized = pp.lemmatize_par(data)
        data_clean = pp.remove_stopwords_par(data_lemmatized)
        #data_nouns = nouns_only(data_clean)
        data_most_frequent = most_frequent_eval(data_clean) #data_nouns
        results[filename[:-14]] = data_most_frequent

    with open('evaluation/evaluation_Paragraph_Frequency.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)


eval_paragraph_frequency()


# result on the whole dataset:  
def paragraph_frequency():
    """ A function that stores the most common noun per paragraph in the manifestos and its frequency in a json file.

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
        #paragraphs_nouns = nouns_only(paragraphs_clean)
        paragraphs_most_frequent = most_frequent(paragraphs_clean) #paragraphs_nouns
        results[filename[:-14]] = paragraphs_most_frequent

    with open('results/Paragraph_Frequency.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)


paragraph_frequency()
