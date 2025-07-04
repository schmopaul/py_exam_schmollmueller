import sqlite3
import csv
import os

db_path = os.path.join('tasks.db')
csv_path = 'tasks.csv'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:  # <- utf-8-sig gegen BOM
    reader = csv.DictReader(csvfile, delimiter=';')
    print("Detected columns:", reader.fieldnames)  # <-- Zeigt echte Spaltennamen

    for row in reader:
        try:
            title = row['title']
            done = int(row['done'])
            cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', (title, done))
        except KeyError as e:
            print(f"Column not found: {e} – available: {row.keys()}")
        except Exception as e:
            print(f"Unexpected error: {e}")

conn.commit()
conn.close()
print("CSV import finished.")
