"""
Report exporter parent class.
"""

from typing import List, Dict

from reportmix.models.report import Report


class Exporter:
    """
    A merged report exporter.
    Export a list of issues to a file.
    """

    def __init__(self, config: Dict[str, str]):
        """
        Initialize the report exporter with the given configuration.
        :param config: Report exporter configuration.
        """
        self.config = config

    def export(self, report: Report, output_file: str, fields: List[str]):
        """
        Export a list of issues to a file.
        :param report: Report with the list of issues to export.
        :param output_file: Path to the output file.
        :param fields: List of fields to include in the output report.
        """
