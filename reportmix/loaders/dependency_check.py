"""
Dependency-Check report loader.
"""

import csv
import logging
from datetime import datetime
from os import path
from typing import List

from reportmix.config.property import ConfigProperty
from reportmix.loader import Loader
from reportmix.models import severity
from reportmix.models.issue import Issue
from reportmix.models.project import Project
from reportmix.models.subject import Subject
from reportmix.models.tool import Tool

# Configuration properties
PROPERTIES: List[ConfigProperty] = [
    ConfigProperty("report_file", "path to the report file", False, "dependency-check-report.csv")
]


class DependencyCheckLoader(Loader):
    """
    Dependency-Check report loader (CSV format only).
    """

    def load(self) -> List[Issue]:
        """
        Load the Dependency Check report file (CSV format only),
        parse it, map vulnerabilities to issues, and return the list.
        :return: List of vulnerabilities.
        """
        report_file_path = path.realpath(self.config["report_file"])
        if not (report_file_path.endswith(".csv") and path.exists(report_file_path)):
            logging.warning("Dependency check report ignored (file not found or not *.csv)")
            return []
        logging.debug("Loading report %s", report_file_path)
        try:
            with open(report_file_path, "r", newline='') as report_file:
                report = csv.DictReader(report_file, delimiter=',', quotechar='"')
                issues = []
                for row in report:
                    issues.append(Issue(
                        ref="",
                        identifier=row["CVE"],
                        name=row["CVE"],
                        type="VULNERABILITY",
                        category=row["CWE"],
                        description=row["Vulnerability"],
                        more="",
                        action="",
                        effort="",
                        # TODO Improve date parsing
                        analysis_date=datetime.strptime(row["ScanDate"][:24],
                                                        "%a, %d %b %Y %H:%M:%S"),
                        severity=severity.guess(row["CVSSv3_BaseSeverity"]),
                        score=row["CVSSv3"],
                        confidence=row["CPE Confidence"],
                        evidences=int(row["Evidence Count"]),
                        source=row["Source"],
                        source_date=None,
                        url="",
                        tool=Tool(
                            identifier="dependency_check",
                            name="Dependency-Check",
                            version=""
                        ),
                        subject=Subject(
                            identifier=row["Identifiers"],
                            name=row["Description"],
                            description=row["DependencyName"],
                            version="",
                            location=row["DependencyPath"],
                            license=row["License"]
                        ),
                        project=Project(
                            identifier=row["Project"],
                            name=row["Project"],
                            version=""
                        )
                    ))
                return issues
        except Exception as ex:
            logging.error("Failed to load, parse and map the report (%s)", ex)
            return []
