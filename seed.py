"this is a file to fill the database"

#imports
import json
import db
from pathlib import Path    # imports the path action

#paths
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DATA_PATH = Path(__file__).resolve().parent / "data" / "restaurants.json"

def main():
    #read JSON

    with open(DATA_PATH) as f:
        data = json.load(f)

    # Open database and build tables
    connection = db.get_connection()

    with open(SCHEMA_PATH) as f:
        connection.executescript(f.read())

    restaurant_count = 0
    item_count = 0

    for restaurant in data:
        cursor = connection.execute(
            "INSERT INTO restaurants (name, city) VALUES (?, ?)",
            (restaurant["name"], restaurant["city"]),
        )
        restaurant_id = cursor.lastrowid

        for item in restaurant["menu"]:
            # tags_str = ",".join(item["tags"])
            # item.get("description")
            
            cursor = connection.execute(
                "INSERT INTO menu_items (restaurant_id, name, description) VALUES (?, ?, ?)",
                (restaurant_id, item["name"], item["description"])
            )
            item_id = cursor.lastrowid

            for tag in item["tags"]:
                connection.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
                tag_id = connection.execute(
                    "SELECT id FROM tags WHERE name = ?", (tag,)
                ).fetchone()["id"]
                connection.execute(
                "INSERT INTO item_tags (item_id, tag_id) VALUES (?, ?)", (item_id, tag_id) 
                )
            
            

            item_count += 1

        restaurant_count += 1
    connection.commit()
    connection.close()
    print(f"Seeded {restaurant_count} restaurants, {item_count} menu items")

if __name__ == "__main__":
    main()


