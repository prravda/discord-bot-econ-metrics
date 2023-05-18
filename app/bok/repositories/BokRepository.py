from sqlalchemy.orm import Session

from app.bok.repositories.AbstractBokRepository import AbstractBokRepository


class BokRepository(AbstractBokRepository):
    def __init__(self, session: Session):
        self.__session = session

    def save_gdp_by_period(self):
        pass
