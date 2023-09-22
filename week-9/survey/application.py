import csv

from flask import Flask, redirect, render_template, request
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SelectField
from wtforms.validators import InputRequired, Email, DataRequired
from flask_bootstrap import Bootstrap


# Configure application
app = Flask(__name__)
Bootstrap(app)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "supersecretkey"

# Sample anime data
ANIMES = [
    {"id": "1", "name": "One Piece"},
    {"id": "2", "name": "Tokyo Revengers"},
    {"id": "3", "name": "Hunter × Hunter"},
    {"id": "4", "name": "The Stranger by the Shore"},
    {"id": "5", "name": "Naruto"},
    {"id": "6", "name": "Attack on Titan"},
    {"id": "7", "name": "Dakaichi: I'm Being Harassed By the Sexiest Man of the Year"},
]


# Form class using WTForms
class Form(FlaskForm):
    nickname = StringField("Nickname", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    favorite_anime = SelectField(
        "Favorite Anime",
        choices=[(anime["name"]) for anime in ANIMES],
        validators=[DataRequired()],
    )
    age = RadioField(
        choices=[("above", "Above"), ("below", "Below")],
        render_kw={"class": "form-check-input"},
        default="below",
        validators=[InputRequired()],
    )
    is_gay = RadioField(
        choices=[("yes", "I'm gay")],
        render_kw={"class": "form-check-input"},
        default="yes",
        validators=[InputRequired()],
    )


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    return redirect("/form")


@app.route("/form", methods=["GET", "POST"])
def form():
    form = Form(request.form)

    if request.method == "POST" and form.validate():
        # Save form data to csv
        with open("survey.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    form.nickname.data,
                    form.email.data,
                    form.favorite_anime.data,
                    form.age.data,
                    form.is_gay.data,
                ]
            )
        return redirect("/sheet")

    return render_template("form.html", animes=ANIMES, form=form)


@app.route("/sheet", methods=["GET"])
def sheet():
    data = []

    with open("survey.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    return render_template("sheet.html", data=data)
