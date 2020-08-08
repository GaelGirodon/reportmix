"""
JSON report exporter.
"""

import json
from typing import List

from reportmix.exporter import Exporter
from reportmix.models.report import Report


class JsonExporter(Exporter):
    """
    Export a merged report to a JSON file.
    """

    def export(self, report: Report, output_file: str, fields: List[str]):
        with open(output_file, "w") as file:
            json.dump([i.to_dict() for i in report.issues], file, default=str)
