import sqlite3
import uuid

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE,
        username TEXT UNIQUE,
        password TEXT
    )
''')
conn.commit()

admin_uuid = str(uuid.uuid4())
cursor.execute(
    "INSERT OR IGNORE INTO users (uuid, username, password) VALUES (?, ?, ?)",
    (admin_uuid, 'administrator', '8Xu0c:2z&-u>Z:>?2$`4|Z`lmTa7H+')
)

charlie_uuid = str(uuid.uuid4())
cursor.execute(
    "INSERT OR IGNORE INTO users (uuid, username, password) VALUES (?, ?, ?)",
    (charlie_uuid, 'Charlie', 'T-n*08XF&0/;gp8b!yk|')
)

conn.commit()
conn.close()
