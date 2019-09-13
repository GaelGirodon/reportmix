class Project:
    """
    A scanned project.
    """

    def __init__(self, identifier: str, name: str, description: str, version: str):
        """
        Initialize a scanned project.
        :param identifier: Project unique identifier
        :param name: Project short common name
        :param description: Project description
        :param version: Project version (semantic version or something else)
        """
        self.identifier = identifier
        self.name = name
        self.description = description
        self.version = version
