from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector

helper, get_helpers = Collector("flakes_rating").split()


@helper
def get_rating(type_: str, id_: str) -> dict[str, int]:
    return tk.get_action("flakes_rating_average")(
        {}, {"target_id": id_, "target_type": type_}
    )
