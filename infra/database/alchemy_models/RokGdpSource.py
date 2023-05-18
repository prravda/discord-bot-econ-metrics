from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from infra.database.alchemy_models.Base import Base


class RokGdpSource(Base):
    __tablename__ = 'rok_gdp_source'

    id = Column(Integer, primary_key=True)
    stat_code = Column(String(50))
    stat_name = Column(String(100))

    item_code_first = Column(Integer)
    item_name_first = Column(String(50))

    item_code_second = Column(String(50), nullable=True)
    item_name_second = Column(String(50), nullable=True)

    item_code_third = Column(String(50), nullable=True)
    item_name_third = Column(String(50), nullable=True)

    item_code_fourth = Column(String(50), nullable=True)
    item_name_fourth = Column(String(50), nullable=True)

    unit_name = Column(String(50))

    raw_time = Column(String(50))

    data_value = Column(Float)

    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f'id = {self.id}, status_code = {self.stat_code}, ' \
               f'status_name = {self.stat_code}, ' \
               f'item_code_first = {self.item_code_first}, item_name_first = {self.item_name_first} ' \
               f'item_code_second = {self.item_code_second}, item_name_second = {self.item_name_second} ' \
               f'item_code_third = {self.item_code_third}, item_name_third = {self.item_name_third} ' \
               f'item_code_fourth = {self.item_code_fourth}, item_name_fourth = {self.item_name_fourth} ' \
               f'unit_name = {self.unit_name}, raw_time = {self.raw_time}, data_value = {self.data_value}'