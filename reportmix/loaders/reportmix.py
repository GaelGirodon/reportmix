"""
ReportMix report loader.
"""

import csv
import logging
from datetime import datetime
from os import path
from typing import List

from reportmix.config.property import ConfigProperty
from reportmix.errors import LoadingError
from reportmix.loader import Loader
from reportmix.models import severity
from reportmix.models.issue import Issue
from reportmix.models.project import Project
from reportmix.models.report import Report
from reportmix.models.subject import Subject
from reportmix.models.tool import Tool

# Configuration properties
PROPERTIES: List[ConfigProperty] = [
    ConfigProperty("report_file", "path to the report file", False)
]


class ReportMixLoader(Loader):
    """
    ReportMix report loader (CSV required).
    """

    def load(self) -> Report:
        """
        Load the ReportMix report file (CSV required), parse it, and return the
        list of issues.
        :return: Loaded issues.
        """
        if "report_file" not in self.config or self.config["report_file"] is None:
            raise LoadingError("ReportMix report ignored (report file path required)")

        report_file_path = path.realpath(self.config["report_file"])
        if not (report_file_path.endswith(".csv") and path.exists(report_file_path)):
            raise LoadingError("ReportMix report ignored (file not found or not *.csv)")

        logging.debug("Loading report %s", report_file_path)

        try:
            # Load issues from the CSV report
            with open(report_file_path, "r", newline='') as report_file:
                report = csv.DictReader(report_file, delimiter=',', quotechar='"')
                issues = []
                for row in report:
                    analysis_date = None
                    if row.get("analysis_date"):
                        analysis_date = datetime.fromisoformat(row["analysis_date"])
                    source_date = None
                    if row.get("source_date"):
                        source_date = datetime.fromisoformat(row["source_date"])
                    evidences = 1
                    if row.get("evidences", "1").isdecimal():
                        evidences = int(row.get("evidences", "1"))
                    issues.append(Issue(
                        ref=row.get("ref"),
                        identifier=row["identifier"],  # Required
                        name=row.get("name"),
                        type=row.get("type"),
                        category=row.get("category"),
                        description=row.get("description"),
                        more=row.get("more"),
                        action=row.get("action"),
                        effort=row.get("effort"),
                        analysis_date=analysis_date,
                        severity=severity.from_identifier(row.get("severity")),
                        score=row.get("score"),
                        confidence=row.get("confidence"),
                        evidences=evidences,
                        source=row.get("source"),
                        source_date=source_date,
                        url=row.get("url"),
                        tool=Tool(
                            identifier=row["tool_identifier"],  # Required
                            name=row.get("tool_name"),
                            version=row.get("tool_version"),
                        ),
                        subject=Subject(
                            identifier=row["subject_identifier"],  # Required
                            name=row.get("subject_name"),
                            description=row.get("subject_description"),
                            version=row.get("subject_version"),
                            location=row.get("subject_location"),
                            license=row.get("subject_license"),
                        ),
                        project=Project(
                            identifier=row.get("project_identifier"),
                            name=row.get("project_name"),
                            version=row.get("project_version"),
                        ),
                        # meta ignored
                        # hash ignored
                    ))
                tools = list({i.tool.identifier: i.tool for i in issues}.values())
                return Report(issues, tools)
        except Exception as ex:
            raise LoadingError("Failed to load and parse the report: {}".format(ex))
