import spacy
import csv
from spacy.lang.de.stop_words import STOP_WORDS
from collections import Counter
from spacy.matcher import Matcher

punctuation = [",", ".", "!", "?", "-", "_", ":", ";", "--", "-", " –"]
custom_stop_words = ["der", "die", "das", "grüne", "linke", "afd", "spd", "cdu", "csu", "fdp", "für", "über", "müssen"]
STOP_WORDS.update(punctuation)
STOP_WORDS.update(custom_stop_words)

# Pure Frequency Approach (stop words)
# Gesamten Text in einem String speichern, diesen tokenisieren, Stopwörter entfernen und die häufigsten Lemmata ausgeben lassen

def csv_to_string(filename):
    """ A function that reads a csv file and saves it in a string, excluding headers.

    Parameters
    ----------
    filename: name of the file in csv format

    Return
    ------
    manifesto_as_str: string containing text chunks excluding headers ("H")
    """
    with open(filename, newline='', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)
        manifesto_as_str = ""
        next(reader)
        for line in reader: 
            if line[1] != "H" and line[1] != "NA":
                manifesto_as_str = manifesto_as_str + " " + line[0]

    return manifesto_as_str

def lemmatize(manifesto_as_str):
    """ A function that lemmatizes the tokens in a given file using spaCy's German model.

    Parameters
    ----------
    manifesto_as_str: string obtained from csv file, excluding paragraphs

    Return
    ------
    manifesto_lemmatized: string lemmatized into lowercase words
    """
    nlp = spacy.load("de_core_news_sm")
    manifesto_processed = nlp(manifesto_as_str)
    manifesto_lemmatized = []
    for token in manifesto_processed:
        manifesto_lemmatized.append(token.lemma_.lower())

    return manifesto_lemmatized


# 3. Stoppwörter und Interpunktion entfernen

def remove_stopwords(manifesto_lemmatized):
    """ A function that removes stop words.

    Parameters
    ----------
    manifesto_lemmatized: list with lowercase lemmas for each token

    Return
    ------
    manifesto_clean: list of lemmas excluding stop words
    """
    manifesto_clean = []
    for lemma in manifesto_lemmatized:
        if lemma not in STOP_WORDS:
            manifesto_clean.append(lemma) 
    return manifesto_clean

# 4. Worthäufigkeiten zählen
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


#######
#tf-idf versuch:
#####dafür müssen erstmal alle wahlprogramme in einem liste sein und die strings müssen gejoined werden!!!!!

from sklearn.feature_extraction.text import CountVectorizer
import re
cv=CountVectorizer(max_df=0.8,stop_words=STOP_WORDS, max_features=10000) #ngram_range=(1,3)
corpus = []
corpus.append(lemmatize(csv_to_string('41113_202109.csv'))) 
corpus.append(lemmatize(csv_to_string('41223_202109.csv'))) 
corpus.append(lemmatize(csv_to_string('41320_202109.csv'))) 
corpus.append(lemmatize(csv_to_string('41420_202109.csv'))) 
corpus.append(lemmatize(csv_to_string('41521_202109.csv')))
corpus.append(lemmatize(csv_to_string('41953_202109.csv')))

for file in corpus:
    X=cv.fit_transform(file)

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(X)
doc = corpus[0]
tf_idf_vector=tfidf_transformer.transform(cv.transform([corpus[0]]))
print(tf_idf_vector)
print(corpus)
from scipy.sparse import coo_matrix
def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
sort_coo(tf_idf_vector)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results




#sort the tf-idf vectors by descending order of scores
sorted_items=sort_coo(tf_idf_vector.tocoo())
#extract only the top n; n here is 10
keywords=extract_topn_from_vector(feature_names,sorted_items,5)
 
# now print the results
print("\nAbstract:")
print(doc)
print("\nKeywords:")
for k in keywords:
    print(k,keywords[k])