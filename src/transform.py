import pandas as pd

def transform_song_data(df):
    song_cols = ['song_id', 'title', 'artist_id', 'year', 'duration']
    artist_cols = ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    
    songs_df = df[song_cols].drop_duplicates()
    artists_df = df[artist_cols].drop_duplicates()
    artists_df.columns = ['artist_id', 'name', 'location', 'latitude', 'longitude']
    
    return songs_df, artists_df

def transform_log_data(df):
    df = df[df['page'] == 'NextSong'].copy()
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    t = df['ts']
    time_data = (t, t.dt.hour, t.dt.day, t.dt.isocalendar().week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(dict(zip(column_labels, time_data))).drop_duplicates()
    
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates()
    user_df.columns = ['user_id', 'first_name', 'last_name', 'gender', 'level']
    
    return time_df, user_df, df