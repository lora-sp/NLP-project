from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import coo_matrix
import preprocessing as pp
import re ##???? braucht man das oder kann das weg
import json
from evaluation_data_extraction import eval_files


def sort_coo(coo_matrix):
    """ A function that sorts the tf-idf-vector that was transformed into a sparse matrix in coordinate format.

    Parameters
    ----------
    coo_matrix: array of arrays
        The tf-idf-vector transformed into a matrix.

    Returns
    -------
    coo_sorted: array of arrays
        The sorted matrix.
    """
    tuples = zip(coo_matrix.col, coo_matrix.data)
    coo_sorted = sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
    return coo_sorted
 

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """ A function that extracts the top 10 keywords and their tf-idf scores.

    Parameters
    ----------
    feature_names: lst of str
        Feature names.

    sorted_items: array of arrays
        The sorted matrix.

    Returns
    -------
    results: dict
        Top 10 keywords and their tf-idf scores.
    """
    
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    for idx, score in sorted_items:
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results

def tf_idf_eval():
    """ A function that extracts the top 10 keywords per evaluation file and their tf-idf scores and stores them in a json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    cv = CountVectorizer(max_df=0.8, stop_words=pp.STOP_WORDS, max_features=10000) 

    corpus = []
    for file in eval_files:
        file_joined = ' '.join(file)
        file_clean = pp.remove_stopwords_str(pp.lemmatize_str(file_joined))
        file_data = ' '.join(file_clean)
        corpus.append(file_data)

    X = cv.fit_transform(corpus)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)
    feature_names = cv.get_feature_names()

    results = {}
    for i in range(6):
        doc = corpus[i]
        tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        keywords = extract_topn_from_vector(feature_names, sorted_items, 3) #only the top 3 keywords
        results[pp.filenames[i][:-14]] = keywords 
        # with open("results/TF_IDF.json", 'w', encoding='utf-8') as f:
        #     json.dump(results, f, ensure_ascii=False, indent=3)

    print(results) # nicht soo gut weil eher "seltene" wörter hervorgehoben werden und manche parteien über dieselben themen sprechen

    return

tf_idf_eval()

def tf_idf():
    """ A function that extracts the top 10 keywords per manifesto and their tf-idf scores and stores them in a json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    cv = CountVectorizer(max_df=0.8, stop_words=pp.STOP_WORDS, max_features=10000) 

    corpus = []
    for filename in pp.filenames:
        data = pp.remove_stopwords_str(pp.lemmatize_str(pp.csv_to_string(filename)))
        data_joined = ' '.join(data)
        corpus.append(data_joined)

    X = cv.fit_transform(corpus)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(X)
    feature_names = cv.get_feature_names()

    results = {}
    for i in range(len(corpus)):
        doc = corpus[i]
        tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))
        sorted_items = sort_coo(tf_idf_vector.tocoo())
        keywords = extract_topn_from_vector(feature_names, sorted_items, 10)
        results[pp.filenames[i][:-14]] = keywords 
        with open("results/TF_IDF.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=3)

    return
    
    
tf_idf()

