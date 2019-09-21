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

    def __init__(self, product: str, version: str, company: str, customer: str, audit_date: str):
        """
        Initialize metadata.
        :param product: Product name
        :param version: Product version
        :param company: Company name
        :param customer: Customer name
        :param audit_date: Audit date (default: now())
        """
        self.product = product
        self.version = version
        self.company = company
        self.customer = customer
        self.audit_date = audit_date or str(datetime.now().replace(microsecond=0))


# Metadata configuration properties
PROPERTIES: List[ConfigProperty] = [
    ConfigProperty("product", "the product name"),
    ConfigProperty("version", "the product version"),
    ConfigProperty("company", "the company name"),
    ConfigProperty("customer", "the customer name"),
    ConfigProperty("audit_date", "the audit date")
]
