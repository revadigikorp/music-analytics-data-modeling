"""
Dashboard Data Generator
Generates JSON data files for the analytics dashboard.
"""

import json
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

OUTPUT_DIR = 'dashboard/data'

def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_engine():
    """Create database engine."""
    return create_engine(DATABASE_URL)

def generate_overview_stats(engine):
    """Generate overview statistics."""
    stats = {}
    
    tables = ['users', 'songs', 'artists', 'songplays']
    with engine.connect() as conn:
        for table in tables:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            stats[f'total_{table}'] = count
    
    # Calculate total listening time
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COALESCE(SUM(s.duration), 0) as total_duration
            FROM songplays sp
            JOIN songs s ON sp.song_id = s.song_id
        """)).scalar()
        stats['total_listening_minutes'] = round(result / 60, 1) if result else 0
    
    return stats

def generate_top_songs(engine, limit=10):
    """Generate top played songs data."""
    query = f"""
        SELECT s.title, a.name as artist, COUNT(sp.songplay_id) as plays
        FROM songplays sp
        JOIN songs s ON sp.song_id = s.song_id
        JOIN artists a ON sp.artist_id = a.artist_id
        GROUP BY s.title, a.name
        ORDER BY plays DESC
        LIMIT {limit}
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{'title': row[0], 'artist': row[1], 'plays': row[2]} for row in result]

def generate_top_artists(engine, limit=10):
    """Generate top artists data."""
    query = f"""
        SELECT a.name, COUNT(sp.songplay_id) as plays
        FROM songplays sp
        JOIN artists a ON sp.artist_id = a.artist_id
        GROUP BY a.name
        ORDER BY plays DESC
        LIMIT {limit}
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{'name': row[0], 'plays': row[1]} for row in result]

def generate_hourly_activity(engine):
    """Generate hourly listening activity."""
    query = """
        SELECT t.hour, COUNT(sp.songplay_id) as plays
        FROM songplays sp
        JOIN time t ON sp.start_time = t.start_time
        GROUP BY t.hour
        ORDER BY t.hour
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        # Fill in all 24 hours
        hourly = {i: 0 for i in range(24)}
        for row in result:
            hourly[row[0]] = row[1]
        return [{'hour': h, 'plays': p} for h, p in hourly.items()]

def generate_daily_activity(engine):
    """Generate daily listening activity (by weekday)."""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    query = """
        SELECT t.weekday, COUNT(sp.songplay_id) as plays
        FROM songplays sp
        JOIN time t ON sp.start_time = t.start_time
        GROUP BY t.weekday
        ORDER BY t.weekday
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        daily = {i: 0 for i in range(7)}
        for row in result:
            daily[row[0]] = row[1]
        return [{'day': days[d], 'plays': p} for d, p in daily.items()]

def generate_user_levels(engine):
    """Generate subscription level distribution."""
    query = """
        SELECT level, COUNT(*) as count
        FROM users
        GROUP BY level
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{'level': row[0].capitalize(), 'count': row[1]} for row in result]

def generate_top_locations(engine, limit=5):
    """Generate top listening locations."""
    query = f"""
        SELECT location, COUNT(*) as plays
        FROM songplays
        WHERE location IS NOT NULL
        GROUP BY location
        ORDER BY plays DESC
        LIMIT {limit}
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{'location': row[0], 'plays': row[1]} for row in result]

def generate_recent_activity(engine, limit=10):
    """Generate recent listening activity."""
    query = f"""
        SELECT sp.start_time, u.first_name, u.last_name, s.title, a.name as artist
        FROM songplays sp
        JOIN users u ON sp.user_id = u.user_id
        JOIN songs s ON sp.song_id = s.song_id
        JOIN artists a ON sp.artist_id = a.artist_id
        ORDER BY sp.start_time DESC
        LIMIT {limit}
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [{
            'time': row[0].strftime('%Y-%m-%d %H:%M'),
            'user': f"{row[1]} {row[2]}",
            'song': row[3],
            'artist': row[4]
        } for row in result]

def generate_all_data():
    """Generate all dashboard data files."""
    ensure_output_dir()
    engine = get_engine()
    
    print("🎵 Generating dashboard data...")
    
    # Generate all data
    data = {
        'overview': generate_overview_stats(engine),
        'topSongs': generate_top_songs(engine),
        'topArtists': generate_top_artists(engine),
        'hourlyActivity': generate_hourly_activity(engine),
        'dailyActivity': generate_daily_activity(engine),
        'userLevels': generate_user_levels(engine),
        'topLocations': generate_top_locations(engine),
        'recentActivity': generate_recent_activity(engine),
        'generatedAt': __import__('datetime').datetime.now().isoformat()
    }
    
    # Write combined data file
    output_file = os.path.join(OUTPUT_DIR, 'dashboard_data.json')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Dashboard data saved to {output_file}")
    return data

if __name__ == "__main__":
    generate_all_data()
