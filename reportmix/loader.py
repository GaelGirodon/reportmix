"""
Report loader parent class.
"""

from typing import Dict

from reportmix.models.report import Report


class Loader:
    """
    A report loader.
    Load and parse a specific type of report associated to a tool.
    """

    def __init__(self, config: Dict[str, str]):
        """
        Initialize the report loader with the given configuration.
        :param config: Report loader configuration.
        """
        self.config = config

    def load(self) -> Report:
        """
        Load the report and return the list of issues.
        :return: The loaded report.
        """
        return Report([], [])
