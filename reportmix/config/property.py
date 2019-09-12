class ConfigProperty:
    """
    A configuration property available through the CLI or file configuration.
    """

    def __init__(self, name: str, description: str, mandatory: bool = False, default: str = None):
        """
        Initialize a configuration property.
        :param name: Property name (format: snake_case)
        :param description: Property short help message
        :param mandatory: Set the property as required
        :param default: Property default value
        """
        self.name = name
        self.description = description
        self.mandatory = mandatory
        self.default = default
