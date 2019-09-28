"""
Issue model tests.
"""

import re
from datetime import datetime

from reportmix.models.issue import Issue, FIELDS, FLAT_FIELDS, HASH_FIELDS, select_fields
from reportmix.models.meta import Meta
from reportmix.models.project import Project
from reportmix.models.severity import SEVERITIES
from reportmix.models.subject import Subject
from reportmix.models.tool import Tool

#
# Data
#

NOW = datetime.now()
ISSUE = Issue("ref", "identifier", "name", "type", "category", "description", "more", "action",
              "effort", None, SEVERITIES[1], "score", "confidence", 1, "source", None, "url",
              Tool("identifier", "name", "version"),
              Subject("identifier", "name", "description", "version", "location", "license"),
              Project("identifier", "name", "version"),
              Meta("product", "version", "organization", "client", str(NOW)),
              "hash")
ISSUE_DICT = {"ref": "ref", "identifier": "identifier", "name": "name", "type": "type",
              "category": "category", "description": "description", "more": "more",
              "action": "action", "effort": "effort", "analysis_date": None,
              "severity": SEVERITIES[1], "score": "score", "confidence": "confidence",
              "evidences": 1, "source": "source", "source_date": None, "url": "url",
              "tool": {"identifier": "identifier", "name": "name", "version": "version"},
              "subject": {
                  "identifier": "identifier", "name": "name", "description": "description",
                  "version": "version", "location": "location", "license": "license"
              },
              "project": {
                  "identifier": "identifier", "name": "name", "version": "version"
              },
              "meta": {
                  "product": "product", "version": "version", "organization": "organization",
                  "client": "client", "audit_date": str(NOW)
              },
              "hash": "hash"
              }
ISSUE_FLAT = {"ref": "ref", "identifier": "identifier", "name": "name", "type": "type",
              "category": "category", "description": "description", "more": "more",
              "action": "action", "effort": "effort", "analysis_date": None,
              "severity": SEVERITIES[1], "score": "score", "confidence": "confidence",
              "evidences": 1, "source": "source", "source_date": None, "url": "url", "hash": "hash",
              "tool_identifier": "identifier", "tool_name": "name", "tool_version": "version",
              "subject_identifier": "identifier", "subject_name": "name",
              "subject_description": "description", "subject_version": "version",
              "subject_location": "location", "subject_license": "license",
              "project_identifier": "identifier", "project_name": "name",
              "project_version": "version", "meta_product": "product", "meta_version": "version",
              "meta_organization": "organization", "meta_client": "client",
              "meta_audit_date": str(NOW)
              }


#
# Tests
#

def test_get_field():
    """
    Test the get_field function
    """
    tests = [
        {"field": "name", "value": "name"},
        {"field": "type", "value": "type"},
        {"field": "subject_name", "value": "name"},
        {"field": "meta_audit_date", "value": str(NOW)},
    ]
    for test in tests:
        assert ISSUE.get_field(test["field"]) == test["value"]


def test_compute_hash():
    """
    Test the compute_hash function
    """
    assert re.match("^[a-z0-9]{32}$", ISSUE.compute_hash(HASH_FIELDS))
    assert ISSUE.compute_hash([]) == ""


def test_to_dict():
    """
    Test Issue.to_dict()
    """
    assert ISSUE_DICT == ISSUE.to_dict()


def test_flatten():
    """
    Test Issue.flatten()
    """
    assert ISSUE.flatten() == ISSUE_FLAT


def test_fields():
    """
    Test the value of FIELDS and FLAT_FIELDS constants
    """
    assert FIELDS == list(ISSUE_DICT.keys())
    assert FLAT_FIELDS == list(ISSUE_FLAT.keys())


def test_select_fields():
    """
    Test the select_fields function
    """
    tests = [
        {"fields": ["identifier", "name", "type"], "result": ["identifier", "name", "type"]},
        {"fields": [], "result": []},
        {"fields": ["name", "type", "unknown"], "result": ["name", "type"]}
    ]
    for test in tests:
        assert select_fields(test["fields"]) == test["result"]
