from __future__ import division, print_function

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from flask_cors import CORS, cross_origin

# Define a flask app
from src.models.CRF.crf import predict_result

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
CORS(app)


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route("/train", methods=['POST'])
@cross_origin()
def train_crf():
    train_crf()


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    report_text = request.form['report_text']
    print("in predict: " + report_text)
    res = predict_result(report_text=report_text)
    return res.get("Result")
    #return "response text"


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    # In Cloud
    # app.run(host='0.0.0.0', debug = True, threaded = True)

    # Serve the app with gevent
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()
