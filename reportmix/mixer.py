import logging
from os import path
from typing import Dict, Union

from reportmix.config.builder import GLOBAL_CONFIG
from reportmix.exporters.csv import CsvExporter
from reportmix.exporters.html import HtmlExporter
from reportmix.exporters.json import JsonExporter
from reportmix.loaders.dependency_check import DependencyCheckLoader
from reportmix.loaders.sonarqube import SonarQubeLoader
from reportmix.report import issue


class ReportMixer:
    """
    Merge reports from multiple tools into one single file.
    """

    def __init__(self, config: Dict[str, Union[str, Dict[str, str]]]):
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
            "csv": CsvExporter(self.config),
            "json": JsonExporter(self.config),
            "html": HtmlExporter(self.config)
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
        logging.info("Loaded %d issue(s)", len(issues))

        if len(issues) == 0:
            logging.warning("No issues to export, exiting")
            return

        # Export
        # Format
        output_format: str = self.config["format"]
        if output_format not in self.exporters.keys():
            logging.error("Format %s is not supported", output_format)
            return
        # File
        output_dir: str = path.realpath(self.config["output_dir"])
        if not path.exists(output_dir) or not path.isdir(output_dir):
            logging.error("Invalid output directory %s", output_dir)
            return
        output_file_path = path.join(output_dir, "reportmix." + output_format)
        # Fields (intersection between all fields and selected fields)
        fields = issue.FIELDS
        only_fields = self.config["fields"].lower()
        if only_fields and only_fields != "all":
            only_fields_list = map(lambda f: f.strip(), self.config["fields"].split(","))
            fields = [f for f in only_fields_list if f in fields]
        # Exporter
        logging.debug("Exporting merged report (format: %s, fields: [%s])", output_format, ", ".join(fields))
        self.exporters[output_format].export(output_file_path, issues, fields)
        logging.info("Merged report exported: %s", output_file_path)
