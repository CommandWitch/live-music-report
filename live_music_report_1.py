import os
import sqlite3
import json
from urllib.request import urlopen


def compile_live_music_report(db_path="live_music_catalog.db", output_filename="dashboard.html"):
    """Queries the live_music_catalog database and exports a clean HTML QA dashboard."""

    # 1. Connect to active database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure the table exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS web_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_name TEXT NOT NULL,
            artist_name TEXT NOT NULL,
            collection_name TEXT NOT NULL,
            duration_ms INTEGER,
            status TEXT NOT NULL
        );
        """
    )
    conn.commit()

    # 2. Fetch live data from the iTunes Search API
    tunes_url = "https://itunes.apple.com/search?term=rock&entity=song&limit=3"
    
    try:
        with urlopen(tunes_url) as response:
            tunes_data = json.loads(response.read().decode("utf-8"))
        
        # iTunes API returns items under the 'results' key
        top_tunes = tunes_data.get('results', []) 

        # Insert the fetched API data into our SQLite database
        for track in top_tunes:
            track_name = track.get('trackName', 'Unknown Track')
            artist_name = track.get('artistName', 'Unknown Artist')
            collection_name = track.get('collectionName', 'Unknown Album')
            duration_ms = track.get('trackTimeMillis', 0)
            status = "PASS"  # Default QA status

            cursor.execute(
                """
                INSERT INTO web_tracks (track_name, artist_name, collection_name, duration_ms, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (track_name, artist_name, collection_name, duration_ms, status)
            )
        conn.commit()

    except Exception as e:
        print(f"API or Database error: {e}")

    try:
        # 3. Query rows ordered by newest first
        cursor.execute(
            "SELECT track_name, artist_name, collection_name, duration_ms, status FROM web_tracks ORDER BY id DESC"
        )
        db_rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return
    finally:
        conn.close()

    # 4. Define dark, professional production styling
    html_layout = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Content Ingestion Support Dashboard</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 40px; background-color: #0f172a; color: #f8fafc; }
        h2 { color: #38bdf8; font-weight: 600; border-bottom: 2px solid #334155; padding-bottom: 10px; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }
        th, td { padding: 14px; text-align: left; }
        th { background-color: #1e293b; color: #38bdf8; font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em; }
        tr { background-color: #1e293b; border-bottom: 1px solid #334155; }
        tr:hover { background-color: #24334c; }
        .badge-pass { background-color: #065f46; color: #34d399; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 12px; display: inline-block; }
        .badge-fail { background-color: #7f1d1d; color: #f87171; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 12px; display: inline-block; }
    </style>
</head>
<body>
    <h2>iTunes Ingestion Engine - Live Metadata QA Dashboard</h2>
    <table>
        <thead>
            <tr>
                <th>Track Title</th>
                <th>Artist Identity</th>
                <th>Album Context</th>
                <th>Duration (Mins)</th>
                <th>Validation Review</th>
            </tr>
        </thead>
        <tbody>
"""

    # 5. Dynamically iterate through SQL rows and construct table elements
    for row in db_rows:
        title, artist, album, duration_ms, status = row

        # Convert milliseconds to decimal minutes safely
        minutes = (duration_ms / 1000) / 60 if duration_ms else 0.0

        # Enforce robust conditional styling based on pipeline status flags
        badge_style = "badge-pass" if "PASS" in str(status).upper() else "badge-fail"

        html_layout += f"""            <tr>
                <td><strong>{title}</strong></td>
                <td>{artist}</td>
                <td>{album}</td>
                <td>{minutes:.2f}</td>
                <td><span class="{badge_style}">{status}</span></td>
            </tr>\n"""

    # 6. Append closing structural tags
    html_layout += """        </tbody>
    </table>
</body>
</html>"""

    # 7. Safely output the compiled string to disk
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_layout)

    print(f"Dashboard compilation successful. Output saved to: {output_filename}")


if __name__ == "__main__":
    compile_live_music_report()