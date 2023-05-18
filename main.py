from app.bok.service import BokService
from app.configuration.environments import ENV_VARIABLES

import discord
from discord.ext import tasks

from app.data_reader.concretes.BokDataReader import BokDataReader

from infra.database.connection import SessionManager

# init database
SessionManager()

# init discord bot
intents = discord.Intents.default()
bot = discord.Bot()

# init service dependencies
concrete_reader = BokDataReader()
instance = BokService(concrete_reader)

# when the program was started
# fill the database at first
instance.fill_base_data_to_source_and_target()


@tasks.loop(hours=24*7)
async def check_updated_gdp_periodically():
    data_fetched = instance.update_source()
    if data_fetched:
        data_updated = instance.update_target_from_source()
        if data_updated:
            channel = bot.get_channel(ENV_VARIABLES['DISCORD_CHANNEL_ID'])
            await channel.send('GDP 가 갱신되었습니다!')


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    if not check_updated_gdp_periodically.is_running():
        check_updated_gdp_periodically.start()


@bot.slash_command(
    name="gdp_graph",
    description="연간 기준 GDP 그래프를 그려줍니다!, 시작년과 종료년을 `,` 로 구분해서 입력해주세요(ex. 2014, 2023)!",
    guild_ids=[ENV_VARIABLES['DISCORD_GUILD_ID']]
)
async def gdp_graph(ctx, value):
    from_year, to_year = list(map(lambda year: str(year).strip(), value.split(',')))
    data = instance.get_gdp_by_range(from_year, to_year, 'A')
    buffer = instance.draw_gdp_graph_by_data(data)
    buffer.seek(0)
    file = discord.File(buffer, filename='gdp.png')
    await ctx.respond(file=file)


bot.run(ENV_VARIABLES['DISCORD_TOKEN'])
