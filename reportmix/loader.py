"""
Report loader parent class.
"""

from typing import List, Dict

from reportmix.models.issue import Issue


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

    def load(self) -> List[Issue]:
        """
        Load the report and return the list of items.
        :return: List of items loaded from the report.
        """
        return []
