from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:wuhanxxq@localhost/fastapi"

# engine is responsible for establishing a connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# when you actually want to talk to the SQL database, we have to make use of a session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all the models we define to actually create our tables in Postgres, they are going to be extending the base class.
Base = declarative_base()

# the session object is responsible for talking with the databases, get a connection/session to the database
# everytime we get a request, we are going to get a session, and send statements to it.
# after the request is done, we will then close it out.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()