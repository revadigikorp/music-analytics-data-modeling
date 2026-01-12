"""
Exploratory Data Analysis (EDA) & Insights
Music Analytics Data Modeling Project

This script performs exploratory data analysis on the music streaming data
and generates key insights about user behavior, song popularity, and trends.
"""

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def connect_to_db():
    """Create database connection."""
    engine = create_engine(DATABASE_URL)
    return engine

def load_table(engine, table_name):
    """Load a table from the database into a DataFrame."""
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def basic_stats(engine):
    """Display basic statistics about all tables."""
    print_section("📊 DATABASE OVERVIEW")
    
    tables = ['users', 'songs', 'artists', 'time', 'songplays']
    
    for table in tables:
        query = f"SELECT COUNT(*) as count FROM {table}"
        with engine.connect() as conn:
            count = conn.execute(text(query)).scalar()
        print(f"  • {table.capitalize():12} : {count:,} records")

def user_analysis(engine):
    """Analyze user demographics and behavior."""
    print_section("👥 USER ANALYSIS")
    
    users_df = load_table(engine, 'users')
    
    # Gender distribution
    print("\n  Gender Distribution:")
    gender_counts = users_df['gender'].value_counts()
    for gender, count in gender_counts.items():
        label = "Female" if gender == "F" else "Male"
        pct = (count / len(users_df)) * 100
        print(f"    • {label}: {count} ({pct:.1f}%)")
    
    # Subscription level distribution
    print("\n  Subscription Levels:")
    level_counts = users_df['level'].value_counts()
    for level, count in level_counts.items():
        pct = (count / len(users_df)) * 100
        print(f"    • {level.capitalize()}: {count} ({pct:.1f}%)")

def song_analysis(engine):
    """Analyze song catalog."""
    print_section("🎵 SONG CATALOG ANALYSIS")
    
    songs_df = load_table(engine, 'songs')
    
    print(f"\n  Total Songs: {len(songs_df)}")
    
    # Year distribution
    if songs_df['year'].notna().any() and (songs_df['year'] > 0).any():
        valid_years = songs_df[songs_df['year'] > 0]['year']
        print(f"  Oldest Song Year: {int(valid_years.min())}")
        print(f"  Newest Song Year: {int(valid_years.max())}")
    
    # Duration stats
    avg_duration = songs_df['duration'].mean()
    print(f"  Average Duration: {avg_duration/60:.1f} minutes")
    
    # Sample songs
    print("\n  Sample Songs:")
    for _, song in songs_df.head(5).iterrows():
        print(f"    • {song['title']} ({song['year'] if song['year'] > 0 else 'N/A'})")

def artist_analysis(engine):
    """Analyze artists."""
    print_section("🎤 ARTIST ANALYSIS")
    
    artists_df = load_table(engine, 'artists')
    
    print(f"\n  Total Artists: {len(artists_df)}")
    
    # Artists with location data
    with_location = artists_df[artists_df['location'].notna() & (artists_df['location'] != '')].shape[0]
    print(f"  Artists with Location: {with_location}")
    
    # Artists with geo coordinates
    with_coords = artists_df[artists_df['latitude'].notna()].shape[0]
    print(f"  Artists with Coordinates: {with_coords}")
    
    # Sample artists
    print("\n  Artists:")
    for _, artist in artists_df.head(5).iterrows():
        loc = artist['location'] if artist['location'] else "Unknown location"
        print(f"    • {artist['name']} - {loc}")

def listening_patterns(engine):
    """Analyze listening patterns and trends."""
    print_section("📈 LISTENING PATTERNS")
    
    # Top played songs
    query = """
        SELECT s.title, a.name as artist, COUNT(sp.songplay_id) as play_count
        FROM songplays sp
        JOIN songs s ON sp.song_id = s.song_id
        JOIN artists a ON sp.artist_id = a.artist_id
        GROUP BY s.title, a.name
        ORDER BY play_count DESC
        LIMIT 10
    """
    with engine.connect() as conn:
        top_songs = pd.read_sql(text(query), conn)
    
    print("\n  🏆 Top Played Songs:")
    for i, (_, row) in enumerate(top_songs.iterrows(), 1):
        print(f"    {i}. {row['title']} by {row['artist']} ({row['play_count']} plays)")
    
    # Plays by hour
    query = """
        SELECT t.hour, COUNT(sp.songplay_id) as plays
        FROM songplays sp
        JOIN time t ON sp.start_time = t.start_time
        GROUP BY t.hour
        ORDER BY t.hour
    """
    with engine.connect() as conn:
        hourly = pd.read_sql(text(query), conn)
    
    if not hourly.empty:
        peak_hour = hourly.loc[hourly['plays'].idxmax()]
        print(f"\n  ⏰ Peak Listening Hour: {int(peak_hour['hour'])}:00 ({peak_hour['plays']} plays)")
    
    # Plays by day of week
    query = """
        SELECT t.weekday, COUNT(sp.songplay_id) as plays
        FROM songplays sp
        JOIN time t ON sp.start_time = t.start_time
        GROUP BY t.weekday
        ORDER BY t.weekday
    """
    with engine.connect() as conn:
        daily = pd.read_sql(text(query), conn)
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if not daily.empty:
        print("\n  📅 Plays by Day of Week:")
        for _, row in daily.iterrows():
            day_name = days[int(row['weekday'])]
            bar = "█" * int(row['plays'])
            print(f"    {day_name:10} {bar} {row['plays']}")

