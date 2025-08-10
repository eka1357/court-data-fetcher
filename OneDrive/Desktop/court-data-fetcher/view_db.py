import sqlite3

conn = sqlite3.connect("cases.db")
cur = conn.cursor()
cur.execute("SELECT id, cnr_number, fetched_at FROM queries;")
rows = cur.fetchall()

if rows:
    for row in rows:
        print(row)
else:
    print("No records found.")

conn.close()
