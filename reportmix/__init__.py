import sys

from reportmix.config.builder import ConfigBuilder
from reportmix.errors import AppError
from reportmix.mixer import ReportMixer


def main():
    """Entry point for the application script"""

    # Load configuration
    try:
        config = ConfigBuilder().build()
    except AppError:
        sys.exit(1)

    # Merge reports
    try:
        ReportMixer(config).merge()
    except AppError:
        sys.exit(2)
