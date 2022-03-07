from flask import Flask, request, url_for, render_template, redirect
from utils import database

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

