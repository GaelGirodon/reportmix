"""
Metadata model.
"""

from datetime import datetime
from typing import List

from reportmix.config.property import ConfigProperty


class Meta:
    """
    Metadata (user-defined global fields).
    """

    def __init__(self, product: str, version: str, organization: str, client: str,
                 audit_date: str):
        """
        Initialize metadata.
        :param product: Product name
        :param version: Product version
        :param organization: Organization name
        :param client: Client name
        :param audit_date: Audit date (default: now())
        """
        self.product = product
        self.version = version
        self.organization = organization
        self.client = client
        self.audit_date = audit_date or str(datetime.now().replace(microsecond=0))


# Metadata configuration properties
PROPERTIES: List[ConfigProperty] = [
    ConfigProperty("product", "the product name"),
    ConfigProperty("version", "the product version"),
    ConfigProperty("organization", "the organization name"),
    ConfigProperty("client", "the client name"),
    ConfigProperty("audit_date", "the audit date", False, "now()")
]
