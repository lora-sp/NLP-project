from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import coo_matrix
import re ##???? braucht man das oder kann das weg

cv=CountVectorizer(max_df=0.8,stop_words=STOP_WORDS, max_features=10000) #, ngram_range=(1,3) kann probably weg????

corpus = []
corpus.append(remove_stopwords(lemmatize(csv_to_string('41113_202109.csv')))) 
corpus.append(remove_stopwords(lemmatize(csv_to_string('41223_202109.csv')))) 
corpus.append(remove_stopwords(lemmatize(csv_to_string('41320_202109.csv'))))
corpus.append(remove_stopwords(lemmatize(csv_to_string('41420_202109.csv'))))
corpus.append(remove_stopwords(lemmatize(csv_to_string('41521_202109.csv'))))
corpus.append(remove_stopwords(lemmatize(csv_to_string('41953_202109.csv'))))

X=cv.fit_transform(corpus)

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(X)
feature_names=cv.get_feature_names()
doc = corpus[3]
tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
print(tf_idf_vector)


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 

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
keywords=extract_topn_from_vector(feature_names,sorted_items,10)
 
# now print the results
print("\nAbstract:")
print(doc)
print("\nKeywords:")
for k in keywords:
    print(k,keywords[k])