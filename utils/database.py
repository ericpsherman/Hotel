# import pandas
import typing
from datetime import datetime
from .database_connection import DatabaseConnection

DATE_FORMAT = "%Y-%m-%d"

query_dict = {
            101: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '101'=1",
                  f"UPDATE TABLE availability SET '101' = 0 WHERE Date BETWEEN ? AND ?"],
            102: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '102'=1",
                  f"UPDATE TABLE availability SET '102' = 0 WHERE Date BETWEEN ? AND ?"],
            103: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '103'=1",
                  f"UPDATE TABLE availability SET '103' = 0 WHERE Date BETWEEN ? AND ?"],
            104: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '104'=1",
                  f"UPDATE TABLE availability SET '104' = 0 WHERE Date BETWEEN ? AND ?"],
            105: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '105'=1",
                  f"UPDATE TABLE availability SET '105' = 0 WHERE Date BETWEEN ? AND ?"],
            201: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '201'=1",
                  f"UPDATE TABLE availability SET '201' = 0 WHERE Date BETWEEN ? AND ?"],
            202: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '202'=1",
                  f"UPDATE TABLE availability SET '202' = 0 WHERE Date BETWEEN ? AND ?"],
            203: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '203'=1",
                  f"UPDATE TABLE availability SET '203' = 0 WHERE Date BETWEEN ? AND ?"],
            204: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '204'=1",
                  f"UPDATE TABLE availability SET '204' = 0 WHERE Date BETWEEN ? AND ?"],
            205: [f"SELECT COUNT(*) FROM availability WHERE Date BETWEEN ? AND ? AND '205'=1",
                  f"UPDATE TABLE availability SET '205' = 0 WHERE Date BETWEEN ? AND ?"]
}


def initialize() -> None:
    """
    Has multiple functionalities:
        1. When part 1 is uncommented and part 2 is commented, it uses the excel file to create a database, with two
        tables - rooms and availability. The availability table is a calendar table for the next 30 days.
        2. Once part 1 is run, it shall be commented and part 2 is run every time a booking occurs. Part 2 deletes
        the previous days entries and updates the calendar with more days, ensuring users can always book 30 days in
        advance.
    Note: Call this function every time to proceed with the booking.
    :return: None
    """

    """
        PART 1
    """

    # data_from_excel = pandas.read_excel(r'room_excel.xlsx', sheet_name='Sheet1')
    # dataframe = pandas.DataFrame(data_from_excel, columns=['Room Number', 'Category', 'Price'])
    #
    # with DatabaseConnection('data.db') as connection:
    #     cursor = connection.cursor()
    #     dataframe.to_sql('rooms', connection, if_exists='append', index=False)
    #
    # with DatabaseConnection('data.db') as connection:
    #     cursor = connection.cursor()
    #     cursor.execute('CREATE TABLE IF NOT EXISTS availability(Date TEXT PRIMARY KEY, "101" INTEGER, "102" INTEGER,'
    #                    ' "103" INTEGER, "104" INTEGER, "105" INTEGER, "201" INTEGER, "202" INTEGER, "203" INTEGER,'
    #                    ' "204" INTEGER, "205" INTEGER)')
    #     for data in cursor.execute("SELECT julianday('now')"):
    #         pass
    #     for date in cursor.execute('SELECT date(?)', data):
    #         pass
    #     data = (data[0],)
    #     for _ in range(30):
    #         cursor.execute('INSERT OR IGNORE INTO availability VALUES(?, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)', date)
    #         data = (data[0]+1,)
    #         for date in cursor.execute('SELECT date(?)', data):
    #             pass

    """
        PART 2   
    """

    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT julianday('now')")
        data = cursor.fetchone()
        cursor.execute('SELECT date(?)', data)
        date = cursor.fetchone()
        data = (data[0],)
        cursor.execute('SELECT date(?)', data)
        date = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) from availability where Date < ?', date)
        length_of_updation = cursor.fetchone()
        cursor.execute('DELETE FROM availability where Date < ?', date)

    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        print(length_of_updation)
        data = (data[0] + 30 - length_of_updation[0],)
        cursor.execute('SELECT date(?)', data)
        date = cursor.fetchone()
        print(date)
        for _ in range(length_of_updation[0]):
            cursor.execute('INSERT OR IGNORE INTO availability VALUES(?, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)', date)
            data = (data[0] + 1,)
            for date in cursor.execute('SELECT date(?)', data):
                pass


def display() -> None:
    """
    Displays two tables: rooms(the categories and prices) and availability(a calendar table showing availability).
    :return: None
    """
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        for room in cursor.execute('SELECT * FROM rooms'):
            print(room)

    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        for available in cursor.execute('SELECT * from availability'):
            print(available)


def is_available(from_date=None, to_date=None, room_class=None) -> list[tuple]:
    """
    Checks if a certain category has rooms available between two dates.
    :param from_date: The starting date of booking
    :param to_date: The ending date of booking
    :param room_class: The category of the room
    :return: list of tuple of available rooms and their prices -> list[(room_no, price)]
    """
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        room_numbers = []
        for room in cursor.execute('SELECT "Room Number", Price FROM rooms WHERE Category=?', (room_class,)):
            room_numbers.append(room)

        print(room_numbers)
        available_rooms = []
        a = datetime.strptime(from_date, DATE_FORMAT)
        b = datetime.strptime(to_date, DATE_FORMAT)
        delta = b - a
        print(delta.days)

        cursor = connection.cursor()
        list_of_availability = []
        for data in cursor.execute('SELECT * FROM availability WHERE Date BETWEEN ? and ? AND 101=1', (from_date,
                                                                                                       to_date)):
            list_of_availability.append(data)
        print(list_of_availability)


def book_a_room(from_date=None, to_date=None, room_class=None):
    """
    Books a room using specified dates and updates its availability according to the parameters.
    :param from_date: The starting date of booking
    :param to_date: The ending date of booking
    :param room_class: The category of the room
    :return: None
    """
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        room_numbers = []
        for room in cursor.execute('SELECT "Room Number", Price FROM rooms WHERE Category=?', (room_class,)):
            room_numbers.append(room)
        print(room_numbers)


def get_rooms() -> list[dict]:
    """
    Gets details of all the rooms from the database and converts it to a list of dictionaries.
    :return: rooms as list[dict]
    """
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM rooms')
        rooms = [{'room_no': row[0], 'room_type': row[1], 'price': row[2]} for row in cursor.fetchall()]

        return rooms
