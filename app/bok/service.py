from app.data_reader.abstracts.AbstractBokDataReader import AbstractBokDataReader
from app.data_reader.concretes.BokDataReader import BokDataReader

from infra.database.alchemy_models.RokGdpSource import RokGdpSource
from infra.database.alchemy_models.RokGdpTarget import RokGdpTarget
from infra.database.connection import SessionManager

from sqlalchemy import insert, select, update, text

from pandas import DataFrame

from io import BytesIO

from datetime import datetime

import matplotlib.pyplot as plt

import platform

# font configuration by operating system
if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Linux':
    plt.rc('font', family='Malgun Gothic')

plt.rcParams['axes.unicode_minus'] = False


class BokService:
    def __init__(self, reader: AbstractBokDataReader):
        self.__reader = reader
        self.__FIRST_STATISTIC_YEAR = '1960'

    def update_target_from_source(self) -> bool:
        session = SessionManager().get_session()

        query_to_fetch_latest_date_from_target = 'SELECT MAX(updated_at) FROM rok_gdp_target;'
        latest_updated_date_row = session.execute(text(query_to_fetch_latest_date_from_target)).fetchone()

        latest_updated_date = latest_updated_date_row._mapping['MAX(updated_at)']

        query_to_fetch_latest_data_from_source = select(RokGdpSource).where(
            RokGdpSource.created_at > latest_updated_date
        )

        record_should_be_updated = session.execute(query_to_fetch_latest_data_from_source).fetchall()

        for record in record_should_be_updated:
            raw_time = record.RokGdpSource.raw_time
            raw_item_code_first = record.RokGdpSource.item_code_first
            changed_data_value = record.RokGdpSource.data_value

            query_to_update_record = update(RokGdpTarget).where(
                RokGdpTarget.raw_time == raw_time,
                RokGdpTarget.item_code_first == raw_item_code_first,
                RokGdpTarget.updated_at == latest_updated_date,
            ).values(data_value=changed_data_value)

            session.execute(query_to_update_record)

        session.commit()

        return True if len(record_should_be_updated) != 0 else False

    def update_source(self):
        session = SessionManager().get_session()

        query_to_fetch_latest_date_from_hour = 'SELECT MAX(created_at) FROM rok_gdp_source;'
        latest_updated_date_row = session.execute(text(query_to_fetch_latest_date_from_hour)).fetchone()
        latest_updated_date = latest_updated_date_row._mapping['MAX(created_at)']

        # 마지막으로 갱신된 지 5시간 이내라면 갱신 작업이 이뤄지지 않도록 처리
        if (datetime.utcnow() - latest_updated_date).total_seconds() / 3600 < 5:
            return False

        current_year_str = str(datetime.now().year)

        gdp_annually = self.get_gdp_by_range(self.__FIRST_STATISTIC_YEAR, current_year_str, 'A')
        gdp_quarterly = self.get_gdp_by_range(f'{self.__FIRST_STATISTIC_YEAR}Q1', f'{current_year_str}Q4', 'Q')

        records_to_insert = []

        for index, record in gdp_annually.iterrows():
            annual = {}

            annual['stat_code'] = record['STAT_CODE']
            annual['stat_name'] = record['STAT_NAME']

            annual['item_code_first'] = record['ITEM_CODE1']
            annual['item_name_first'] = record['ITEM_NAME1']

            annual['unit_name'] = record['UNIT_NAME']
            annual['raw_time'] = record['TIME']

            annual['data_value'] = float(record['DATA_VALUE'])

            records_to_insert.append(annual)

        for index, record in gdp_quarterly.iterrows():
            quarterly = {}

            quarterly['stat_code'] = record['STAT_CODE']
            quarterly['stat_name'] = record['STAT_NAME']

            quarterly['item_code_first'] = record['ITEM_CODE1']
            quarterly['item_name_first'] = record['ITEM_NAME1']

            quarterly['unit_name'] = record['UNIT_NAME']
            quarterly['raw_time'] = record['TIME']

            quarterly['data_value'] = float(record['DATA_VALUE'])

            records_to_insert.append(quarterly)

        session.execute(insert(RokGdpSource), records_to_insert)

        session.commit()

        return True

    def fill_base_data_to_source_and_target(self):
        session = SessionManager().get_session()

        query_to_fetch_num_of_records = 'SELECT COUNT(id) as num_of_record FROM rok_gdp_source;'
        num_of_records_row = session.execute(text(query_to_fetch_num_of_records)).fetchone()
        num_of_records = num_of_records_row._mapping['num_of_record']

        if num_of_records > 0:
            print('data source table is already filled')
            return

        current_year_str = str(datetime.now().year)

        gdp_annually = self.get_gdp_by_range(self.__FIRST_STATISTIC_YEAR, current_year_str, 'A')
        gdp_quarterly = self.get_gdp_by_range(f'{self.__FIRST_STATISTIC_YEAR}Q1', f'{current_year_str}Q4', 'Q')

        records_to_insert = []

        for index, record in gdp_annually.iterrows():
            annual = {}

            annual['stat_code'] = record['STAT_CODE']
            annual['stat_name'] = record['STAT_NAME']

            annual['item_code_first'] = record['ITEM_CODE1']
            annual['item_name_first'] = record['ITEM_NAME1']

            annual['unit_name'] = record['UNIT_NAME']
            annual['raw_time'] = record['TIME']

            annual['data_value'] = float(record['DATA_VALUE'])

            records_to_insert.append(annual)

        for index, record in gdp_quarterly.iterrows():
            quarterly = {}

            quarterly['stat_code'] = record['STAT_CODE']
            quarterly['stat_name'] = record['STAT_NAME']

            quarterly['item_code_first'] = record['ITEM_CODE1']
            quarterly['item_name_first'] = record['ITEM_NAME1']

            quarterly['unit_name'] = record['UNIT_NAME']
            quarterly['raw_time'] = record['TIME']

            quarterly['data_value'] = float(record['DATA_VALUE'])

            records_to_insert.append(quarterly)

        session.execute(insert(RokGdpSource), records_to_insert)
        session.execute(insert(RokGdpTarget), records_to_insert)

        session.commit()

    def get_gdp_by_range(self, from_str: str, to_str: str, period: str):
        return self.__reader.get_gdp_by_range(from_str, to_str, period)

    def draw_gdp_graph_by_data(self, gdp_data: DataFrame) -> BytesIO:
        gdp_data = gdp_data.loc[gdp_data['ITEM_CODE1'] == '1400']
        gdp_data['DATA_VALUE'] = gdp_data['DATA_VALUE'].astype(float)

        plt.plot(gdp_data['TIME'], gdp_data['DATA_VALUE'], color='b', marker='o', linestyle='solid')
        plt.ticklabel_format(axis='y', useOffset=False, style='plain')
        plt.title('GDP 디플레이터(명목)')
        plt.xlabel('연도')
        plt.ylabel('GDP(10억원)')

        buffer = BytesIO()

        plt.savefig(buffer, format='png')

        return buffer


instance = BokService(BokDataReader())
instance.update_source()
