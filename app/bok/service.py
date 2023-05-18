from app.data_reader.abstracts.AbstractBokDataReader import AbstractBokDataReader

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

    def get_latest_annual_gdp_from_now(self):
        current_year = datetime.now().year

        from_year = str(current_year - 2)
        to_year = str(current_year + 1)

        result = self.__reader.get_gdp_by_range(from_year, to_year, 'A')

        gdp_rows = result.loc[result['ITEM_CODE1'] == '1400']

        return gdp_rows.iloc[-1]

    def check_updated_value(self):
        current_year = datetime.now().year

        latest_data_from_now = self.get_latest_annual_gdp_from_now()

        if latest_data_from_now['TIME'] and int(latest_data_from_now['TIME']) >= current_year:
            return True

        return False

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
