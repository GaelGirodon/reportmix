from reportmix.config.builder import ConfigBuilder
from reportmix.mixer import ReportMixer


def main():
    """Entry point for the application script"""
    config = ConfigBuilder().build()
    ReportMixer(config).merge()
