import os
from typing import TypedDict, cast

from dotenv import load_dotenv, find_dotenv


class EnvVariables(TypedDict):
    DISCORD_TOKEN: str
    DISCORD_GUILD_ID: int
    DISCORD_CHANNEL_ID: int

    AUTHOR_KEY: str

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_ROOT_PASSWORD: str
    DATABASE_NAME: str


load_dotenv(find_dotenv())

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

AUTHOR_KEY = os.getenv('AUTHOR_KEY')

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_ROOT_PASSWORD = os.getenv('DATABASE_ROOT_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

validate = {
    'DISCORD_TOKEN': DISCORD_TOKEN,
    'DISCORD_GUILD_ID': int(DISCORD_GUILD_ID),
    'DISCORD_CHANNEL_ID': int(DISCORD_CHANNEL_ID),
    'AUTHOR_KEY': AUTHOR_KEY,
    'DATABASE_HOST': DATABASE_HOST,
    'DATABASE_USERNAME': DATABASE_USERNAME,
    'DATABASE_PASSWORD': DATABASE_PASSWORD,
    'DATABASE_ROOT_PASSWORD': DATABASE_ROOT_PASSWORD,
    'DATABASE_NAME': DATABASE_NAME,
}

for v in validate:
    if validate[v] is None:
        raise Exception(f"environment variable error: {v} is not valid")

ENV_VARIABLES = cast(EnvVariables, validate)
