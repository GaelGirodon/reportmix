from collections import OrderedDict
from datetime import datetime
from typing import List

from reportmix.report.severity import Severity


class Issue:
    """
    An issue extracted from a report.
    """

    def __init__(self, name: str, type: str, description: str, identifier: str, severity: Severity, score: str,
                 confidence: str, count: int, source: str, scan_date: datetime, tags: List[str],
                 subject_id: str, subject_name: str, subject_description: str, subject_location: str,
                 project_id: str, project_name: str, project_description: str, project_version: str,
                 tool_name: str, tool_version: str):
        """
        Initialize an issue reported about a subject (application feature, file, dependency, etc.) in a project.
        :param name: Issue short name
        :param type: Issue type (UPPER_CASE)
        :param description: A longer (but not too long) description of the issue
        :param identifier: Issue unique identifier
        :param severity: Issue severity
        :param score: Computed score for this issue
        :param confidence: Confidence about this issue
        :param count: Number of evidences of this issue
        :param source: Issue source database
        :param scan_date: Analysis date and time
        :param tags: Issue tags
        :param subject_id: Subject unique identifier (file path, fully qualified name, hash, ...)
        :param subject_name: Subject short name (class name, dependency name, ...)
        :param subject_description: A longer (but not too long) description of the subject
        :param subject_location: The location of the subject (full file path, full package name, URL, ...)
        :param project_id: Project unique identifier
        :param project_name: Project short common name
        :param project_description: Project description
        :param project_version: Project version (semantic version or something else)
        :param tool_name: Scan tool display name
        :param tool_version: Scan tool version
        """
        self.name = name
        self.type = type
        self.description = description
        self.identifier = identifier
        self.severity = severity
        self.score = score
        self.confidence = confidence
        self.count = count
        self.source = source
        self.scan_date = scan_date
        self.tags = tags
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.subject_description = subject_description
        self.subject_location = subject_location
        self.project_id = project_id
        self.project_name = project_name
        self.project_description = project_description
        self.project_version = project_version
        self.tool_name = tool_name
        self.tool_version = tool_version

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(vars(self))


#
# Constants
#

FIELD_NAMES = OrderedDict()
FIELD_NAMES["tool_name"] = "Tool name"
FIELD_NAMES["tool_version"] = "Tool version"
FIELD_NAMES["scan_date"] = "Scan date"
FIELD_NAMES["name"] = "Name"
FIELD_NAMES["description"] = "Description"
FIELD_NAMES["identifier"] = "Identifier"
FIELD_NAMES["type"] = "Type"
FIELD_NAMES["severity"] = "Severity"
FIELD_NAMES["count"] = "Count"
FIELD_NAMES["confidence"] = "Confidence"
FIELD_NAMES["score"] = "Score"
FIELD_NAMES["source"] = "Source"
FIELD_NAMES["subject_id"] = "Subject id"
FIELD_NAMES["subject_name"] = "Subject name"
FIELD_NAMES["subject_description"] = "Subject description"
FIELD_NAMES["subject_location"] = "Subject location"
FIELD_NAMES["project_id"] = "Project id"
FIELD_NAMES["project_name"] = "Project name"
FIELD_NAMES["project_description"] = "Project description"
FIELD_NAMES["project_version"] = "Project version"
FIELD_NAMES["tags"] = "Tags"

FIELDS = list(FIELD_NAMES.keys())


#
# Utilities
#

def issues_to_dicts(issues: List[Issue]):
    """
    Convert a list of Issue objects to a list of dictionaries.
    :param issues: List of Issue objects
    :return: List of dictionaries
    """
    return [vars(issue) for issue in issues]
