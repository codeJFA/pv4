import psycopg2
from psycopg2 import OperationalError
import config

def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=config.dbname,
            user=config.user,
            password=config.password,
            host=config.host,
            port=config.port
        )
        print("Kapcsolódva az adatbázishoz!")
    except OperationalError as e:
        print(f"Hiba a kapcsolódás során: {e}")
    return connection

def close_connection(connection):
    if connection:
        connection.close()
        print("Kapcsolat bezárva.")

def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Lekérdezés végrehajtva sikeresen!")
    except Exception as e:
        print(f"Hiba a lekérdezés során: {e}")
    return cursor, connection  # A kapcsolatot is visszaadjuk