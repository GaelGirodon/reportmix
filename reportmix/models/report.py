"""
Report model.
"""
from typing import List

from reportmix.models.issue import Issue
from reportmix.models.tool import Tool


class Report:
    """
    A mixed report of issues found by tools.
    """

    def __init__(self, issues: List[Issue], tools: List[Tool]):
        """
        Initialize a report of issues found by tools.
        :param issues: List of issues (may be empty)
        :param tools: Tools involved in identifying issues
        """
        self.issues = issues
        self.tools = tools

    def extend(self, report: "Report"):
        """
        Extend report by appending issues and tools from another report.
        :param report: Report to append.
        """
        self.issues.extend(report.issues)
        self.tools.extend(report.tools)
