import argparse
import sys

import sqlite3
from common import get_db_path
from sources import (
    URL_VALIDATOR,
    URL_NAME_EXTRACTOR
)

argparser = argparse.ArgumentParser()
argparser.add_argument("-t", "--type", type=str, choices=URL_NAME_EXTRACTOR.keys(), required=True,
    help="Defines the type of the source")
argparser.add_argument("url", type=str,
    help="Defines the source")

args = argparser.parse_args()
if not URL_VALIDATOR[args.type](args.url):
    print(f"This is an invalid URL for the type <{args.type}>: '{args.url}'")
    sys.exit(1)

with sqlite3.connect(get_db_path()) as conn:
    name = URL_NAME_EXTRACTOR[args.type](args.url)
    conn.execute(f"""
        INSERT INTO sources (tPath, tName, tType)
        VALUES ('{args.url}', '{name}', '{args.type}')
    """)

print("Done !")