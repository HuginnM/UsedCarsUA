import requests

from utils import Predictor
from utils import DataLoader
import numpy as np
from flask import Flask, request, jsonify, make_response, render_template
from flask_bootstrap import Bootstrap
from flask_restful import reqparse
from predict_form import InputData
from settings.constants import SECRET_KEY
import pandas as pd
import json


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    form = InputData()
    if form.validate_on_submit():

        def parse_arg_from_requests(arg, **kwargs):
            parse = reqparse.RequestParser()
            parse.add_argument(arg, **kwargs)
            args = parse.parse_args()
            return args[arg]

        form_values = (
            'car',
            'model',
            'body',
            'engType',
            'engV',
            'drive',
            'mileage',
            'registration',
            'year')

        req_data = {'data': json.dumps(
            {key : request.form.to_dict()[key] for key in form_values})}

        response = requests.get('http://0.0.0.0:8000/predict', data=req_data)
        print(response)
        api_predict = int(response.json()['prediction'][0])
        print(api_predict)
        message += "Predicted price in range: " + str(int(api_predict * 0.95 // 100 * 100))  + \
                   ' - ' + str(int(api_predict * 1.05 // 100 * 100))
    return render_template('index.html', form=form, message=message)


@app.route('/predict', methods=['GET'])
def predict():
    received_keys = sorted(list(request.form.keys()))
    if len(received_keys) > 1 or 'data' not in received_keys:
        err = 'Wrong request keys'
        return make_response(jsonify(error=err), 400)

    data = json.loads(request.form.get(received_keys[0]))
    print(data)
    df = pd.DataFrame.from_dict([data])
    loader = DataLoader()
    loader.fit(df)
    processed_df = loader.load_data()

    print(processed_df)

    predictor = Predictor()
    response_dict = {'prediction': predictor.predict(processed_df).tolist()}

    return make_response(jsonify(response_dict), 200)


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
