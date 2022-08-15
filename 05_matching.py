import spacy
from spacy.matcher import Matcher
from spacy.matcher import DependencyMatcher
import preprocessing as pp

# Pattern matching and dependency matching
# Works with preprocessing variant 1 (manifesto as one continuous string)

#######################################################################################################################
# 1: pattern matching

def paragraphs_to_patterns(manifesto_as_str):
    nlp = spacy.load("de_core_news_sm")
    matcher = Matcher(nlp.vocab)

    pattern = [{"TAG": "VMFIN", "ORTH": {"IN": ["wollen", "will", "möchten", "möchte"]}}, 
               {"OP": "?"},
               {"POS": "DET", "OP": "?"}, 
               {"POS": "NOUN"}, 
               {"TAG": "VVINF"}]

    matcher.add("modals_pattern", [pattern])

    manifesto_processed =  nlp(manifesto_as_str)
    matches = matcher(manifesto_processed)

    print(len(matches)) #75 oder 48 mit orth restriction

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  
        span = manifesto_processed[start:end] 
        print(span.text) #type(match_id), string_id, 

    return

paragraphs_to_patterns(pp.csv_to_string('41113_202109.csv'))


#######################################################################################################################
# 2: dependency matching

def paragraphs_to_deps(manifesto_as_str):
    nlp = spacy.load("de_core_news_sm")
    matcher = DependencyMatcher(nlp.vocab)

    pattern = [
        {
            "RIGHT_ID": "modal", 
            "RIGHT_ATTRS": {"TAG": "VMFIN", "ORTH": {"IN": ["wollen", "will", "möchten", "möchte"]}}
        },
        {
             "LEFT_ID": "modal",
             "REL_OP": ".*",
             "RIGHT_ID": "noun",
             "RIGHT_ATTRS": {"POS": "NOUN"},
        },
        {
             "LEFT_ID": "noun", 
             "REL_OP": "<<", 
             "RIGHT_ID": "verb",
             "RIGHT_ATTRS": {"TAG": "VVINF", "DEP": "oa"}
        }
    ]

    matcher.add("modal_pattern", [pattern])
    manifesto_processed = nlp(manifesto_as_str)
    matches = matcher(manifesto_processed)

    print(len(matches))

    for k in matches:
        match_id, token_ids = k
        print(' '.join([manifesto_processed[token_ids[i]].text for i in range(len(token_ids))]))

    return 

paragraphs_to_deps(pp.csv_to_string('41113_202109.csv'))

# Reihenfolge der Token muss im Deutschen beachtet werden