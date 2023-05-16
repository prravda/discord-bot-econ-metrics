from sqlalchemy import URL, create_engine
from sqlalchemy import create_engine, Column, Integer, String
from app.configuration.environments import ENV_VARIABLES
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url_object = URL.create(
    'mariadb+mariadbconnector',
    username=ENV_VARIABLES['DATABASE_USERNAME'],
    password=ENV_VARIABLES['DATABASE_PASSWORD'],
    host=ENV_VARIABLES['DATABASE_HOST'],
    port=ENV_VARIABLES['DATABASE_PORT'],
    database=ENV_VARIABLES['DATABASE_NAME'],
)

# Create an engine to connect to the database
engine = create_engine(url_object, echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()


# Define a model class representing the table
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))


# Create the table in the database
Base.metadata.create_all(engine)

# Create a session
session = Session()


def test():
    # Insert a record using the query builder
    user = User(name='John Doe', email='john@example.com')
    session.add(user)
    session.commit()

    # Query data using the query builder
    query = session.query(User).filter(User.name == 'John Doe')
    result = query.all()

    # Print the retrieved records
    for row in result:
        print(f"ID: {row.id}, Name: {row.name}, Email: {row.email}")

    # Close the session
    session.close()
