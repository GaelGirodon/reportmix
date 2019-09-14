import json
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
properties: List[ConfigProperty] = [
    ConfigProperty("report_file", "path to the report file", True, "npm-audit.json")
]


class NpmAuditLoader(Loader):
    """
    npm security audit report loader.
    """

    def load(self) -> List[Issue]:
        """
        Load the npm audit report in JSON format,
        parse it, map vulnerabilities to issues, and return the list.
        :return: List of vulnerabilities.
        """
        report_file_path = path.realpath(self.config["report_file"])
        if not (report_file_path.endswith(".json") and path.exists(report_file_path)):
            logging.warning("npm audit report ignored (file not found or not *.json)")
            return []
        logging.debug("Loading report %s", report_file_path)
        try:
            with open(report_file_path, "r", encoding="utf8") as report_file:
                report = json.load(report_file)
                advisories = report["advisories"]
                issues = []
                for number, a in advisories.items():
                    for f in a["findings"]:
                        issues.append(Issue(
                            ref=a["id"],
                            identifier=", ".join(a["cves"]) or a["title"],
                            name=a["title"],
                            type="VULNERABILITY",
                            category=a["cwe"],
                            description=a["overview"],
                            more="",
                            action=a["recommendation"],
                            effort="",
                            analysis_date=None,
                            severity=severity.guess(a["severity"]),
                            score="",
                            confidence="",
                            evidences=len(a["findings"]),
                            source="NPM Public Advisories",
                            source_date=datetime.strptime(a["created"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                            url=a["url"],
                            tool=Tool(
                                identifier="npm_audit",
                                name="npm audit",
                                version=""
                            ),
                            subject=Subject(
                                identifier=a["module_name"],
                                name=a["module_name"],
                                description="",
                                version="Vulnerable versions: {}, Patched versions: {}".format(
                                    a["vulnerable_versions"], a["patched_versions"]),
                                location=f["paths"][0] if len(f["paths"]) > 0 else "",
                                license=""
                            ),
                            project=Project(
                                identifier="",
                                name="",
                                version=""
                            )
                        ))
                return issues
        except Exception as ex:
            logging.error("Failed to load, parse and map the report (%s)", ex)
            return []
