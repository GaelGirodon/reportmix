"""
JSON report exporter.
"""

import json
from typing import List

from reportmix.exporter import Exporter
from reportmix.models.issue import Issue


class JsonExporter(Exporter):
    """
    Export a merged report to a JSON file.
    """

    def export(self, output_file: str, issues: List[Issue], fields: List[str]):
        with open(output_file, "w") as file:
            json.dump([i.to_dict() for i in issues], file, default=str)
