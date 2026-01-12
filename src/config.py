import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SONG_DATA_PATH = 'data/song_data'
LOG_DATA_PATH = 'data/log_data'