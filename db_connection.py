# db_connection.py
import os
import psycopg2

def get_connection():
    """
    Returns a psycopg2 connection. Configure via environment variables:
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
    """
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "etl_data")
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASS = os.environ.get("DB_PASS", "damilare")

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn