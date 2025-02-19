import os
from dotenv import load_dotenv

load_dotenv()

bot_key = os.environ.get("bot_key")

DB_HOST = os.environ.get("DB_HOST")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT", 3306)
NOTICE_DB_NAME = os.environ.get("NOTICE_DB_NAME")

RSS_FEED_URL = os.environ.get("RSS_FEED_URL")
MAX_DB_SIZE = os.environ.get("MAX_DB_SIZE")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
ASK_CHANNEL_ID = os.environ.get("ASK_CHANNEL_ID")