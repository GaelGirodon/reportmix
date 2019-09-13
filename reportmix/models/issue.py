import inspect
from datetime import datetime
from typing import List, Dict, Union

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

    def __init__(self, identifier: str, name: str, type: str, description: str, date: datetime, tags: List[str],
                 severity: Severity, score: str, confidence: str, count: int, source: str,
                 tool: Tool, subject: Subject, project: Project):
        """
        Initialize an issue reported by a tool about a subject in a project.
        :param identifier: Issue unique identifier
        :param name: Issue short name
        :param type: Issue type (UPPER_CASE)
        :param description: A longer (but not too long) description of the issue
        :param date: Analysis date and time
        :param tags: Issue tags
        :param severity: Issue severity
        :param score: Computed score for this issue
        :param confidence: Confidence about this issue
        :param count: Number of evidences of this issue
        :param source: Issue source database
        :param tool: Scan tool
        :param subject: Subject (application feature, file, dependency, etc.) affected by the issue
        :param project: Project affected by the issue
        """
        self.identifier = identifier
        self.name = name
        self.type = type
        self.description = description
        self.date = date
        self.tags = tags
        self.severity = severity
        self.score = score
        self.confidence = confidence
        self.count = count
        self.source = source
        self.tool = tool
        self.subject = subject
        self.project = project

    def to_dict(self) -> Dict:
        d = vars(self).copy()
        d["tool"] = vars(self.tool).copy()
        d["subject"] = vars(self.subject).copy()
        d["project"] = vars(self.project).copy()
        return d

    def flatten(self, sub_sep: str = "_", list_sep: str = ", ") -> FlatIssue:
        """
        Flatten an issue to get a single level dictionary by mapping the object
        to a dictionary, bringing sub-dictionaries to the first level
        and concatenating lists of strings (["a", "b", "c"] => "a, b, c").
        Example: the attribute "name" of the sub-dictionary "project" will become
        an attribute of the root dictionary "project_name".
        :param sub_sep: Parent key and sub key separator
        :param list_sep: List items separator
        :return: The flattened issue
        """
        dict_issue = self.to_dict()
        result = dict_issue.copy()
        for key in ["tool", "subject", "project"]:  # Dictionaries
            for sub_key in dict_issue[key].keys():
                result[key + sub_sep + sub_key] = dict_issue[key][sub_key]
            result.pop(key)
        for key in ["tags"]:  # Lists
            result[key] = list_sep.join(dict_issue[key])
        return result


#
# Constants
#

# The list of issue fields
FIELDS = inspect.getfullargspec(Issue.__init__).args[1:]

# The list of issue fields after flattening
FLAT_FIELDS = [f for f in FIELDS if f not in ["tool", "subject", "project"]]
FLAT_FIELDS.extend(["tool_" + f for f in inspect.getfullargspec(Tool.__init__).args[1:]])
FLAT_FIELDS.extend(["subject_" + f for f in inspect.getfullargspec(Subject.__init__).args[1:]])
FLAT_FIELDS.extend(["project_" + f for f in inspect.getfullargspec(Project.__init__).args[1:]])
