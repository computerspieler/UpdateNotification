import sqlite3
from common import get_db_path

with open("setup.sql", "r") as f:
	with sqlite3.connect(get_db_path()) as conn:
		cur = conn.cursor()
		cur.execute(f.read())

