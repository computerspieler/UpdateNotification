import logging
from datetime import datetime, timezone

import sqlite3
from common import get_db_path
from sources import RELEASE_RETRIEVER

QUERY = """
SELECT
	id, tName, tPath, tType, tDate
FROM
	sources
"""

logging.getLogger().setLevel(logging.DEBUG)

path = get_db_path()
now = datetime.now()
with sqlite3.connect(get_db_path()) as conn:
	for row in conn.execute(QUERY).fetchall():
		id, name, path, tType, date = row
		logging.info(f"Updating {name}")
		try:
			last_date = datetime.fromisoformat(date)
			if last_date.tzinfo is None:
				last_date = last_date.replace(tzinfo=timezone.utc)
			out = RELEASE_RETRIEVER[tType](path, last_date)
			if out != None:
				out.title = name
				out()
			conn.execute(f"UPDATE sources SET tDate='{str(now)}' WHERE id={id}")
		except Exception as e:
			logging.error(f"An error occured while reading {name}: {e}")