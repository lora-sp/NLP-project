from spacy.matcher import Matcher
#???? und dependency matcher!

# Pattern matching and dependency matching
# Works with preprocessing variant 2 (manifesto divided into paragraphs)

#######################################################################################################################
# 1: pattern matching

def paragraphs_to_patterns(longest_paragraphs):
    nlp = spacy.load("de_core_news_sm")
    matcher = Matcher(nlp.vocab)

    pattern = [{"TAG": "VMFIN"}, 
               {"OP": "?"},
               {"OP": "?"},
               {"OP": "?"},
               {"POS": "DET", "OP": "?"}, 
               {"POS": "NOUN"}, 
               {"TAG": "VVINF"}]

    matcher.add("modals_pattern", [pattern])

    for paragraph in longest_paragraphs:

        paragraph_processed =  nlp(paragraph)
        matches = matcher(paragraph_processed)

        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  
            span = paragraph_processed[start:end] 
            print(type(match_id), string_id, start, end, span.text)

    return

paragraphs_to_patterns(csv_to_paragraphs('41113_202109.csv'))


#######################################################################################################################
# 2: dependency matching