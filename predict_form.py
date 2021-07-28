from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField, FloatField, StringField
from wtforms.validators import DataRequired
import pandas as pd

uniq_vals = pd.read_csv("data/unique_cat_vals.csv", index_col=0)


class InputData(FlaskForm):
    car = SelectField(label="Car", choices=uniq_vals.car.dropna().sort_values(), validators=[DataRequired()])
    model = SelectField("Model", choices=uniq_vals.model.dropna().sort_values(), validators=[DataRequired()])
    body = SelectField(label="Body", choices=uniq_vals.body.dropna().sort_values(), validators=[DataRequired()])
    drive = SelectField("Drive", choices=uniq_vals.drive.dropna().sort_values(), validators=[DataRequired()])
    engType = SelectField("Engine type: ", choices=uniq_vals.engType.dropna().sort_values(), validators=[DataRequired()])
    engV = FloatField("Engine Volume", validators=[DataRequired()])
    year = IntegerField("Year", validators=[DataRequired()])
    mileage = IntegerField(label="Mileage", validators=[DataRequired()])
    registration = SelectField(label="Registration", choices=uniq_vals.registration.dropna())

    submit = SubmitField("Predict the price")
