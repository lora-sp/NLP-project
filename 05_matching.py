import spacy
from spacy.matcher import Matcher
from spacy.matcher import DependencyMatcher
import preprocessing as pp

# Pattern matching and dependency matching

#######################################################################################################################
# 1: pattern matching


def string_to_patterns(manifesto_as_str):
    """
    A function that extracts all occurrences of the defined pattern.

    Parameters
    ----------
    manifesto_as_str: str
        Manifesto text without headers and additional information.

    Returns
    -------
    matches_lst: lst of str
        All occurrences of the defined pattern.
    """
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

    #print(len(matches)) #75 oder 48 mit orth restriction

    matches_lst = []
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  
        span = manifesto_processed[start:end] 
        matches_lst.append(span.text) #type(match_id), string_id, kann oben wahrscheinlich weg

    return matches_lst


def pattern_matching():
    """ A function that stores all occurrences of the defined pattern in the manifestos in a json file.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """ 
    results = {}
    for filename in pp.filenames:
        manifesto_as_str = pp.csv_to_string(filename)
        manifesto_patterns = string_to_patterns(manifesto_as_str)
        results[filename[:-14]] = manifesto_patterns

    with open('results/Pattern_Matching.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=3)
    
    return 


pattern_matching()


#######################################################################################################################
# 2: dependency matching


def paragraphs_to_deps(manifesto_as_str):
    """
    A function that extracts all occurrences of the defined dependency relation.

    Parameters
    ----------
    manifesto_as_str: str
        Manifesto text without headers and additional information.

    Returns
    -------
    None
    """
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

