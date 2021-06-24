import os

from dotenv import find_dotenv, load_dotenv

# Load environment variables from '.env' file.
load_dotenv(find_dotenv())

# Redis settings.
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Flask-specific settings.
class Config(object):
    # Flask
    JSON_SORT_KEYS = False
    PREFERRED_URL_SCHEME = "https"
    SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(20)
