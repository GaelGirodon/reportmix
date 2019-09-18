"""
Tool model.
"""


class Tool:
    """
    A tool that scanned a project and found issues.
    """

    def __init__(self, identifier: str, name: str, version: str):
        """
        Initialize a tool that scanned a project and found issues.
        :param identifier: Scan tool id
        :param name: Scan tool display name
        :param version: Scan tool version
        """
        self.identifier = identifier
        self.name = name
        self.version = version
