from flask import Flask, request, url_for, render_template, redirect
from database import data

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
