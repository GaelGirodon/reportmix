"""
HTML report exporter tests.
"""

from reportmix.exporters.html import limit, pretty_field


def test_limit():
    """
    Test the custom filter "limit"
    """
    tests = [
        {"value": "", "max_length": 64, "result": ""},
        {"value": "test", "max_length": 64, "result": "test"},
        {"value": "t<es>t", "max_length": 64, "result": "t&lt;es&gt;t"},
        {"value": "test", "max_length": 2, "result": '<span title="test">te...</span>'},
        {"value": "<test", "max_length": 2, "result": '<span title="&lt;test">&lt;t...</span>'},
    ]
    for test in tests:
        assert limit(test["value"], test["max_length"]) == test["result"]


def test_pretty_field():
    """
    Test the custom filter "prettyfield"
    """
    tests = [
        {"value": "", "result": ""},
        {"value": "a_key", "result": "A key"},
        {"value": "an_identifier", "result": "An id"},
    ]
    for test in tests:
        assert pretty_field(test["value"]) == test["result"]
