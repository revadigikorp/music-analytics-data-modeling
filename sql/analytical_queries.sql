-- Top 10 most played songs
SELECT s.title, COUNT(sp.songplay_id) AS play_count
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
GROUP BY s.title
ORDER BY play_count DESC
LIMIT 10;

-- Daily active users over the last 30 days
SELECT t.day, COUNT(DISTINCT sp.user_id) AS active_users
FROM songplays sp
JOIN time t ON sp.start_time = t.start_time
GROUP BY t.day
ORDER BY t.day;