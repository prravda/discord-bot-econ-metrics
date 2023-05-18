from typing import Optional

from sqlalchemy import URL, create_engine
from app.configuration.environments import ENV_VARIABLES
from sqlalchemy.orm import Session
from infra.database.alchemy_models.Base import Base

# Call alchemy models inherit the Base class
from infra.database.alchemy_models.RokGdpSource import RokGdpSource
from infra.database.alchemy_models.RokGdpTarget import RokGdpTarget


class SessionManager:
    def __init__(self):
        self.__session: Optional[Session] = None

    def get_session(self):
        if self.__session is None:
            url_object = URL.create(
                'mariadb+mariadbconnector',
                username=ENV_VARIABLES['DATABASE_USERNAME'],
                password=ENV_VARIABLES['DATABASE_PASSWORD'],
                host=ENV_VARIABLES['DATABASE_HOST'],
                port=3306,
                database=ENV_VARIABLES['DATABASE_NAME'],
            )

            # Create an engine to connect to the database
            engine = create_engine(url_object, echo=True)

            # Create the table using alchemy models
            Base.metadata.create_all(engine)

            # Create a session factory
            self.__session = Session(bind=engine)

        return self.__session
