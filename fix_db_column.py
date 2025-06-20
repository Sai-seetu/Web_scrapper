import sqlite3

db_path = "instance/scraper.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE api_link ADD COLUMN scraped_text TEXT;")
    print("✅ Column 'scraped_text' added successfully.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Skipping column addition: {e}")

conn.commit()
conn.close()
