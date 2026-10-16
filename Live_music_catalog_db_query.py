import sqlite3

def query_music_database(db_path="live_music_catalog.db"):
    """Connects to the SQLite database and prints all stored tracks."""
    
    # 1. Connect to the existing database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 2. Execute a SELECT query to retrieve the tracks
        cursor.execute(
            """
            SELECT id, track_name, artist_name, collection_name, duration_ms, status 
            FROM web_tracks 
            ORDER BY id DESC
            """
        )
        
        # 3. Fetch all matching rows from the query
        rows = cursor.fetchall()
        
        if not rows:
            print("No tracks found in the database.")
            return

        print(f"Successfully retrieved {len(rows)} track(s) from the database:\n" + "-" * 50)
        
        # 4. Loop through and display the rows
        for row in rows:
            track_id, title, artist, album, duration_ms, status = row
            
            # Convert milliseconds to minutes safely
            minutes = (duration_ms / 1000) / 60 if duration_ms else 0.0
            
            print(f"Record ID : {track_id}")
            print(f"Track     : {title}")
            print(f"Artist    : {artist}")
            print(f"Album     : {album}")
            print(f"Duration  : {minutes:.2f} mins")
            print(f"Status    : {status}")
            print("-" * 50)
            
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
    finally:
        # 5. Always close the connection when finished
        conn.close()

if __name__ == "__main__":
    query_music_database()