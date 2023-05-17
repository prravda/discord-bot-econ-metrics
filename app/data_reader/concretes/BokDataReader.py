from PublicDataReader import Ecos
from pandas import DataFrame

from app.configuration.bok_stat_codetable import BOK_STAT_CODETABLE
from app.data_reader.abstracts.AbstractBokDataReader import AbstractBokDataReader
from app.configuration.environments import ENV_VARIABLES


class BokDataReader(AbstractBokDataReader):
    def __init__(self):
        self.__api = Ecos(ENV_VARIABLES['AUTHOR_KEY'])

    # TODO: implement input validator
    def validate_input(self, from_str: str, to_str: str, period: str):
        try:
            pass

        except Exception as e:
            print(e)

    def get_gdp_by_range(self, from_str: str, to_str: str, period: str) -> DataFrame:
        try:
            self.validate_input(from_str, to_str, period)

            result = self.__api.get_statistic_search(
                통계표코드=BOK_STAT_CODETABLE['GDP'],
                주기=period,
                검색시작일자=from_str,
                검색종료일자=to_str,
            )

            # TODO: If there are any error message, contain this error instance
            if result is not None and not result.empty:
                return result

            else:
                raise Exception('GDP 정보가 조회되지 않았습니다. 자세한 오류를 확인해주세요.')

        except Exception as e:
            print(e)
