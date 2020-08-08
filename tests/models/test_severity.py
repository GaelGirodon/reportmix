"""
Severity model tests.
"""

from typing import Dict, List, Union

from reportmix.models.severity import SEVERITIES, from_identifier, Severity


def test_from_identifier():
    """
    Test the from_identifier method
    """
    tests: List[Dict[str, Union[None, str, Severity]]] = [
        {"value": None, "expected": SEVERITIES[0]},
        {"value": "", "expected": SEVERITIES[0]},
        {"value": "LOW", "expected": SEVERITIES[2]},
        {"value": "CRITICAL", "expected": SEVERITIES[5]},
        {"value": "UNKNOWN!!", "expected": None},
    ]
    for test in tests:
        assert from_identifier(test["value"]) == test["expected"]
