from PublicDataReader import Ecos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from app.configuration.environments import ENV_VARIABLES


class BokService:
    def __int__(self):
        pass

    def get_gdp(self):
        print(ENV_VARIABLES["AUTHOR_KEY"])
        api = Ecos(ENV_VARIABLES["AUTHOR_KEY"])

        df_gdp = api.get_statistic_search(
            통계표코드='200Y005',
            주기='A',
            검색시작일자='2015',
            검색종료일자='2022',
        )

        gdp_year = df_gdp[df_gdp['통계항목명1'] == '국내총생산(시장가격, GDP)']
        gdp_year = gdp_year[['시점', '값']]
        gdp_year['값'] = gdp_year['값'].astype(float)

        plt.plot(gdp_year['시점'], gdp_year['값'], color='b', marker='o', linestyle='solid')
        plt.ticklabel_format(axis='y', useOffset=False, style='plain')
        plt.title('GDP 디플레이터 (명목)')
        plt.xlabel('연도')
        plt.ylabel('GDP(10억원)')
        plt.savefig('KoreanBank_GDP.png')

    def polling_gdp(self) -> None:
        """
        한국은행 GDP 정보를 일정 간격마다 호출하는 함수입니다.
        :return: None
        """

    def is_there_updated_gdp(self) -> bool:
        """
        한국은행 정보 중, 호출 시점을 기준으로 GDP 정보가 존재하는지 여부를 반환합니다.
        :return:
        """



instance = BokService()
instance.get_gdp()
