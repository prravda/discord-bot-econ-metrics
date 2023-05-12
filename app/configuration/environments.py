import os
from dotenv import load_dotenv

load_dotenv('../../.env')

AUTHOR_KEY = os.getenv('AUTHOR_KEY')

ENV_VARIABLES = {
    "AUTHOR_KEY": AUTHOR_KEY,
}