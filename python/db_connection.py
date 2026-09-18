import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 5432)),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(connection_url)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))

            print("PostgreSQL connection successful!")
            print(result.fetchone()[0])

    except Exception as e:
        print("PostgreSQL connection failed:")
        print(e)


if __name__ == "__main__":
    test_connection()