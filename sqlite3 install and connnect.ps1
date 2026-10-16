N.B. This is the Python version of slite3 (REL)

python
>>> import sqlite3
>>> c = sqlite3.connect("live_music_catalog.db")
>>> c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

<# To Exit the Python interpreter, type exit() and press Enter.
-- Connect:        sqlite3 ./my_database.db
-- List tables:    .tables
-- Describe table: .schema table_name
-- Disconnect:     .quit
#>



