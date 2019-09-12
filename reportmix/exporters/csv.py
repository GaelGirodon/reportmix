import csv
from typing import List

from reportmix.exporter import Exporter
from reportmix.report.issue import Issue


class CsvExporter(Exporter):
    """
    Export a merged report to a CSV file.
    """

    def export(self, dest: str, issues: List[Issue]):
        with open(dest, "w", newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=vars(issues[0]).keys(),
                                    delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for issue in issues:
                writer.writerow(vars(issue))
