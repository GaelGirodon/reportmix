"""
Severity model.
"""

from typing import List, Union


class Severity:
    """
    An issue severity.
    """

    def __init__(self, identifier: str, name: str):
        """
        Initialize an issue severity from a name and an id.
        :param identifier: Severity unique identifier
        :param name: Severity display name
        """
        self.identifier = identifier
        self.name = name

    def __str__(self) -> str:
        return self.identifier

    def __repr__(self) -> str:
        return "'" + self.identifier + "'"


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
    # else
    val = val.lower()
    sev = None
    if val in ("info", "none"):
        sev = SEVERITIES[1]
    elif val in ("low", "minor"):
        sev = SEVERITIES[2]
    elif val in ("medium", "moderate"):
        sev = SEVERITIES[3]
    elif val in ("high", "major"):
        sev = SEVERITIES[4]
    elif val in ("critical", "blocker"):
        sev = SEVERITIES[5]
    return sev
