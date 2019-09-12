import json
from typing import List

from reportmix.exporter import Exporter
from reportmix.report.issue import Issue


class JsonExporter(Exporter):
    """
    Export a merged report to a JSON file.
    """

    def export(self, dest: str, issues: List[Issue]):
        with open(dest, "w") as output_file:
            json.dump([vars(issue) for issue in issues], output_file, default=str)
