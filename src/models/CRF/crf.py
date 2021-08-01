from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
import pandas as pd

from src.feature_extraction.process_reports import get_sentences_from_report
from src.feature_extraction.sentence_features import get_features_corpus

import pickle as pkl

# Modeling
from sklearn.model_selection import cross_val_predict, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn_crfsuite import CRF, scorers, metrics
from sklearn_crfsuite.metrics import flat_classification_report
from sklearn.metrics import classification_report, make_scorer
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, train_test_split

# predict(text)
os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)

tagged = pd.read_csv(
    "D:\\Work\\Projects\\ideas_WHI\\PapersWithCode_NegationDetection\\UMLS_Utils\\src\\models\\data"
    "\\rpt_words_clean_24April_01.csv")
tagged = tagged.loc[0:4011]
tagged['Tag'].fillna('O', inplace=True)
tag_list = []

OUTPUT_FORMAT_TEXT = 1
OUTPUT_FORMAT_TUPLE = 2


# Extract only tag from dataframe
def get_list(df, i):
    return list(df.loc[df['Sentence #'] == i, 'Tag'])


# get a list of list from a flat list
def get_labels_lol():
    for i in range(0, 400):
        temp_lst = get_list(tagged, i)
        tag_list.append(temp_lst)
    return tag_list


def get_train_features(report_text):
    sentences = get_sentences_from_report(report_text)
    print(sentences)
    features = get_features_corpus(sentences)
    print(features)
    return features


def model_crf():
    crf = CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=200,
        all_possible_transitions=True
    )
    return crf


def get_saved_crf_model():
    features_pkl = 'D:\\Work\\Projects\\ideas_WHI\\PapersWithCode_NegationDetection\\UMLS_Utils\\src\\models' \
                   '\\saved_models\\crf.pickle'
    return pkl.load(open(features_pkl, 'rb'))


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def train_crf():
    crf = model_crf()
    features_pkl = 'D:\\Work\\Projects\\ideas_WHI\\PapersWithCode_NegationDetection\\UMLS_Utils\\src\\models' \
                   '\\saved_models\\Word_Features.pickle'
    X_train = pkl.load(open(features_pkl, 'rb'))
    y_train = get_labels_lol()
    crf.fit(X_train, y_train)
    return crf


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    report_text = request.json["text"]
    output_format = request.json["output_format"]
    X_test = get_train_features(report_text)
    crf = get_saved_crf_model()
    y_predicted = crf.predict(X_test)
    # print(y_predicted)
    if output_format == OUTPUT_FORMAT_TEXT:
        return {"Result": str(parse_output(X_test, y_predicted))}
    elif output_format == OUTPUT_FORMAT_TUPLE:
        return {"Result": str(parse_output_tuples(X_test, y_predicted))}
    else:
        return {"Result": str(parse_output(X_test, y_predicted))}


def predict_result(report_text):
    X_test = get_train_features(report_text)
    crf = get_saved_crf_model()
    y_predicted = crf.predict(X_test)
    print(y_predicted)
    print("Parsed html result:" + parse_output_html(str(parse_output(X_test, y_predicted))))
    text = " ".join(parse_output(X_test, y_predicted))
    print("Parsed html after join:" + parse_output_html(text))
    print("Parsed result:" + str(parse_output(X_test, y_predicted)))
    return {"Result": parse_output_html(text)}
    #if output_format == OUTPUT_FORMAT_TEXT:
    #    return {"Result": str(parse_output(X_test, y_predicted))}
    #elif output_format == OUTPUT_FORMAT_TUPLE:
    #    return {"Result": str(parse_output_tuples(X_test, y_predicted))}
    #else:
    #    return {"Result": str(parse_output(X_test, y_predicted))}


def parse_output_html(text):
    print("text: " + text)
    parsed_text = text.split()
    sentences = []
    inside = False;
    for word in parsed_text:
        parts = word.split("/")
        if parts[1] == "B":
            inside = True
            sentences.append("<span class='highlight'>" + parts[0])
        elif parts[1] == "O":
            if inside:
                sentences.append("</span> " + parts[0])
                inside = False
            else:
                sentences.append(parts[0])
        elif parts[1] == "I":
            sentences.append(parts[0])
    print("all html: " + str(sentences))
    return " ".join(word for word in sentences)


def parse_output(X, y):
    sentences = []
    for x, y in zip(X, y):
        each_sent = " ".join((xi.get('word') + '/' + yi) for xi, yi in zip(x, y))
        sentences.append(each_sent)
    return sentences


def parse_output_tuples(X, Y):
    sent = []
    for xi, yi in zip(X, Y):
        sent.append(list(map(lambda x, y: (x.get('word'), y), xi, yi)))
    return sent


# port = int(os.getenv("PORT"))
# if __name__ == "__main__":
# app.run(host='0.0.0.0', port=port)
#    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
