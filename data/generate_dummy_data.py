import os
import json

# Define directory paths
SONG_DATA_PATH = 'data/song_data'
LOG_DATA_PATH = 'data/log_data'

# Ensure directories exist
os.makedirs(SONG_DATA_PATH, exist_ok=True)
os.makedirs(LOG_DATA_PATH, exist_ok=True)

# Sample Song Data
songs = [
    {
        "num_songs": 1, "artist_id": "ARJNIQD1187FB3E113", "artist_latitude": None, 
        "artist_longitude": None, "artist_location": "", "artist_name": "Gipsy Kings", 
        "song_id": "SOYMRWW12A6D4FAB14", "title": "The Ocean", "duration": 235.44118, "year": 1982
    },
    {
        "num_songs": 1, "artist_id": "ARMJAGH1187FB546F3", "artist_latitude": 35.14968, 
        "artist_longitude": -90.04892, "artist_location": "Memphis, TN", "artist_name": "The Box Tops", 
        "song_id": "SOCIWDW12A8C13D406", "title": "Soul Deep", "duration": 148.03546, "year": 1969
    }
]

# Sample Log Data
logs = [
    {
        "artist": "Gipsy Kings", "auth": "Logged In", "firstName": "Kaylee", "gender": "F", 
        "itemInSession": 0, "lastName": "Summers", "length": 235.44118, "level": "free", 
        "location": "Phoenix-Mesa-Scottsdale, AZ", "method": "PUT", "page": "NextSong", 
        "registration": 1540344794796.0, "sessionId": 139, "song": "The Ocean", "status": 200, 
        "ts": 1541106106796, "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36", "userId": "8"
    },
    {
        "artist": "The Box Tops", "auth": "Logged In", "firstName": "Kaylee", "gender": "F", 
        "itemInSession": 1, "lastName": "Summers", "length": 148.03546, "level": "free", 
        "location": "Phoenix-Mesa-Scottsdale, AZ", "method": "PUT", "page": "NextSong", 
        "registration": 1540344794796.0, "sessionId": 139, "song": "Soul Deep", "status": 200, 
        "ts": 1541106341796, "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36", "userId": "8"
    }
]

# Write Song Data Files
for i, song in enumerate(songs):
    with open(os.path.join(SONG_DATA_PATH, f'song_{i}.json'), 'w') as f:
        json.dump(song, f)

# Write Log Data Files
with open(os.path.join(LOG_DATA_PATH, '2018-11-01-events.json'), 'w') as f:
    for entry in logs:
        f.write(json.dumps(entry) + '\n')

print(f"Generated {len(songs)} song files in {SONG_DATA_PATH}")
print(f"Generated 1 log file in {LOG_DATA_PATH}")