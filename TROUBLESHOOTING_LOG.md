# Music Analytics Data Modeling - Troubleshooting Log

**Date:** January 12, 2026  
**Author:** Antigravity AI Assistant

---

## Overview

This document details the issues encountered while setting up and running the Music Analytics Data Modeling ETL pipeline, along with the fixes applied to resolve them.

---

## Issue #1: Database Connection Failure

### Symptom
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection refused
```

### Root Cause
Two problems:
1. PostgreSQL database container was not running
2. Credentials in `.env` did not match `docker-compose.yml` configuration

| File | Setting | Value |
|------|---------|-------|
| `.env` (before) | Credentials | `student:student_password` / `music_streaming` |
| `docker-compose.yml` | Credentials | `music:music` / `musicdb` |

### Fix Applied

**File:** `.env`
```diff
- DATABASE_URL=postgresql://student:student_password@localhost:5432/music_streaming
+ DATABASE_URL=postgresql://music:music@localhost:5432/musicdb
```

**Command:** Started the database container
```powershell
docker compose up -d
```

---

## Issue #2: Missing Artist Columns in Song Data

### Symptom
```
KeyError: "['artist_location', 'artist_latitude', 'artist_longitude'] not in index"
```

### Root Cause
The `transform_song_data()` function in `src/transform.py` expected these columns for the artists table:
- `artist_location`
- `artist_latitude`
- `artist_longitude`

However, `setup_database_and_data.py` was generating song data without these fields.

### Fix Applied

**File:** `setup_database_and_data.py` (lines 36-39)
```diff
  songs = [
-     {"num_songs": 1, "artist_id": "ARJNIQD", "artist_name": "Gipsy Kings", "song_id": "SOYMRWW", "title": "The Ocean", "duration": 235, "year": 1982},
-     {"num_songs": 1, "artist_id": "ARMJAGH", "artist_name": "The Box Tops", "song_id": "SOCIWDW", "title": "Soul Deep", "duration": 148, "year": 1969}
+     {"num_songs": 1, "artist_id": "ARJNIQD", "artist_name": "Gipsy Kings", "artist_location": "", "artist_latitude": None, "artist_longitude": None, "song_id": "SOYMRWW", "title": "The Ocean", "duration": 235, "year": 1982},
+     {"num_songs": 1, "artist_id": "ARMJAGH", "artist_name": "The Box Tops", "artist_location": "Memphis, TN", "artist_latitude": 35.14968, "artist_longitude": -90.04892, "song_id": "SOCIWDW", "title": "Soul Deep", "duration": 148, "year": 1969}
  ]
```

---

## Issue #3: Missing Log Data Columns

### Symptom
```
KeyError: "['lastName'] not in index"
```
(and similar errors for `location`, `userAgent`)

### Root Cause
The `transform_log_data()` function and ETL pipeline expected these columns in log data:
- `lastName` (for users table)
- `location` (for songplays table)
- `userAgent` (for songplays table)

The generated log data was missing these fields.

### Fix Applied

**File:** `setup_database_and_data.py` (lines 41-44)
```diff
  logs = [
-     {"artist": "Gipsy Kings", "firstName": "Kaylee", "gender": "F", "level": "free", "page": "NextSong", "sessionId": 139, "song": "The Ocean", "ts": 1541106106796, "userId": "8"},
-     {"artist": "The Box Tops", "firstName": "Kaylee", "gender": "F", "level": "free", "page": "NextSong", "sessionId": 139, "song": "Soul Deep", "ts": 1541106341796, "userId": "8"}
+     {"artist": "Gipsy Kings", "firstName": "Kaylee", "lastName": "Summers", "gender": "F", "level": "free", "location": "Phoenix-Mesa-Scottsdale, AZ", "page": "NextSong", "sessionId": 139, "song": "The Ocean", "ts": 1541106106796, "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36", "userId": "8"},
+     {"artist": "The Box Tops", "firstName": "Kaylee", "lastName": "Summers", "gender": "F", "level": "free", "location": "Phoenix-Mesa-Scottsdale, AZ", "page": "NextSong", "sessionId": 139, "song": "Soul Deep", "ts": 1541106341796, "userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36", "userId": "8"}
  ]
```

---

## Issue #4: Column Name Mismatch During Merge

### Symptom
```
KeyError: 'title'
```

### Root Cause
In `src/etl_pipeline.py`, the songplays fact table was being built by merging:
- `log_df` (has column `song`)
- `songs_df` (has column `title`)

The merge was on `'title'`, but log data uses `'song'` for the song name.

### Fix Applied

**File:** `src/etl_pipeline.py` (line 23)
```diff
  # 3. Fact Table Lookup & Load
+ log_df = log_df.rename(columns={'song': 'title'})  # Align column names for merge
  songplay_data = log_df.merge(songs_df, on='title', how='left')...
```

---

## Issue #5: Duplicate Column Names After Merge

### Symptom
```
KeyError: "['location'] not in index"
```

### Root Cause
After merging `log_df` with `artists_df`, both DataFrames had a `location` column:
- `log_df.location` → User's listening location (e.g., "Phoenix-Mesa-Scottsdale, AZ")
- `artists_df.location` → Artist's location (e.g., "Memphis, TN")

Pandas automatically renamed these to `location_x` and `location_y`, breaking the column selection.

### Fix Applied

**File:** `src/etl_pipeline.py` (line 24)
```diff
- songplay_data = log_df.merge(songs_df, on='title', how='left').merge(artists_df, on='artist_id', how='left')
+ songplay_data = log_df.merge(songs_df, on='title', how='left').merge(artists_df, on='artist_id', how='left', suffixes=('', '_artist'))
```

This ensures the log's `location` column keeps its original name while the artist's location becomes `location_artist`.

---

## Verification

After all fixes, the ETL pipeline ran successfully:

```powershell
python setup_database_and_data.py
# ✅ Tables dropped and recreated successfully.
# ✅ Dummy data created in data/song_data and data/log_data

$env:PYTHONPATH = "src"; python src/etl_pipeline.py
# ✅ No errors
```

### Data Loaded:
| Table | Records |
|-------|---------|
| artists | 2 (Gipsy Kings, The Box Tops) |
| songs | 2 (The Ocean, Soul Deep) |
| users | 1 (Kaylee Summers) |
| time | 2 (timestamps) |
| songplays | 2 (fact records) |

---

## Files Modified

| File | Changes |
|------|---------|
| `.env` | Fixed DATABASE_URL credentials |
| `setup_database_and_data.py` | Added missing columns to song and log data |
| `src/etl_pipeline.py` | Fixed column rename and merge suffix handling |

---

## Lessons Learned

1. **Always verify configuration consistency** - Credentials in `.env` must match the actual database configuration in `docker-compose.yml`.

2. **Schema-driven data generation** - When generating test data, ensure all columns required by the transform layer are included.

3. **Be mindful of column name collisions** - When merging DataFrames with overlapping column names, use the `suffixes` parameter to control naming.

4. **Test incrementally** - Running setup and ETL separately helps isolate where failures occur.
