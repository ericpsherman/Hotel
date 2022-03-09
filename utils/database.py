import pandas
import typing
from .database_connection import DatabaseConnection


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


def show_available_rooms(date_from, date_to) -> None:
    """
    Displays rooms in the date range given by the user.
    :param date_from:
    :param date_to:
    :return: None
    """
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        for available in cursor.execute(f'SELECT * FROM availability WHERE Date BETWEEN {date_from} AND {date_to}'):
            print(available)
