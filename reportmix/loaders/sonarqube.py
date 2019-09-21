"""
SonarQube report loader.
"""

import logging
from datetime import datetime
from typing import List

import requests

from reportmix.config.property import ConfigProperty
from reportmix.errors import AppError
from reportmix.loader import Loader
from reportmix.models.issue import Issue
from reportmix.models.project import Project
from reportmix.models.severity import SEVERITIES
from reportmix.models.subject import Subject
from reportmix.models.tool import Tool

# Possible values for types and statuses request parameters
TYPES = ["CODE_SMELL", "BUG", "VULNERABILITY", "SECURITY_HOTSPOT"]
DEFAULT_TYPES = TYPES[2]
STATUSES = ["OPEN", "CONFIRMED", "REOPENED", "RESOLVED", "CLOSED",
            "TO_REVIEW", "IN_REVIEW", "REVIEWED"]
DEFAULT_STATUSES = ",".join(STATUSES[0:3])

# Configuration properties
# https://docs.sonarqube.org/latest/analysis/analysis-parameters/
PROPERTIES: List[ConfigProperty] = [
    ConfigProperty("host_url", "the server URL", False, "http://localhost:9000"),
    ConfigProperty("login", "the login or authentication token"),
    ConfigProperty("password", "the password that goes with the login username"),
    ConfigProperty("project_key", "the project's unique key"),
    ConfigProperty("types", "issue types ({})".format(", ".join(TYPES)), False,
                   DEFAULT_TYPES, "^((T),)*(T)$".replace("T", "|".join(TYPES))),
    ConfigProperty("statuses", "issue statuses ({})".format(", ".join(STATUSES)), False,
                   DEFAULT_STATUSES, "^((S),)*(S)$".replace("S", "|".join(STATUSES)))
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
        cfg = self.config
        if not (cfg["host_url"] and cfg["project_key"]):
            logging.warning("SonarQube report ignored (required params: host_url, project_key)")
            return []

        # Authentication params
        auth = (cfg["login"] or "", cfg["password"] or "")

        # Fetch project info
        project_url = "{}/api/projects/search?q={}".format(cfg["host_url"], cfg["project_key"])
        try:
            resp = requests.get(project_url, auth=auth)
            project_resp = resp.json()["components"][0]
            project = Project(project_resp["key"], project_resp["name"], "")
        except Exception as ex:
            logging.error("Failed to get project information (%s)", ex)
            return []

        # Fetch issues info
        page_size = 500  # Number of issues in a result page
        page_index = 1  # Current page index
        total = page_size  # Total number of issues

        issues_base_url = "{}/api/issues/search?componentKeys={}&statuses={}&s=SEVERITY" \
                          "&asc=false&types={}&ps={}" \
            .format(cfg["host_url"], cfg["project_key"], DEFAULT_STATUSES,
                    cfg["types"] or DEFAULT_TYPES, page_size)
        try:
            issues = []
            # For each page (while total > max items fetched during the last iteration
            # and no more than 10000 issues have been requested)
            while total >= (page_index - 1) * page_size and page_index * page_size <= 10000:
                issues_url = issues_base_url + "&p=" + str(page_index)
                logging.debug("Fetching issues from %s", issues_url)
                # Request
                resp = requests.get(issues_url, auth=auth)
                result = resp.json()
                # Check response body
                if "paging" not in result or "issues" not in result:
                    logging.error("Server response is invalid ('paging' and 'issues' keys missing)")
                    raise AppError()
                total = result["paging"]["total"]
                fetched_count = (page_index - 1) * page_size + len(result["issues"])
                logging.debug("Fetched %d / %d issues", fetched_count, total)
                # Map issues
                for issue in result["issues"]:
                    # Severity
                    if issue["severity"] in SONARQUBE_SEVERITIES:
                        severity = SONARQUBE_SEVERITIES[issue["severity"]]
                    else:
                        severity = SEVERITIES[0]
                    # Subject location
                    location = issue["component"]
                    if "line" in issue:
                        location += ":" + str(issue["line"])
                    # Issue
                    issues.append(Issue(
                        ref=issue["key"],
                        identifier=issue["rule"],
                        name=issue["rule"],
                        type=issue["type"],
                        category=issue["type"],
                        description=issue["message"],
                        more=", ".join(issue["tags"]),
                        action=issue["message"],
                        effort=issue["effort"] if "effort" in issue else "",
                        analysis_date=datetime.strptime(project_resp["lastAnalysisDate"][:19],
                                                        "%Y-%m-%dT%H:%M:%S"),
                        severity=severity,
                        score="",
                        confidence="",
                        evidences=1,
                        source=issue["rule"],
                        source_date=datetime.strptime(issue["creationDate"][:19],
                                                      "%Y-%m-%dT%H:%M:%S"),
                        url="",
                        tool=Tool(
                            identifier="sonarqube",
                            name="SonarQube",
                            version=resp.headers["Sonar-Version"]
                        ),
                        subject=Subject(
                            identifier=issue["hash"] if "hash" in issue else "",
                            name=issue["component"],
                            description="",
                            version="",
                            location=location,
                            license=""
                        ),
                        project=project
                    ))
                page_index += 1  # Go to the next result page
            return issues
        except Exception as ex:
            logging.error("Failed to process issues (%s)", ex)
            return []


# SonarQube severities are a bit "excessive" so we define
# a custom map instead of using guess() function.
SONARQUBE_SEVERITIES = {
    "INFO": SEVERITIES[1],
    "MINOR": SEVERITIES[2],
    "MAJOR": SEVERITIES[3],
    "CRITICAL": SEVERITIES[4],
    "BLOCKER": SEVERITIES[5]
}
