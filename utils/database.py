from .database_connection import DatabaseConnection


"""
    
"""
def initialize() -> None:
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()


