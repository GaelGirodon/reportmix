class Subject:
    """
    A subject affected by an issue (feature, file, class, dependency, ...).
    """

    def __init__(self, identifier: str, name: str, description: str, location: str):
        """
        Initialize a subject affected by an issue.
        :param identifier: Subject unique identifier (file path, fully qualified name, hash, ...)
        :param name: Subject short name (class name, dependency name, ...)
        :param description: A longer (but not too long) description of the subject
        :param location: The location of the subject (full file path, full package name, URL, ...)
        """
        self.identifier = identifier
        self.name = name
        self.description = description
        self.location = location
