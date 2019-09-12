import logging
from os import path

from reportmix.config.builder import GLOBAL_CONFIG
from reportmix.exporters.csv import CsvExporter
from reportmix.exporters.html import HtmlExporter
from reportmix.exporters.json import JsonExporter
from reportmix.loaders.dependency_check import DependencyCheckLoader
from reportmix.loaders.sonarqube import SonarQubeLoader


class ReportMixer:
    """
    Merge reports from multiple tools into one single file.
    """

    def __init__(self, config):
        """
        Initialize the report mixer.
        :param config: Configuration.
        """
        self.config = config[GLOBAL_CONFIG]
        self.loaders = {
            "dependency_check": DependencyCheckLoader(config["dependency_check"]),
            "sonarqube": SonarQubeLoader(config["sonarqube"])
        }
        self.exporters = {
            "csv": CsvExporter(),
            "json": JsonExporter(),
            "html": HtmlExporter()
        }

    def merge(self) -> None:
        """
        Load and merge all available reports.
        """
        # Load and merge
        issues = []
        logging.info("Merge reports: %s", ", ".join(self.loaders.keys()))
        for name, loader in self.loaders.items():
            logging.info("Loading %s report", name)
            issues.extend(loader.load())
        logging.debug("Issues: %s", issues)
        # Export
        output_format: str = self.config["format"]
        if output_format not in self.exporters.keys():
            logging.error("Format %s is not supported", output_format)
            return
        output_dir: str = path.realpath(self.config["output_dir"])
        if not path.exists(output_dir) or not path.isdir(output_dir):
            logging.error("Invalid output directory %s", output_dir)
            return
        output_file_path = path.join(output_dir, "reportmix." + output_format)
        logging.info("Exporting merged report with format %s to %s", output_format, output_file_path)
        self.exporters[output_format].export(output_file_path, issues)
