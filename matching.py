"""
matching.py

The core logic of the app: given a user's dietary restrictions, preferences,
and location, decide which menu items match and in what order.

These four functions are PURE -- they take data in and return data out, with no
database and no Flask. That means you can test them from a Python shell with
data you type by hand. The __main__ block at the bottom wires them to the real
database for a quick end-to-end check.

Key idea used throughout:
  - restrictions  -> a HARD filter. An item must have every restriction tag or
                     it's dropped.
  - preferences   -> a SOFT rank. Items are kept regardless, but ones with more
                     matching preference tags sort higher.
"""


def parse_tags(tags_str):
    """Turn the stored tag string into a set.

    Input:  "vegan,gluten-free"      (how tags are stored in the DB)
    Output: {"vegan", "gluten-free"}  (a set, easy to compare)

    Steps:
      1. split the string on "," to get a list
      2. hand that list to set() and return it

    (Our data always has at least one tag, so don't worry about the empty
    string case for now.)
    """
    # TODO: your code here
    tags_list = tags_str.split(",")
    return set(tags_list)
    
    


def item_matches(item_tags, restrictions):
    """Return True only if the item satisfies EVERY restriction.

    Inputs are both sets, e.g.
        item_tags    = {"vegan", "gluten-free", "nut-free"}
        restrictions = {"vegan", "gluten-free"}
    -> True  (every restriction is present on the item)

        restrictions = {"vegan", "halal"}
    -> False ("halal" is not on the item)

    Hint: this is a one-line subset check. Which set must be a subset of which?
    If restrictions is empty, every item should pass -- check that the operator
    you pick gives that for free.
    """
    # TODO: your code here - believe this works - but is there a more effificen solution?
    match = restrictions.issubset(item_tags)
    # for restriction in restrictions:
    #     for tag in item_tags:
    #         if restriction == tag:
    #             match = True
    #             continue
    #         else:
    #             match = False
    return match


def score_item(item_tags, preferences):
    """Return how many preference tags the item has (an int, 0 or more).

    Used only for ranking -- never to filter anything out.

        item_tags   = {"vegan", "spicy"}
        preferences = {"spicy", "vegetarian"}
    -> 1  (only "spicy" is in both)

    Hint: intersection, then len().
    """
    # TODO: your code here - is there a more efficient solution
    score = 0
    for prefence in preferences:
        for tag in item_tags:
            if prefence == tag:
                score += 1
    return score


def search(restrictions, preferences, location, rows):
    """Filter and rank menu items.

    Inputs:
      restrictions, preferences -- lists of tag strings from the caller,
                                   e.g. ["vegan", "gluten-free"]. May be empty.
      location                  -- a city string, matched exactly.
      rows                      -- a list of dict-like records, each with keys:
                                     "restaurant", "city", "name",
                                     "description", "tags"
                                   ("tags" is the raw "a,b,c" string)

    Returns:
      a list of dicts, each:
        {"restaurant": ..., "name": ..., "description": ...,
         "tags": [... list ...], "score": <int>}
      sorted by score, highest first.

    Steps:
      1. convert restrictions and preferences from lists to sets (once, up here
         -- not inside the loop)
      2. make an empty list for results
      3. for each row in rows:
           a. skip it if row["city"] does not equal location
           b. item_tags = parse_tags(row["tags"])
           c. skip it if not item_tags = parse_tags(row["tags"])
           d. score = score_item(item_tags, preference_set)
           e. append a result dict (see shape above) to results
      4. sort results by "score", highest first, and return it
         (sorted(results, key=..., reverse=True) -- key is a function that
          takes one result dict and returns its score)
    """
    # TODO: your code here
    set_restrictions = set(restrictions)
    set_preferences = set(preferences)
    results = []
    for row in rows:
        if row["city"] != location: continue   
        else:
            item_tags = parse_tags(row["tags"])
            # print(row["name"], "->", repr(item_tags), type(item_tags),
            #   "| matches:", item_matches(item_tags, set_restrictions))
            if not item_matches(item_tags, set_restrictions):
                continue
            else:
                score = score_item(item_tags, set_preferences)
                results.append({
                    "restaurant": row["restaurant"],
                    "name": row["name"],
                    "description": row["description"],
                    "tags": sorted(item_tags),
                    "score": score,
                })
    return sorted(results, key=lambda r: r["score"], reverse=True)
            



# ---------------------------------------------------------------------------
# Checkpoint runner (written for you). Run:  python matching.py
# Loads the real database and prints a sample search so you can see the
# functions working end to end.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import db  # imported here, not at the top, so the functions above stay pure

    connection = db.get_connection()
    # One JOIN pulls each menu item together with its restaurant. The "AS"
    # names line up with the keys search() expects in each row.
    rows = connection.execute(
        """
        SELECT r.name        AS restaurant,
               r.city        AS city,
               m.name        AS name,
               m.description AS description,
               m.tags        AS tags
        FROM menu_items m
        JOIN restaurants r ON r.id = m.restaurant_id
        """
    ).fetchall()
    connection.close()

    # Same query you checked by hand earlier: gluten-free + dairy-free in
    # Sydney, preferring spicy. Expect Duck Soup first, then Lentil Power Bowl.
    results = search(
        restrictions=["gluten-free", "dairy-free"],
        preferences=["spicy"],
        location="Sydney",
        rows=rows,
    )
    for r in results:
        print(f'{r["score"]}  {r["restaurant"]:<16}  {r["name"]}')