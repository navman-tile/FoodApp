"""
test_matching.py

Tests for the pure functions in matching.py.

Run from the project folder with:
    pytest

pytest finds this file (name starts with "test_"), runs every function whose
name starts with "test_", and reports which assert statements failed.

No database here -- search() takes its rows as an argument, so we hand it the
small hand-made list below.
"""

from matching import parse_tags, item_matches, score_item, search


# A tiny fake result set, same shape search() gets from the DB:
# keys restaurant / city / name / description / tags, where "tags" is the raw
# comma-joined string exactly as it's stored.
SAMPLE_ROWS = [
    {"restaurant": "Green Fork", "city": "Austin", "name": "Lentil Bowl",
     "description": "lentils", "tags": "vegan,gluten-free,dairy-free"},
    {"restaurant": "Green Fork", "city": "Austin", "name": "Spicy Tacos",
     "description": "tacos", "tags": "vegan,gluten-free,dairy-free,spicy"},
    {"restaurant": "Smoke House", "city": "Austin", "name": "Brisket",
     "description": "beef", "tags": "gluten-free,dairy-free"},
    {"restaurant": "Harbour Grill", "city": "Sydney", "name": "Falafel Wrap",
     "description": "falafel", "tags": "vegan,dairy-free"},
]


# ---------------------------------------------------------------------------
# parse_tags
# ---------------------------------------------------------------------------

def test_parse_tags_splits_into_a_set():
    # Arrange + Act
    result = parse_tags("vegan,gluten-free,spicy")
    # Assert -- order doesn't matter, it's a set
    assert result == {"vegan", "gluten-free", "spicy"}


def test_parse_tags_single_tag():
    # TODO: parse_tags("vegan") should return {"vegan"}
    ...


# ---------------------------------------------------------------------------
# item_matches
# ---------------------------------------------------------------------------

def test_item_matches_when_all_restrictions_present():
    item = {"vegan", "gluten-free", "nut-free"}
    assert item_matches(item, {"vegan", "gluten-free"}) is True


def test_item_matches_false_when_one_restriction_missing():
    # TODO: item has {"vegan", "gluten-free"}, restrictions ask for
    # {"vegan", "halal"} -> should be False
    ...


def test_item_matches_true_when_no_restrictions():
    # TODO: any item, restrictions = set() -> should be True
    # (no restrictions means nothing to fail)
    ...


# ---------------------------------------------------------------------------
# score_item
# ---------------------------------------------------------------------------

def test_score_item_counts_overlap():
    # TODO: item {"vegan", "spicy"}, preferences {"spicy", "vegetarian"} -> 1
    ...


def test_score_item_zero_when_no_overlap():
    # TODO: item {"vegan"}, preferences {"spicy"} -> 0
    ...


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------

def test_search_filters_by_city():
    # No restrictions, no preferences, just the city filter.
    results = search([], [], "Sydney", SAMPLE_ROWS)
    names = [r["name"] for r in results]
    assert names == ["Falafel Wrap"]


def test_search_filters_by_restrictions():
    # TODO: search(["vegan"], [], "Austin", SAMPLE_ROWS)
    # Lentil Bowl and Spicy Tacos are vegan; Brisket is not.
    # Assert the result has 2 items, and "Brisket" is not among the names.
    ...


def test_search_ranks_preferred_items_first():
    # TODO: search(["vegan"], ["spicy"], "Austin", SAMPLE_ROWS)
    # Both results are vegan; Spicy Tacos has the "spicy" preference so it
    # should come first. Assert results[0]["name"] == "Spicy Tacos"
    # and results[0]["score"] == 1.
    ...


def test_search_empty_restrictions_returns_everything_in_city():
    # TODO: search([], [], "Austin", SAMPLE_ROWS) -> all 3 Austin rows
    ...


def test_search_unknown_city_returns_empty_list():
    # TODO: search([], [], "Paris", SAMPLE_ROWS) -> []
    ...
