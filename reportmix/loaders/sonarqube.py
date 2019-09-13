import logging
from datetime import datetime
from typing import List

import requests

from reportmix.config.property import ConfigProperty
from reportmix.loader import Loader
from reportmix.models import severity
from reportmix.models.issue import Issue
from reportmix.models.project import Project
from reportmix.models.subject import Subject
from reportmix.models.tool import Tool

# Configuration properties
# https://docs.sonarqube.org/latest/analysis/analysis-parameters/
properties: List[ConfigProperty] = [
    ConfigProperty("host_url", "the server URL", True, "http://localhost:9000"),
    ConfigProperty("login", "the login or authentication token"),
    ConfigProperty("password", "the password that goes with the login username"),
    ConfigProperty("project_key", "the project's unique key", True),
    ConfigProperty("types", "comma-separated list of types (CODE_SMELL,BUG,VULNERABILITY,SECURITY_HOTSPOT)",
                   True, "VULNERABILITY")
]


class SonarQubeLoader(Loader):
    """
    SonarQube project report loader using the Web API.
    """

    def load(self) -> List[Issue]:
        """
        Load project issues from the SonarQube Web API,
        parse them, map them, and return the list.
        :return: List of vulnerabilities.
        """
        if not (self.config["host_url"] and self.config["project_key"]):
            logging.warning("SonarQube report ignored (missing params: host_url and/or project_key)")
            return []
        # Build API URL
        url = self.config["host_url"] + "/api/issues/search"
        url += "?componentKeys=" + self.config["project_key"]
        url += "&statuses=OPEN,CONFIRMED,REOPENED&s=STATUS&types=" + (self.config["types"] or "") + "&facets=severities"
        # Fetch and map issues
        try:
            logging.debug("Fetching issues from %s", url)
            r = requests.get(url, auth=(self.config["login"] or "", self.config["password"] or ""))
            result = r.json()
            logging.debug("Fetched %d issues", result["total"])
            issues = []
            for issue in result["issues"]:
                issues.append(Issue(
                    name=issue["rule"],
                    type=issue["type"],
                    description=issue["message"],
                    identifier=issue["key"],
                    severity=severity.guess(issue["severity"]),
                    score="",
                    confidence="",
                    count=1,
                    source=issue["rule"],
                    date=datetime.strptime(issue["creationDate"], "%Y-%m-%dT%H:%M:%S%z"),
                    tags=issue["tags"],
                    subject=Subject(
                        identifier="",
                        name="",
                        description="",
                        location=issue["component"] + (":" + str(issue["line"]) if "line" in issue else "")
                    ),
                    project=Project(
                        identifier=issue["project"],
                        name=issue["project"],
                        description="",
                        version=""
                    ),
                    tool=Tool(
                        identifier="sonarqube",
                        name="SonarQube",
                        version=r.headers["Sonar-Version"]
                    )
                ))
            return issues
        except Exception as ex:
            logging.error("Failed to process issues (%s)", ex)
            return []
