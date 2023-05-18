from abc import ABC, abstractmethod
from pandas import DataFrame


class AbstractBokDataReader(ABC):
    # TODO: add methods and it's output type as dataclasses object
    @abstractmethod
    def get_gdp_by_range(self, from_str: str, to_str: str, period: str) -> DataFrame:
        pass