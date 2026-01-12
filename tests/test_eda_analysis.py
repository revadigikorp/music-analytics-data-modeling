"""
Tests for EDA Analysis Module
"""
import pytest
import pandas as pd
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL
from src.eda_analysis import (
    connect_to_db,
    load_table,
    basic_stats,
    user_analysis,
    song_analysis,
    artist_analysis,
    listening_patterns,
    user_engagement,
    location_insights,
    run_eda
)


@pytest.fixture
def engine():
    """Create database engine for tests."""
    return create_engine(DATABASE_URL)


class TestDatabaseConnection:
    """Tests for database connectivity."""
    
    def test_connect_to_db_returns_engine(self):
        """Test that connect_to_db returns a valid engine."""
        engine = connect_to_db()
        assert engine is not None
    
    def test_database_is_accessible(self, engine):
        """Test that database can be queried."""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            assert result == 1


class TestLoadTable:
    """Tests for table loading functionality."""
    
    def test_load_users_table(self, engine):
        """Test loading users table returns DataFrame."""
        df = load_table(engine, 'users')
        assert isinstance(df, pd.DataFrame)
        assert 'user_id' in df.columns
        assert 'first_name' in df.columns
    
    def test_load_songs_table(self, engine):
        """Test loading songs table returns DataFrame."""
        df = load_table(engine, 'songs')
        assert isinstance(df, pd.DataFrame)
        assert 'song_id' in df.columns
        assert 'title' in df.columns
    
    def test_load_artists_table(self, engine):
        """Test loading artists table returns DataFrame."""
        df = load_table(engine, 'artists')
        assert isinstance(df, pd.DataFrame)
        assert 'artist_id' in df.columns
        assert 'name' in df.columns
    
    def test_load_songplays_table(self, engine):
        """Test loading songplays table returns DataFrame."""
        df = load_table(engine, 'songplays')
        assert isinstance(df, pd.DataFrame)
        assert 'songplay_id' in df.columns


class TestDataQuality:
    """Tests for data quality checks."""
    
    def test_users_have_required_fields(self, engine):
        """Test that users have all required fields populated."""
        df = load_table(engine, 'users')
        if len(df) > 0:
            assert df['user_id'].notna().all()
            assert df['first_name'].notna().all()
    
    def test_songs_have_required_fields(self, engine):
        """Test that songs have all required fields populated."""
        df = load_table(engine, 'songs')
        if len(df) > 0:
            assert df['song_id'].notna().all()
            assert df['title'].notna().all()
    
    def test_artists_have_required_fields(self, engine):
        """Test that artists have all required fields populated."""
        df = load_table(engine, 'artists')
        if len(df) > 0:
            assert df['artist_id'].notna().all()
            assert df['name'].notna().all()
    
    def test_songplays_foreign_keys_valid(self, engine):
        """Test that songplays have valid foreign key references."""
        songplays = load_table(engine, 'songplays')
        users = load_table(engine, 'users')
        
        if len(songplays) > 0:
            # All user_ids in songplays should exist in users table
            valid_user_ids = set(users['user_id'].tolist())
            songplay_user_ids = set(songplays['user_id'].tolist())
            assert songplay_user_ids.issubset(valid_user_ids)


class TestEDAFunctions:
    """Tests for EDA analysis functions."""
    
    def test_basic_stats_runs_without_error(self, engine, capsys):
        """Test that basic_stats executes successfully."""
        basic_stats(engine)
        captured = capsys.readouterr()
        assert "DATABASE OVERVIEW" in captured.out
    
    def test_user_analysis_runs_without_error(self, engine, capsys):
        """Test that user_analysis executes successfully."""
        user_analysis(engine)
        captured = capsys.readouterr()
        assert "USER ANALYSIS" in captured.out
    
    def test_song_analysis_runs_without_error(self, engine, capsys):
        """Test that song_analysis executes successfully."""
        song_analysis(engine)
        captured = capsys.readouterr()
        assert "SONG CATALOG ANALYSIS" in captured.out
    
    def test_artist_analysis_runs_without_error(self, engine, capsys):
        """Test that artist_analysis executes successfully."""
        artist_analysis(engine)
        captured = capsys.readouterr()
        assert "ARTIST ANALYSIS" in captured.out
    
    def test_listening_patterns_runs_without_error(self, engine, capsys):
        """Test that listening_patterns executes successfully."""
        listening_patterns(engine)
        captured = capsys.readouterr()
        assert "LISTENING PATTERNS" in captured.out
    
    def test_user_engagement_runs_without_error(self, engine, capsys):
        """Test that user_engagement executes successfully."""
        user_engagement(engine)
        captured = capsys.readouterr()
        assert "USER ENGAGEMENT" in captured.out
    
    def test_location_insights_runs_without_error(self, engine, capsys):
        """Test that location_insights executes successfully."""
        location_insights(engine)
        captured = capsys.readouterr()
        assert "GEOGRAPHIC INSIGHTS" in captured.out


class TestFullEDA:
    """Integration test for full EDA run."""
    
    def test_run_eda_completes_successfully(self, capsys):
        """Test that full EDA run completes without errors."""
        run_eda()
        captured = capsys.readouterr()
        assert "EDA COMPLETE" in captured.out
        assert "DATABASE OVERVIEW" in captured.out
        assert "KEY INSIGHTS" in captured.out
