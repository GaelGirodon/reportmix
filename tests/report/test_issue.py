from datetime import datetime

from reportmix.models.issue import Issue, FIELDS, FLAT_FIELDS
from reportmix.models.project import Project
from reportmix.models.severity import SEVERITIES
from reportmix.models.subject import Subject
from reportmix.models.tool import Tool

#
# Data
#

date = datetime.now()
issue = Issue("identifier", "name", "type", "description", date, ["tags"], SEVERITIES[1],
              "score", "confidence", 1, "source", Tool("identifier", "name", "version"),
              Subject("identifier", "name", "description", "location"),
              Project("identifier", "name", "description", "version"))
dict_issue = {"identifier": "identifier", "name": "name", "type": "type", "description": "description",
              "date": date, "tags": ["tags"], "severity": SEVERITIES[1], "score": "score", "confidence": "confidence",
              "count": 1, "source": "source",
              "tool": {"identifier": "identifier", "name": "name", "version": "version"},
              "subject": {
                  "identifier": "identifier", "name": "name", "description": "description", "location": "location"
              },
              "project": {
                  "identifier": "identifier", "name": "name", "description": "description", "version": "version"
              }}
flat_issue = {"identifier": "identifier", "name": "name", "type": "type", "description": "description",
              "date": date, "tags": "tags", "severity": SEVERITIES[1], "score": "score", "confidence": "confidence",
              "count": 1, "source": "source", "tool_identifier": "identifier", "tool_name": "name",
              "tool_version": "version", "subject_identifier": "identifier", "subject_name": "name",
              "subject_description": "description", "subject_location": "location", "project_identifier": "identifier",
              "project_name": "name", "project_description": "description", "project_version": "version"}


#
# Tests
#

def test_to_dict():
    """
    Test Issue.to_dict()
    """
    assert dict_issue == issue.to_dict()


def test_flatten():
    """
    Test Issue.flatten()
    """
    assert issue.flatten() == flat_issue


def test_fields():
    """
    Test the value of FIELDS and FLAT_FIELDS constants
    """
    assert FIELDS == list(dict_issue.keys())
    assert FLAT_FIELDS == list(flat_issue.keys())
