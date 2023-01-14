from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:yasirhome@localhost/fastapi"

# Engine is rsponsible for connecting with database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# to communicate with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# all the model will be extending by this base class
Base = declarative_base()

# dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                                 user='postgres', password='yasirhome', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successfully!")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error:", error)
#         time.sleep(2)
