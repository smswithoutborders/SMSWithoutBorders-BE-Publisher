from peewee import MySQLDatabase
from peewee import DatabaseError

def connector(database: str, user: str, password: str, host: str) -> MySQLDatabase:
    """
    """
    try:
        db = MySQLDatabase(
            database,
            user=user,
            password=password,
            host=host,
        )

        return db

    except DatabaseError as error:
        raise error