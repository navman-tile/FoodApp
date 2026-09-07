-- schema.sql
-- Defines the shape of the database. seed.py runs this file to build empty
-- tables, then fills them from data/restaurants.json.
--
-- Re-running is always safe: we DROP each table before recreating it, so the
-- database is rebuilt from scratch every time seed.py runs. This is the
-- project's "reset button".

-- Drop the CHILD table first. menu_items points at restaurants via a foreign
-- key, so restaurants can't be dropped while menu_items still references it.
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS restaurants;


-- -----------------------------------------------------------------------------
-- restaurants  (worked example — study this, then write menu_items below)
-- -----------------------------------------------------------------------------
CREATE TABLE restaurants (
    -- Unique id for each restaurant. Declared exactly like this, SQLite fills
    -- it in automatically (1, 2, 3, ...). We never set it by hand.
    id   INTEGER PRIMARY KEY,

    -- The restaurant's name. NOT NULL = the database refuses a row without one.
    name TEXT NOT NULL,

    -- The city, matched exactly against the user's typed location.
    city TEXT NOT NULL
);


-- -----------------------------------------------------------------------------
-- menu_items  (YOUR TURN)
--
-- Columns it needs, and the type/constraints to give each one:
--   id            -- same idea as restaurants.id (auto-assigned unique id)
--   restaurant_id -- INTEGER. Which restaurant this item belongs to. It holds
--                    a value from restaurants.id, so add:
--                        REFERENCES restaurants(id)
--                    Should an item ever have no restaurant? (-> NOT NULL?)
--   name          -- the dish name. Required?
--   description   -- the short blurb shown in results. Is it required for the
--                    app to work, or is it display-only? (that answers NOT NULL)
--   tags          -- the comma-separated string, e.g. "vegan,gluten-free".
--                    Every item in our data has at least one tag. Required?
--
-- Write the CREATE TABLE statement below. Keep a comment on each column
-- saying what it's for.
-- -----------------------------------------------------------------------------

CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY,
    restaurant_id INTEGER NOT NULL REFERENCES restaurants(id),
    name TEXT NOT NULL,
    description TEXT,
    tags TEXT NOT NULL
);