from __future__ import annotations

import ckan.plugins.toolkit as tk

CONFIG_MAX_RATING = "ckanext.flakes_rating.max_rating"
DEFAULT_MAX_RATING = 5

CONFIG_MIN_RATING = "ckanext.flakes_rating.min_rating"
DEFAULT_MIN_RATING = 1


def max_rating() -> int:
    return tk.asint(tk.config.get(CONFIG_MAX_RATING, DEFAULT_MAX_RATING))


def min_rating() -> int:
    return tk.asint(tk.config.get(CONFIG_MIN_RATING, DEFAULT_MIN_RATING))
