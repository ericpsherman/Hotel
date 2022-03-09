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
        print(date_from,date_to)
        database.show_available_rooms(date_from, date_to)
    return render_template('booking.html')


if __name__ == '__main__':
    # app.run(debug=True)
    booking_availability = database.is_available('2022-03-09', '2022-03-14', 'A Class')
    print(booking_availability)
    if booking_availability[0]:
        database.book_a_room(booking_availability[1], booking_availability[2], booking_availability[3])
    database.display()
