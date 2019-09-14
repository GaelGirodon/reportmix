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
issue = Issue("ref", "identifier", "name", "type", "category", "description", "more", "action", "effort",
              None, SEVERITIES[1], "score", "confidence", 1, "source", None, "url",
              Tool("identifier", "name", "version"),
              Subject("identifier", "name", "description", "version", "location", "license"),
              Project("identifier", "name", "version"))
dict_issue = {"ref": "ref", "identifier": "identifier", "name": "name", "type": "type", "category": "category",
              "description": "description", "more": "more", "action": "action", "effort": "effort",
              "analysis_date": None, "severity": SEVERITIES[1], "score": "score", "confidence": "confidence",
              "evidences": 1, "source": "source", "source_date": None, "url": "url",
              "tool": {"identifier": "identifier", "name": "name", "version": "version"},
              "subject": {
                  "identifier": "identifier", "name": "name", "description": "description",
                  "version": "version", "location": "location", "license": "license"
              },
              "project": {
                  "identifier": "identifier", "name": "name", "version": "version"
              }}
flat_issue = {"ref": "ref", "identifier": "identifier", "name": "name", "type": "type", "category": "category",
              "description": "description", "more": "more", "action": "action", "effort": "effort",
              "analysis_date": None, "severity": SEVERITIES[1], "score": "score", "confidence": "confidence",
              "evidences": 1, "source": "source", "source_date": None, "url": "url",
              "tool_identifier": "identifier", "tool_name": "name", "tool_version": "version",
              "subject_identifier": "identifier", "subject_name": "name", "subject_description": "description",
              "subject_version": "version", "subject_location": "location", "subject_license": "license",
              "project_identifier": "identifier", "project_name": "name", "project_version": "version"
              }


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
