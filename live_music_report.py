import os
import sqlite3




def compile_live_music_report(db_path="live_music_catalog.db", output_filename="dashboard.html"):
    """Queries the live_music_catalog database and exports a clean HTML QA dashboard."""

    # 1. Connect to active database file
    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 2. Ensure the table exists and query rows ordered by newest first
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

        cursor.execute(
            "SELECT track_name, artist_name, collection_name, duration_ms, status FROM web_tracks ORDER BY id DESC"
        )
        db_rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        return
    finally:
        conn.close()

    # 3. Define dark, professional production styling
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

    # 4. Dynamically iterate through SQL rows and construct table elements
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

    # 5. Append closing structural tags
    html_layout += """        </tbody>
    </table>
</body>
</html>"""

    # 6. Safely output the compiled string to disk
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_layout)

    print(f"Dashboard compilation successful. Output saved to: {output_filename}")


if __name__ == "__main__":
    compile_live_music_report()
