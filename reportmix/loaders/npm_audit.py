"""
npm audit report loader.
"""

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
PROPERTIES: List[ConfigProperty] = [
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
                for number, adv in advisories.items():
                    for finding in adv["findings"]:
                        issues.append(Issue(
                            ref=adv["id"] or number,
                            identifier=", ".join(adv["cves"]) or adv["title"],
                            name=adv["title"],
                            type="VULNERABILITY",
                            category=adv["cwe"],
                            description=str(adv["overview"]).strip(),
                            more="",
                            action=str(adv["recommendation"]).strip(),
                            effort="",
                            analysis_date=None,
                            severity=severity.guess(adv["severity"]),
                            score="",
                            confidence="",
                            evidences=len(adv["findings"]),
                            source="NPM Public Advisories",
                            source_date=datetime.strptime(adv["created"], "%Y-%m-%dT%H:%M:%S.%fZ"),
                            url=adv["url"],
                            tool=Tool(
                                identifier="npm_audit",
                                name="npm audit",
                                version=""
                            ),
                            subject=Subject(
                                identifier=adv["module_name"],
                                name=adv["module_name"],
                                description="",
                                version="Vulnerable versions: {}, Patched versions: {}".format(
                                    adv["vulnerable_versions"], adv["patched_versions"]),
                                location=finding["paths"][0] if finding["paths"] else "",
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
