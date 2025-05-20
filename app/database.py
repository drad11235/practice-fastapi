from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# specify the connection string / location of the PostgreSQL database / a URL for SQLAlchemy to use...
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine connects sqlalchemy to the postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# talk to the database via a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class; all models later defined to create the Postgres tables will be extensions (i.e. inheritance) from this etc.
Base = declarative_base()


# the session object is responsible for talking to the database; the "dependency" function get_db is an efficient way to create 
#  a session connection to the db - each and every time there is a REQUEST to any of our API ENDPOINTS - this will result in a 
#  SESSION and enable the transmission of SQL statements for any of our PATH OPERATIONS i.e. ultimately via the psycopg2 driver 
# to the database.
# this function is therefore passed in as a parameter to each path operation to create the session to the db and then
#  close the session once the REQUEST / operation has been carried out...
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# cursor factory -> adds the column names to the values when executing a query
# the code below was used for raw SQL i.e. early in development, before SQLAlchemy was used.
# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='9!Rd!37jkMN!2', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)

