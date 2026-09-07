"this is a file to fill the database"

#imports
import json
import db
from pathlib import Path    # imports the path action

#paths
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DATA_PATH = Path(__file__).resolve().parent / "data" / "restaurants.json"

#read JSON

with open(DATA_PATH) as f:
    data = json.load(f)

# Open database and build tables
connection = db.get_connection()

with open(SCHEMA_PATH) as f:
    connection.executescript(f.read())
