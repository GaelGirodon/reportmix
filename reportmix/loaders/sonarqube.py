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
types = ["CODE_SMELL", "BUG", "VULNERABILITY", "SECURITY_HOTSPOT"]
default_types = types[2]
statuses = ["OPEN", "CONFIRMED", "REOPENED", "RESOLVED", "CLOSED", "TO_REVIEW", "IN_REVIEW", "REVIEWED"]
default_statuses = ",".join(statuses[0:3])

# Configuration properties
# https://docs.sonarqube.org/latest/analysis/analysis-parameters/
properties: List[ConfigProperty] = [
    ConfigProperty("host_url", "the server URL", False, "http://localhost:9000"),
    ConfigProperty("login", "the login or authentication token"),
    ConfigProperty("password", "the password that goes with the login username"),
    ConfigProperty("project_key", "the project's unique key"),
    ConfigProperty("types", "issue types ({})".format(", ".join(types)), False, default_types,
                   "^((T),)*(T)$".replace("T", "|".join(types))),
    ConfigProperty("statuses", "issue statuses ({})".format(", ".join(statuses)), False, default_statuses,
                   "^((S),)*(S)$".replace("S", "|".join(statuses)))
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

        # Authentication params
        auth = (self.config["login"] or "", self.config["password"] or "")

        # Fetch project info
        project_url = "{}/api/projects/search?q={}".format(self.config["host_url"], self.config["project_key"])
        try:
            resp = requests.get(project_url, auth=auth)
            p = resp.json()["components"][0]
            project = Project(p["key"], p["name"], "")
        except Exception as ex:
            logging.error("Failed to get project information (%s)", ex)
            return []

        # Fetch issues info
        page_size = 500  # Number of issues in a result page
        page_index = 1  # Current page index
        total = page_size  # Total number of issues

        issues_base_url = "{}/api/issues/search?componentKeys={}&statuses={}&s=SEVERITY&asc=false&types={}&ps={}" \
            .format(self.config["host_url"], self.config["project_key"],
                    default_statuses, self.config["types"] or default_types, page_size)
        try:
            issues = []
            # For each page
            while total >= (page_index - 1) * page_size:  # While total > max items fetched during the last iteration
                issues_url = issues_base_url + "&p=" + str(page_index)
                logging.debug("Fetching issues from %s", issues_url)
                # Request
                resp = requests.get(issues_url, auth=auth)
                result = resp.json()
                # Check response body
                if "paging" not in result or "issues" not in result:
                    logging.error("Server response is invalid (missing 'paging' and 'issues' keys)")
                    raise AppError()
                total = result["paging"]["total"]
                logging.debug("Fetched %d / %d issues", (page_index - 1) * page_size + len(result["issues"]), total)
                # Map issues
                for issue in result["issues"]:
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
                        analysis_date=datetime.strptime(p["lastAnalysisDate"], "%Y-%m-%dT%H:%M:%S%z"),
                        severity=severities[issue["severity"]] if issue["severity"] in severities else SEVERITIES[0],
                        score="",
                        confidence="",
                        evidences=1,
                        source=issue["rule"],
                        source_date=datetime.strptime(issue["creationDate"], "%Y-%m-%dT%H:%M:%S%z"),
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
                            location=issue["component"] + (":" + str(issue["line"]) if "line" in issue else ""),
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
severities = {
    "INFO": SEVERITIES[1],
    "MINOR": SEVERITIES[2],
    "MAJOR": SEVERITIES[3],
    "CRITICAL": SEVERITIES[4],
    "BLOCKER": SEVERITIES[5]
}
