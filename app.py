from flask import Flask, request, url_for, render_template, redirect
from utils import database

app = Flask(__name__)


@app.route('/')
def home():
    rooms = database.get_rooms()
    return render_template('home.html', rooms=rooms)


@app.route('/room/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        date_from = request.form.get('date-from')
        date_to = request.form.get('date-to')
        database.show_available_rooms(date_from, date_to)
    return render_template('booking.html')


if __name__ == '__main__':
    app.run(debug=True)
