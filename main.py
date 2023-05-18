from app.bok.service import BokService
from app.configuration.environments import ENV_VARIABLES

import discord
from discord.ext import tasks

from app.data_reader.concretes.BokDataReader import BokDataReader

from datetime import datetime

from infra.database.connection import SessionManager

# init database
SessionManager()

# init discord bot
intents = discord.Intents.default()
bot = discord.Bot()

# init service dependencies
concrete_reader = BokDataReader()
instance = BokService(concrete_reader)


@tasks.loop(hours=24)
async def check_updated_annual_gdp_periodically():
    if instance.check_updated_value():
        channel = bot.get_channel(1052239870912893011)
        await channel.send(f'{datetime.now()} 기준 갱신된 GDP data 가 있어요!')


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    check_updated_annual_gdp_periodically.start()


@bot.slash_command(name="gdp_graph", description="연간 기준 GDP 그래프를 그려줍니다!, 시작년과 종료년을 `,` 로 구분해서 입력해주세요(ex. 2014, 2023)!",
                   guild_ids=[1052239870912893008])
async def gdp_graph(ctx, value):
    from_year, to_year = list(map(lambda year: str(year).strip(), value.split(',')))
    data = instance.get_gdp_by_range(from_year, to_year, 'A')
    buffer = instance.draw_gdp_graph_by_data(data)
    buffer.seek(0)
    file = discord.File(buffer, filename='gdp.png')
    await ctx.respond(file=file)


bot.run(ENV_VARIABLES['DISCORD_TOKEN'])
