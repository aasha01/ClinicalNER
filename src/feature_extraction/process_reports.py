import pandas as pd
import spacy

import spacy.cli
spacy.cli.download("en_core_web_md")
nlp = spacy.load("en_core_web_md")

# Preprocess report text
import tqdm
import re


def split_in_sentences(text):
    doc = nlp(text)
    return [str(sent).strip() for sent in doc.sents if len(str(sent).strip()) > 0]


def remove_special_characters_except(text, remove_digits=False):
    pattern = r'[^a-zA-Z0-9\s.]' if not remove_digits else r'[^a-zA-Z\s.]'
    text = re.sub(pattern, '', text)
    return text


def clean_report_text(text):
    text = text.translate(text.maketrans("\n\t\r", "   "))
    text = remove_special_characters_except(text, remove_digits=True)
    return text


def remove_multiple_spaces(text):
    text = re.sub(' +', ' ', text)
    return text


def remove_multiple_dots(text):
    consequitivedots = re.compile(r'\.{2,}')
    text = consequitivedots.sub('', text).strip()
    return text


def report_to_sentences(text):
    text = clean_report_text(text)
    text = remove_multiple_dots(text)
    text = remove_multiple_spaces(text)
    return split_in_sentences(text)


# Can be used only for a dataset (collection) of text
def report_corpus_pre_processor(text_coll):
    norm_corpus = []
    for doc in tqdm.tqdm(text_coll):
        norm_corpus.extend(report_to_sentences(doc))
    return norm_corpus


# Returns a list of sentences which were preprocessed and split.
def get_sentences_from_report(report_text):
    return report_to_sentences(report_text)
