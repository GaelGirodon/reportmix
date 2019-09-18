"""
Report exporter parent class.
"""

from typing import List, Dict

from reportmix.models.issue import Issue


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

    def export(self, output_file: str, issues: List[Issue], fields: List[str]):
        """
        Export a list of issues to a file.
        :param output_file: Path to the output file.
        :param issues: List of issues to write.
        :param fields: List of fields to include in the output report.
        """
