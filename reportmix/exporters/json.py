import json
from typing import List

from reportmix.exporter import Exporter
from reportmix.report.issue import Issue, issues_to_dicts


class JsonExporter(Exporter):
    """
    Export a merged report to a JSON file.
    """

    def export(self, output_file: str, issues: List[Issue], fields: List[str]):
        # Keep only required fields
        raw_items = issues_to_dicts(issues)
        items = []
        for raw_item in raw_items:
            item = {}
            for f in fields:
                item[f] = raw_item[f]
            items.append(item)
        # Export
        with open(output_file, "w") as output_file:
            json.dump(items, output_file, default=str)
