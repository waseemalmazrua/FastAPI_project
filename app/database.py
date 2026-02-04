from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
import time 
from app.config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False , autoflush=False,bind=engine)

Base = declarative_base()



def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:


#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='Wasiem123456',
#                                 port='8000',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection was successful")
#         break
#     except Exception as error:
#         print("connection to database failed")
#         print("error:", error)
#         time.sleep(2)