# 🎵 Music Analytics Data Modeling

A complete ETL (Extract, Transform, Load) pipeline for a music streaming analytics platform. This project models user listening behavior data using a **star schema** optimized for analytical queries.

---

## 📋 Project Overview

This project simulates a music streaming service's data warehouse, processing JSON log files (user activity) and song metadata into a PostgreSQL database designed for analytics.

### Use Cases
- Track which songs and artists are most popular
- Analyze user listening patterns over time
- Understand user demographics and subscription levels
- Generate daily/weekly/monthly activity reports

---

## 🗂️ Data Model (Star Schema)

```
                    ┌─────────────┐
                    │    time     │
                    │─────────────│
                    │ start_time  │◄──┐
                    │ hour        │   │
                    │ day         │   │
                    │ week        │   │
                    │ month       │   │
                    │ year        │   │
                    │ weekday     │   │
                    └─────────────┘   │
                                      │
┌─────────────┐    ┌─────────────────┴────────────────┐    ┌─────────────┐
│   users     │    │           songplays              │    │   songs     │
│─────────────│    │──────────────────────────────────│    │─────────────│
│ user_id     │◄───│ songplay_id (PK)                 │───►│ song_id     │
│ first_name  │    │ start_time (FK)                  │    │ title       │
│ last_name   │    │ user_id (FK)                     │    │ artist_id   │
│ gender      │    │ level                            │    │ year        │
│ level       │    │ song_id (FK)                     │    │ duration    │
└─────────────┘    │ artist_id (FK)                   │    └─────────────┘
                   │ session_id                       │
                   │ location                         │    ┌─────────────┐
                   │ user_agent                       │    │   artists   │
                   └──────────────────────────────────┘    │─────────────│
                                      │                    │ artist_id   │
                                      └───────────────────►│ name        │
                                                           │ location    │
                                                           │ latitude    │
                                                           │ longitude   │
                                                           └─────────────┘
```

### Tables

| Table | Type | Description |
|-------|------|-------------|
| `songplays` | Fact | Records of song plays (user listening events) |
| `users` | Dimension | User information |
| `songs` | Dimension | Song metadata |
| `artists` | Dimension | Artist information |
| `time` | Dimension | Timestamps broken into time units |

---

## 🛠️ Tech Stack

- **Python 3.x** - ETL pipeline
- **PostgreSQL 15** - Data warehouse
- **SQLAlchemy** - Database ORM
- **Pandas** - Data transformation
- **Docker** - Database containerization
- **pytest** - Testing framework

---

## 📁 Project Structure

```
music-analytics-data-modeling/
├── data/
│   ├── song_data/          # JSON files with song metadata
│   ├── log_data/           # JSON files with user activity logs
│   └── generate_dummy_data.py
├── src/
│   ├── config.py           # Configuration and environment variables
│   ├── extract.py          # Data extraction from JSON files
│   ├── transform.py        # Data transformation logic
│   ├── load.py             # Load data to PostgreSQL
│   └── etl_pipeline.py     # Main ETL orchestration
├── sql/
│   ├── create_tables.sql   # Table creation DDL
│   ├── drop_tables.sql     # Table cleanup
│   └── analytical_queries.sql  # Sample analytics queries
├── tests/
│   └── test_quality_checks.py  # Data quality tests
├── .env                    # Environment variables (DATABASE_URL)
├── docker-compose.yml      # PostgreSQL container config
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker Desktop

### 1. Start the Database

```powershell
docker compose up -d
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Setup Database & Generate Sample Data

```powershell
python setup_database_and_data.py
```

This will:
- Drop and recreate all tables
- Generate sample song and log data

### 4. Run the ETL Pipeline

```powershell
$env:PYTHONPATH = "src"
python src/etl_pipeline.py
```

### 5. Run Tests

```powershell
pytest tests/test_quality_checks.py
```

---

## 📊 Sample Analytics Queries

### Top 10 Most Played Songs
```sql
SELECT s.title, COUNT(sp.songplay_id) AS play_count
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
GROUP BY s.title
ORDER BY play_count DESC
LIMIT 10;
```

### Daily Active Users
```sql
SELECT t.day, COUNT(DISTINCT sp.user_id) AS active_users
FROM songplays sp
JOIN time t ON sp.start_time = t.start_time
GROUP BY t.day
ORDER BY t.day;
```

---

## ⚙️ Configuration

Environment variables are stored in `.env`:

```env
DATABASE_URL=postgresql://music:music@localhost:5432/musicdb
```

---

## 📝 Troubleshooting

See [TROUBLESHOOTING_LOG.md](./TROUBLESHOOTING_LOG.md) for common issues and solutions.

---

## 📄 License

This project is for educational purposes.