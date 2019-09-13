from typing import List, Union


class Severity:
    """
    An issue severity.
    """

    def __init__(self, id: str, name: str):
        """
        Initialize an issue severity from a name and an id.
        :param id: Severity id
        :param name: Severity display name
        """
        self.id = id
        self.name = name

    def __str__(self) -> str:
        return self.id

    def __repr__(self) -> str:
        return "'" + self.id + "'"


#
# Constants
#

# Severities (based on CVSS v3 Ratings)
SEVERITIES: List[Severity] = [
    Severity("NOT_DEFINED", "Not Defined"),
    Severity("NONE", "None"),
    Severity("LOW", "Low"),
    Severity("MEDIUM", "Medium"),
    Severity("HIGH", "High"),
    Severity("CRITICAL", "Critical")
]


#
# Helpers
#

def guess(value: str) -> Union[Severity, None]:
    """
    Try to guess a severity from a given input value.
    :param value: Input value.
    :return: Guessed severity (None if guess failed)
    """
    val = value.strip() if value else value
    if not val:
        return SEVERITIES[0]
    val = val.lower()
    if val == "info" or val == "none":
        return SEVERITIES[1]
    if val == "low" or val == "minor":
        return SEVERITIES[2]
    elif val == "medium" or val == "moderate":
        return SEVERITIES[3]
    elif val == "high" or val == "major":
        return SEVERITIES[4]
    elif val == "critical" or val == "blocker":
        return SEVERITIES[5]
    else:
        return None
