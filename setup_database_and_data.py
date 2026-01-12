import os
import json
import psycopg2
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 1. Load configuration
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
SONG_DATA_PATH = 'data/song_data'
LOG_DATA_PATH = 'data/log_data'

def setup():
    # Ensure directories exist
    os.makedirs(SONG_DATA_PATH, exist_ok=True)
    os.makedirs(LOG_DATA_PATH, exist_ok=True)

    # 2. Create Tables using SQLAlchemy (No psql tool needed!)
    print("Connecting to database to create tables...")
    engine = create_engine(DATABASE_URL)
    
    # Read SQL files
    with open('sql/drop_tables.sql', 'r') as f:
        drop_query = f.read()
    with open('sql/create_tables.sql', 'r') as f:
        create_query = f.read()

    with engine.connect() as conn:
        conn.execute(text(drop_query))
        conn.execute(text(create_query))
        conn.commit()
    print("✅ Tables dropped and recreated successfully.")

    # 3. Generate Dummy Data
    print("Generating sample JSON data...")
    songs = [
        {"num_songs": 1, "artist_id": "ARJNIQD", "artist_name": "Gipsy Kings", "artist_location": "", "artist_latitude": None, "artist_longitude": None, "song_id": "SOYMRWW", "title": "The Ocean", "duration": 235, "year": 1982},
        {"num_songs": 1, "artist_id": "ARMJAGH", "artist_name": "The Box Tops", "artist_location": "Memphis, TN", "artist_latitude": 35.14968, "artist_longitude": -90.04892, "song_id": "SOCIWDW", "title": "Soul Deep", "duration": 148, "year": 1969}
    ]
    
    logs = [
        {"artist": "Gipsy Kings", "firstName": "Kaylee", "lastName": "Summers", "gender": "F", "level": "free", "location": "Phoenix-Mesa-Scottsdale, AZ", "page": "NextSong", "sessionId": 139, "song": "The Ocean", "ts": 1541106106796, "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36", "userId": "8"},
        {"artist": "The Box Tops", "firstName": "Kaylee", "lastName": "Summers", "gender": "F", "level": "free", "location": "Phoenix-Mesa-Scottsdale, AZ", "page": "NextSong", "sessionId": 139, "song": "Soul Deep", "ts": 1541106341796, "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36", "userId": "8"}
    ]

    for i, song in enumerate(songs):
        with open(os.path.join(SONG_DATA_PATH, f'song_{i}.json'), 'w') as f:
            json.dump(song, f)

    with open(os.path.join(LOG_DATA_PATH, 'events.json'), 'w') as f:
        for entry in logs:
            f.write(json.dumps(entry) + '\n')
    
    print(f"✅ Dummy data created in {SONG_DATA_PATH} and {LOG_DATA_PATH}")

if __name__ == "__main__":
    setup()