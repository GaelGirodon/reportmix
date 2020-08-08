"""
CSV report exporter.
"""

import csv
from typing import List

from reportmix.exporter import Exporter
from reportmix.models.report import Report


class CsvExporter(Exporter):
    """
    Export a merged report to a CSV file.
    """

    def export(self, report: Report, output_file: str, fields: List[str]):
        with open(output_file, "w", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields, extrasaction='ignore',
                                    delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for issue in report.issues:
                writer.writerow(issue.flatten())
