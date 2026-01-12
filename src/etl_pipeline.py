from sqlalchemy import create_engine
from config import DATABASE_URL, SONG_DATA_PATH, LOG_DATA_PATH
from extract import extract_json_data
from transform import transform_song_data, transform_log_data
from load import load_to_db

def run_etl():
    engine = create_engine(DATABASE_URL)
    
    # 1. Song Data
    song_raw = extract_json_data(SONG_DATA_PATH)
    songs_df, artists_df = transform_song_data(song_raw)
    load_to_db(artists_df, 'artists', engine)
    load_to_db(songs_df, 'songs', engine)
    
    # 2. Log Data
    log_raw = extract_json_data(LOG_DATA_PATH)
    time_df, user_df, log_df = transform_log_data(log_raw)
    load_to_db(time_df, 'time', engine)
    load_to_db(user_df, 'users', engine)
    
    # 3. Fact Table Lookup & Load
    log_df = log_df.rename(columns={'song': 'title'})  # Align column names for merge
    songplay_data = log_df.merge(songs_df, on='title', how='left').merge(artists_df, on='artist_id', how='left', suffixes=('', '_artist'))
    songplays_df = songplay_data[[
        'ts', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent'
    ]]
    songplays_df.columns = [
        'start_time', 'user_id', 'level', 'song_id', 'artist_id', 'session_id', 'location', 'user_agent'
    ]
    load_to_db(songplays_df, 'songplays', engine)

if __name__ == "__main__":
    run_etl()