#!/usr/bin/env python

"""
Application main function and version.
"""

import logging
import sys

from reportmix.config.builder import ConfigBuilder
from reportmix.mixer import ReportMixer

__version__ = "0.6.0"


def main():
    """
    Entry point for the application script.
    """

    # Load configuration
    try:
        config = ConfigBuilder(__version__).build()
    except Exception as ex:
        logging.error(ex)
        sys.exit(1)

    # Merge reports
    try:
        ReportMixer(config).merge()
    except Exception as ex:
        logging.error(ex)
        sys.exit(2)


if __name__ == "__main__":
    main()
