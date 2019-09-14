from reportmix.exporters.html import limit, pretty_field


def test_limit():
    """
    Test the custom filter "limit"
    """
    tests = [
        {"value": "", "max_length": 64, "result": ""},
        {"value": "test", "max_length": 64, "result": "test"},
        {"value": "test", "max_length": 2, "result": '<span title="test">te...</span>'},
    ]
    for t in tests:
        assert limit(t["value"], t["max_length"]) == t["result"]


def test_pretty_field():
    """
    Test the custom filter "prettyfield"
    """
    tests = [
        {"value": "", "result": ""},
        {"value": "a_key", "result": "A key"},
        {"value": "an_identifier", "result": "An id"},
    ]
    for t in tests:
        assert pretty_field(t["value"]) == t["result"]
