"""
Configuration property.
"""

import re


class ConfigProperty:
    """
    A configuration property available through the CLI or file configuration.
    """

    def __init__(self, name: str, description: str, mandatory: bool = False,
                 default: str = None, pattern: str = None):
        """
        Initialize a configuration property.
        :param name: Property name (format: snake_case)
        :param description: Property short help message
        :param mandatory: Set the property as required (a loader property can't be mandatory,
        if a property is missing, log a warning and ignore this loader)
        :param default: Property default value
        :param pattern: Validation pattern
        """
        self.name = name
        self.description = description
        self.mandatory = mandatory
        self.default = default
        self.pattern = pattern

    def is_valid(self, value) -> bool:
        """
        Check if a given value is valid for this property.
        :param value: The value to test
        :return: true if the value is valid
        """
        required_ok = not self.mandatory or value
        pattern_ok = not self.pattern or re.match(self.pattern, value)
        return required_ok and pattern_ok
