from flask import Flask, request, url_for, render_template, redirect
from utils import database

app = Flask(__name__)


@app.route('/')
def home():
    rooms = database.get_rooms()
    return render_template('home.html', rooms=rooms)


@app.route('/room/booking')
def booking():
    return render_template('booking.html')


if __name__ == '__main__':
    #app.run(debug=True)
    database.is_available('2022-03-09', '2022-03-14', 'A Class')
