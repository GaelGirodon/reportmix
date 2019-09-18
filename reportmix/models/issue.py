"""
Main issue model.
"""

import inspect
from datetime import datetime
from typing import Dict, Union, Optional

from reportmix.models.meta import Meta
from reportmix.models.project import Project
from reportmix.models.severity import Severity
from reportmix.models.subject import Subject
from reportmix.models.tool import Tool

# An issue as a dictionary with only first level items (no sub-dictionary or list).
FlatIssue = Dict[str, Union[str, int, datetime]]


class Issue:
    """
    An issue extracted from a report.
    """

    def __init__(self, ref: str, identifier: str, name: str, type: str, category: str,
                 description: str, more: str, action: str, effort: str,
                 analysis_date: Optional[datetime], severity: Severity, score: str,
                 confidence: str, evidences: int, source: str, source_date: Optional[datetime],
                 url: str, tool: Tool, subject: Subject, project: Project, meta: Meta = None):
        """
        Initialize an issue reported by a tool about a subject in a project.
        :param ref: Issue technical reference/identifier
        :param identifier: Issue unique identifier (CVE, rule, ...)
        :param name: Issue short name
        :param type: Issue type (UPPER_CASE)
        :param category: Issue category (e.g. CWE)
        :param description: A longer (but not too long) description of the issue
        :param more: More information about the issue
        :param action: Recommended action to solve the issue
        :param effort: Necessary effort to solve the issue (debt)
        :param analysis_date: Analysis / report creation date and time
        :param severity: Issue severity
        :param score: Computed score for this issue
        :param confidence: Confidence about this issue
        :param evidences: Number of evidences of this issue
        :param source: Issue source database
        :param source_date: Advisory, rule or ticket creation date
        :param url: Advisory, rule or ticket URL
        :param tool: Scan tool
        :param subject: Subject (application feature, file, dependency, etc.) affected by the issue
        :param project: Project affected by the issue
        :param meta: User-defined metadata
        """
        self.ref = ref
        self.identifier = identifier
        self.name = name
        self.type = type
        self.category = category
        self.description = description
        self.more = more
        self.action = action
        self.effort = effort
        self.analysis_date = analysis_date
        self.severity = severity
        self.score = score
        self.confidence = confidence
        self.evidences = evidences
        self.source = source
        self.source_date = source_date
        self.url = url
        self.tool = tool
        self.subject = subject
        self.project = project
        self.meta = meta

    def to_dict(self) -> Dict:
        """
        Map the issue to a dictionary (deep mapping).
        :return: The issue as a dictionary
        """
        issue = vars(self).copy()
        issue["tool"] = vars(self.tool).copy()
        issue["subject"] = vars(self.subject).copy()
        issue["project"] = vars(self.project).copy()
        issue["meta"] = vars(self.meta).copy()
        return issue

    def flatten(self, sub_sep: str = "_") -> FlatIssue:
        """
        Flatten an issue to get a single level dictionary by mapping the object
        to a dictionary and bringing sub-dictionaries to the first level.
        Example: the attribute "name" of the sub-dictionary "project" will become
        an attribute of the root dictionary "project_name".
        :param sub_sep: Parent key and sub key separator
        :return: The flattened issue
        """
        dict_issue = self.to_dict()
        result = dict_issue.copy()
        for key in ["tool", "subject", "project", "meta"]:  # Sub-dictionaries
            for sub_key in dict_issue[key].keys():
                result[key + sub_sep + sub_key] = dict_issue[key][sub_key]
            result.pop(key)
        return result


#
# Constants
#

# The list of issue fields
FIELDS = inspect.getfullargspec(Issue.__init__).args[1:]

# The list of issue fields after flattening
FLAT_FIELDS = [f for f in FIELDS if f not in ["tool", "subject", "project", "meta"]]
FLAT_FIELDS.extend(["tool_" + f for f in inspect.getfullargspec(Tool.__init__).args[1:]])
FLAT_FIELDS.extend(["subject_" + f for f in inspect.getfullargspec(Subject.__init__).args[1:]])
FLAT_FIELDS.extend(["project_" + f for f in inspect.getfullargspec(Project.__init__).args[1:]])
FLAT_FIELDS.extend(["meta_" + f for f in inspect.getfullargspec(Meta.__init__).args[1:]])
