import csv
import logging
from datetime import datetime
from os import path
from typing import List

from reportmix.config.property import ConfigProperty
from reportmix.loader import Loader
from reportmix.report import severity
from reportmix.report.issue import Issue

# Configuration properties
properties: List[ConfigProperty] = [
    ConfigProperty("report_file", "path to the report file", True, "dependency-check-report.csv")
]


class DependencyCheckLoader(Loader):
    """
    Dependency Check report loader (CSV format only).
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
                        name=row["CWE"],
                        type="VULNERABILITY",
                        description=row["Vulnerability"],
                        identifier=row["CVE"],
                        severity=severity.guess(row["CVSSv3_BaseSeverity"]),
                        score=row["CVSSv3"],
                        confidence=row["CPE Confidence"],
                        count=int(row["Evidence Count"]),
                        source=row["Source"],
                        scan_date=datetime.strptime(row["ScanDate"][:24], "%a, %d %b %Y %H:%M:%S"),
                        tags=[],
                        subject_id=row["Identifiers"],
                        subject_name=row["Description"],
                        subject_description=row["DependencyName"],
                        subject_location=row["DependencyPath"],
                        project_id=row["Project"],
                        project_name=row["Project"],
                        project_description="",
                        project_version="",
                        tool_name="Dependency Check",
                        tool_version=""
                    ))
                return issues
        except Exception as ex:
            logging.error("Failed to load, parse and map the report (%s)", ex)
            return []
