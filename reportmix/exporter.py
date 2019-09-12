from typing import List

from reportmix.report.issue import Issue


class Exporter:
    """
    A merged report exporter.
    Export a list of issues to a file.
    """

    def export(self, dest: str, issues: List[Issue]):
        """
        Export a list of issues to a file.
        :param dest: Path to the output file.
        :param issues: List of issues to write.
        """
        pass
