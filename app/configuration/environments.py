import os
from typing import TypedDict, cast

from dotenv import load_dotenv


class EnvVariables(TypedDict):
    AUTHOR_KEY: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_ROOT_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str


load_dotenv('../../.env')

AUTHOR_KEY = os.getenv('AUTHOR_KEY')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_ROOT_PASSWORD = os.getenv('DATABASE_ROOT_PASSWORD')

# optional props
DATABASE_HOST = os.getenv('DATABASE_HOST')

DATABASE_PORT = os.getenv('DATABASE_PORT') if os.getenv('DATABASE_PORT') else 3306
DATABASE_NAME = os.getenv('DATABASE_NAME')

validate = {
    'AUTHOR_KEY': AUTHOR_KEY,
    'DATABASE_USERNAME': DATABASE_USERNAME,
    'DATABASE_PASSWORD': DATABASE_PASSWORD,
    'DATABASE_HOST': DATABASE_HOST,
    'DATABASE_ROOT_PASSWORD': DATABASE_ROOT_PASSWORD,
    'DATABASE_PORT': DATABASE_PORT,
    'DATABASE_NAME': DATABASE_NAME,
}

for v in validate:
    if v != 'DATABASE_HOST' and validate[v] is None:
        raise Exception(f"environment variable error: {v} is not valid")

ENV_VARIABLES: EnvVariables = cast(EnvVariables, validate)