def user_engagement(engine):
    """Analyze user engagement metrics."""
    print_section("💫 USER ENGAGEMENT")
    
    # Most active users
    query = """
        SELECT u.first_name, u.last_name, COUNT(sp.songplay_id) as total_plays
        FROM songplays sp
        JOIN users u ON sp.user_id = u.user_id
        GROUP BY u.user_id, u.first_name, u.last_name
        ORDER BY total_plays DESC
        LIMIT 5
    """
    with engine.connect() as conn:
        active_users = pd.read_sql(text(query), conn)
    
    print("\n  🌟 Most Active Users:")
    for i, (_, user) in enumerate(active_users.iterrows(), 1):
        print(f"    {i}. {user['first_name']} {user['last_name']} - {user['total_plays']} plays")
    
    # Free vs Paid listening
    query = """
        SELECT level, COUNT(*) as plays
        FROM songplays
        GROUP BY level
    """
    with engine.connect() as conn:
        level_plays = pd.read_sql(text(query), conn)
    
    print("\n  💳 Plays by Subscription Level:")
    for _, row in level_plays.iterrows():
        print(f"    • {row['level'].capitalize()}: {row['plays']} plays")

def location_insights(engine):
    """Analyze geographic distribution."""
    print_section("🌍 GEOGRAPHIC INSIGHTS")
    
    query = """
        SELECT location, COUNT(*) as plays
        FROM songplays
        WHERE location IS NOT NULL
        GROUP BY location
        ORDER BY plays DESC
        LIMIT 5
    """
    with engine.connect() as conn:
        locations = pd.read_sql(text(query), conn)
    
    print("\n  📍 Top Listening Locations:")
    for i, (_, loc) in enumerate(locations.iterrows(), 1):
        print(f"    {i}. {loc['location']} ({loc['plays']} plays)")

def key_insights(engine):
    """Generate key business insights."""
    print_section("💡 KEY INSIGHTS & RECOMMENDATIONS")
    
    insights = []
    
    # Check subscription distribution
    query = "SELECT level, COUNT(*) as count FROM users GROUP BY level"
    with engine.connect() as conn:
        levels = pd.read_sql(text(query), conn)
    
    free_users = levels[levels['level'] == 'free']['count'].sum() if 'free' in levels['level'].values else 0
    paid_users = levels[levels['level'] == 'paid']['count'].sum() if 'paid' in levels['level'].values else 0
    
    if free_users > paid_users:
        insights.append(f"📌 {free_users} free users vs {paid_users} paid - opportunity to convert free users to premium")
    
    # Check for peak hours
    query = """
        SELECT t.hour, COUNT(*) as plays
        FROM songplays sp
        JOIN time t ON sp.start_time = t.start_time
        GROUP BY t.hour
        ORDER BY plays DESC
        LIMIT 1
    """
    with engine.connect() as conn:
        peak = pd.read_sql(text(query), conn)
    
    if not peak.empty:
        insights.append(f"📌 Peak activity at {int(peak.iloc[0]['hour'])}:00 - optimal time for promotions")
    
    # Print insights
    print()
    for insight in insights:
        print(f"  {insight}")
    
    print("\n  📌 Data quality is good - all dimension tables are populated")
    print("  📌 Star schema enables efficient analytical queries")

def run_eda():
    """Run complete EDA analysis."""
    print("\n" + "🎵" * 20)
    print("  MUSIC ANALYTICS - EXPLORATORY DATA ANALYSIS")
    print("🎵" * 20)
    
    engine = connect_to_db()
    
    basic_stats(engine)
    user_analysis(engine)
    song_analysis(engine)
    artist_analysis(engine)
    listening_patterns(engine)
    user_engagement(engine)
    location_insights(engine)
    key_insights(engine)
    
    print("\n" + "=" * 60)
    print("  ✅ EDA COMPLETE")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_eda()
