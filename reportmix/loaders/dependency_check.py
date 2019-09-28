"""
Dependency-Check report loader.
"""

import csv
import json
import logging
import re
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
    Dependency-Check report loader (CSV required, JSON optional).
    """

    def load(self) -> List[Issue]:
        """
        Load the Dependency Check report file (CSV required, JSON optional),
        parse it, map vulnerabilities to issues, and return the list.
        :return: List of vulnerabilities.
        """
        report_file_path = path.realpath(self.config["report_file"])
        if not (report_file_path.endswith(".csv") and path.exists(report_file_path)):
            logging.warning("Dependency check report ignored (file not found or not *.csv)")
            return []
        logging.debug("Loading report %s", report_file_path)
        try:
            # Load the JSON report to extract scan and project info
            json_report_file_path = re.sub(r"\.csv$", ".json", report_file_path)
            scan, project = {}, {}
            if path.exists(json_report_file_path):
                with open(json_report_file_path, "r", encoding="utf8") as json_report_file:
                    json_report = json.load(json_report_file)
                    scan = json_report["scanInfo"]
                    project = json_report["projectInfo"]

            # Load vulnerabilities from the CSV report and map them to issues
            with open(report_file_path, "r", newline='') as report_file:
                report = csv.DictReader(report_file, delimiter=',', quotechar='"')
                issues = []
                for row in report:
                    if "groupID" in project and "artifactID" in project:
                        project_identifier = project["groupID"] + ":" + project["artifactID"]
                    else:
                        project_identifier = row["Project"]
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
                            version=scan["engineVersion"] if "engineVersion" in scan else ""
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
                            identifier=project_identifier,
                            name=row["Project"],
                            version=project["version"] if "version" in project else ""
                        )
                    ))
                return issues
        except Exception as ex:
            logging.error("Failed to load, parse and map the report (%s)", ex)
            return []
