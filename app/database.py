from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = settings.database_url
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastpost',
#                                 user='exsan', password='ehsan2404',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection successfull")
#         break
#     except Exception as error:
#         print("Connection failed")
#         print("Error: ", error)
#         time.sleep(2)




# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#             {"title": "favorite charecter", "content": "I LOVE ZLATAN", "id": 2}]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i