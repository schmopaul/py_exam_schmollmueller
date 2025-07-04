import sqlite3
import os

# Ensure the folder exists
#os.makedirs('db', exist_ok=True)

# Path to the database inside the ex_03 folder
db_path = os.path.join('tasks.db')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create the 'tasks' table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done INTEGER DEFAULT 0 CHECK (done IN (0, 1))
)
''')

conn.commit()
conn.close()
print(f"Database created at {db_path}")
