#!/usr/bin/env python
# coding: utf-8

# !python -m spacy download en_core_web_md
import spacy.cli
spacy.cli.download("en_core_web_md")
import en_core_web_md
nlp = en_core_web_md.load()


import spacy
nlp = spacy.load("en_core_web_md")


import re
from bs4 import BeautifulSoup
import unicodedata
import contractions
import spacy

nlp = spacy.load('en_core_web_md')


def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    [s.extract() for s in soup(['iframe', 'script'])]
    stripped_text = soup.get_text()
    stripped_text = re.sub(r'[\r|\n|\r\n]+', '\n', stripped_text)
    return stripped_text


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def expand_contractions(text):
    return contractions.fix(text)


def spacy_lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text


def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-Z0-9\s]' if not remove_digits else r'[^a-zA-Z\s]'
    text = re.sub(pattern, '', text)
    return text


def remove_stopwords(text, is_lower_case=False, stopwords=None):
    tokens = nlp(text)
    return ' '.join([tkn.text for tkn in tokens if not tkn.is_stop])


import tqdm

def text_pre_processor(text, html_strip=True, accented_char_removal=True, contraction_expansion=True,
                       text_lower_case=True, text_stemming=False, text_lemmatization=True, 
                       special_char_removal=True, remove_digits=True, stopword_removal=True, 
                       stopword_list=None):
    
    # strip HTML
    if html_strip:
        text = strip_html_tags(text)
    
    # remove extra newlines (often might be present in really noisy text)
    text = text.translate(text.maketrans("\n\t\r", "   "))
    
    # remove accented characters
    if accented_char_removal:
        text = remove_accented_chars(text)
    
    # expand contractions    
    if contraction_expansion:
        text = expand_contractions(text)
        
    
    # lemmatize text
    if text_lemmatization:
        text = spacy_lemmatize_text(text) 
        
    # remove special characters and\or digits    
    if special_char_removal:
        # insert spaces between special characters to isolate them    
        special_char_pattern = re.compile(r'([{.(-)!}])')
        text = special_char_pattern.sub(" \\1 ", text)
        text = remove_special_characters(text, remove_digits=remove_digits)  
        
    # stem text
    if text_stemming and not text_lemmatization:
        text = simple_stemming(text)
        
    # lowercase the text    
    if text_lower_case:
        text = text.lower()
        
        
    # remove stopwords
    if stopword_removal:
        text = remove_stopwords(text)
        
    # remove extra whitespace
    text = re.sub(' +', ' ', text)
    text = text.strip()
    
    return text

#Can be used only for a dataset (collection) of text
def corpus_pre_processor(text_coll):
    norm_corpus = []
    for doc in tqdm.tqdm(text_coll):
        norm_corpus.append(text_pre_processor(doc))
    return norm_corpus

#document = """<p>Héllo! Héllo! can you hear me! I just heard about <b>Python</b>!<br/>\r\n 
#              It's an amazing language which can be used for [Scripting\tWeb development\tBackend development],\r\n\r\n
#              Information Retrieval, Natural Language Processing, Machine Learning & Artificial Intelligence!\n
#              What are you waiting for? Go and get started.<br/> He's learning, she's learning, they've already\n\n
#              got a headstart! GET PYTHON 3.6 NOW!</p>
#           """
#text_pre_processor(document)


# Use for text collection
#corpus_pre_processor(corpus)
