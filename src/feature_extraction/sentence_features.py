import spacy
import pandas as pd

from src.DAO.ConnectUMLS import symantic_type_lookup, is_cui_found, cui_lookup
# !python -m spacy download en_core_web_md
import spacy.cli
spacy.cli.download("en_core_web_md")

nlp = spacy.load("en_core_web_md")


def get_parent_token(doc, token_text):
    for chunk in doc.noun_chunks:
        if str(chunk).find(token_text) != -1:
            return chunk.root.head


def get_features_sentence(sentence, i):
    # G1 = pd.DataFrame(columns = ['word', 'prev_word', 'next_word', 'word_length', 'prev_2_words', 'next_2_words',
    #                            'word_POS_tag','prev_POS_tag', 'next_POS_tag', 'lemmatized', 'parent',
    #                             'bigram', 'trigram', 'reverse_bigram'])

    features = []

    doc = nlp(sentence)
    doc_len = len(doc) - 1

    for token in doc:
        current_word = token.text.lower()

        word_length = len(current_word)
        BOS = False
        EOS = False

        prev_token = ""
        next_token = ""

        if word_length == 0:
            continue

        token_index = token.i

        if token_index == 0:
            BOS = True

        if token_index == doc_len:
            EOS = True

        if token_index == 0:
            prev_word = "*"
        else:
            prev_token = doc[token_index - 1]
            prev_word = prev_token.text

        if token_index < doc_len:
            next_token = doc[token_index + 1]
            next_word = next_token.text
        else:
            next_word = "*"

        if token_index > 1:
            prev_2_words = doc[token_index - 2].text + ' ' + doc[token_index - 1].text
        elif token_index == 1:
            prev_2_words = doc[token_index - 1].text
        else:
            prev_2_words = "*"

        if token_index < (doc_len - 2):
            next_2_words = doc[token_index + 1].text + ' ' + doc[token_index + 2].text
        elif token_index == (doc_len - 1):
            next_2_words = doc[token_index + 1].text
        else:
            next_2_words = "*"

        word_POS_tag = token.pos_

        if token_index == 0:
            prev_POS_tag = ''
        else:
            prev_POS_tag = prev_token.pos_

        if token_index < doc_len:
            next_POS_tag = next_token.pos_
        else:
            next_POS_tag = ''

        lemma = token.lemma_

        parent = get_parent_token(doc, current_word)
        if type(parent) == type(None):
            parent_text = ''
        else:
            parent_text = parent.text
        # Parent node's chunk is not very accurate. So may be excluded when using it in learning CRF

        bigram = current_word + ' ' + next_word
        trigram = prev_word + ' ' + current_word + ' ' + next_word
        reverse_bigram = prev_word + ' ' + current_word

        # UMLS Features to Dict
        sty_word = symantic_type_lookup(current_word)
        sty_prev_word = symantic_type_lookup(prev_word)
        sty_next_word = symantic_type_lookup(next_word)
        match_bigram = is_cui_found(bigram)
        match_trigram = is_cui_found(trigram)
        match_reverse_bigram = is_cui_found(reverse_bigram)
        CIU_word = cui_lookup(current_word)

        feat_dict = {'sent': i, 'word': current_word, 'prev_word': prev_word, 'next_word': next_word,
                     'word_length': word_length, 'prev_2_words': prev_2_words, 'next_2_words': next_2_words,
                     'word_POS_tag': word_POS_tag, 'prev_POS_tag': prev_POS_tag, 'next_POS_tag': next_POS_tag,
                     'lemmatized': lemma, 'parent': parent_text, 'bigram': bigram, 'trigram': trigram,
                     'reverse_bigram': reverse_bigram, 'BOS': BOS, 'EOS': EOS,
                     'sty_word': sty_word, 'sty_prev_word': sty_prev_word, 'sty_next_word': sty_next_word,
                     'match_bigram': match_bigram, 'match_trigram': match_trigram,
                     'match_reverse_bigram': match_reverse_bigram,
                     'CIU_word': CIU_word}

        features.append(feat_dict)
    return features


def get_features_corpus(report_sentences):
    corpus = []
    for i, each_sentence in enumerate(report_sentences):
        print(each_sentence, ' - ', i)
        corpus.append(get_features_sentence(each_sentence, i))
    return corpus


# Input as a list of sentences
# Output is a list of lists
def get_features_from_sentences(report_sentences):
    return get_features_corpus(report_sentences)


# This code is to get training data sentences without features
# Used only when manually tuning the model
# Not used by the application directly
def get_training_data_sentence(sentence, i):
    G1 = pd.DataFrame(columns=['Sentence #', 'Word', 'POS', 'Tag'])

    doc = nlp(sentence)
    doc_len = len(doc) - 1

    for token in doc:
        current_word = token.text

        token_index = token.i

        #Sentence #	 Word	POS	Tag
        train_data = {'Sentence #': i, 'Word': current_word, 'POS': token.pos_, 'Tag': ''}

        G1 = G1.append(train_data, ignore_index=True)
    return G1


def get_training_data_corpus(report_sentences):
    G1 = pd.DataFrame(columns=['Sentence #', 'Word', 'POS', 'Tag'])
    for i, each_sentence in enumerate(report_sentences):
        print(each_sentence, ' - ', i)
        G1 = G1.append(get_training_data_sentence(each_sentence, i), ignore_index=True)
    return G1
