"""
app.py

The Flask web layer. Two routes:
  GET /            -> the HTML page
  GET /api/search  -> JSON results, powered by matching.search()

Routes here stay thin: read the request, call into matching.py, return a
response. No matching logic lives in this file.

Run the dev server with:
    flask run
(or `python app.py`, which uses the __main__ block at the bottom)
"""

from flask import Flask, render_template, request, jsonify

import db
import matching

# __name__ tells Flask where this app lives, so it can find the templates/
# and static/ folders next to this file.
app = Flask(__name__)


# The SQL that loads every menu item joined to its restaurant. Same query the
# matching.py __main__ block uses. (Duplicated in two places for now -- if it
# shows up a third time, move it into its own function.)
MENU_QUERY = """
    SELECT r.name        AS restaurant,
           r.city        AS city,
           m.name        AS name,
           m.description AS description,
           m.tags        AS tags
    FROM menu_items m
    JOIN restaurants r ON r.id = m.restaurant_id
"""


def load_rows():
    """Open the DB, run MENU_QUERY, return the rows, close the connection."""
    connection = db.get_connection()
    rows = connection.execute(MENU_QUERY).fetchall()
    connection.close()
    return rows


@app.route("/")
def index():
    # render_template looks in templates/ for this file, fills in any
    # placeholders (none yet), and returns the finished HTML.
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    """Read the query string, run the search, return JSON.

    A request looks like:
        /api/search?restrictions=vegan,gluten-free&preferences=spicy&location=Sydney

    Steps:
      1. Read three values from request.args, each defaulting to "" if missing:
           restrictions_raw, preferences_raw, location
         (request.args.get("name", "") -- the "" is the default)

      2. Turn the two comma-joined strings into lists of tags. Watch the edge
         case: "".split(",") returns [""], NOT []. So filter out empty strings.
         A list comprehension does both jobs at once:
             [t for t in raw.split(",") if t]

      3. rows = load_rows()

      4. results = matching.search(restrictions, preferences, location, rows)

      5. return jsonify(results)
    """
    # TODO: your code here
    restrictions_raw = request.args.get("restrictions", "")
    preferences_raw = request.args.get("preferences", "")
    location = request.args.get("location", "")

    # restrictions = restrictions_raw.split(",")
    # preferences = preferences_raw.split(",")
    # explain the line below
    restrictions = [t for t in restrictions_raw.split(",") if t]
    preferences = [t for t in preferences_raw.split(",") if t]

    rows = load_rows()
    results = matching.search(restrictions, preferences, location, rows)
    return jsonify(results)


if __name__ == "__main__":
    # debug=True gives auto-reload on save and a helpful error page in the
    # browser. Fine for local development, never for a real deployment.
    app.run(debug=True)
