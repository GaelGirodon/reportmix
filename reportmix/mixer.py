"""
Main class.
"""

import logging
from os import path
from typing import Dict, Union

from reportmix.config.builder import GLOBAL_CONFIG
from reportmix.errors import LoadingError, AppError
from reportmix.exporters.csv import CsvExporter
from reportmix.exporters.html import HtmlExporter
from reportmix.exporters.json import JsonExporter
from reportmix.loaders.dependency_check import DependencyCheckLoader
from reportmix.loaders.npm_audit import NpmAuditLoader
from reportmix.loaders.reportmix import ReportMixLoader
from reportmix.loaders.sonarqube import SonarQubeLoader
from reportmix.models.issue import FLAT_FIELDS, HASH_FIELDS, select_fields
from reportmix.models.meta import Meta
from reportmix.models.report import Report


class ReportMixer:
    """
    Merge reports from multiple tools into one single file.
    """

    def __init__(self, config: Dict[str, Union[str, Dict[str, str]]]):
        """
        Initialize the report mixer.
        :param config: Configuration
        """
        self.config = config[GLOBAL_CONFIG]
        self.meta_config = config["meta"]
        self.loaders = {
            "dependency_check": DependencyCheckLoader(config["dependency_check"]),
            "npm_audit": NpmAuditLoader(config["npm_audit"]),
            "sonarqube": SonarQubeLoader(config["sonarqube"]),
            "reportmix": ReportMixLoader(config["reportmix"])
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
        report = self._load()
        if not report.issues:
            logging.warning("No issue has been loaded, report(s) will be empty")
        # Export
        self._export(report)

    def _load(self) -> Report:
        """
        Load and merge issues from all loaders.
        Set metadata fields from configuration.
        :return: Loaded issues
        """
        # Load and merge
        report = Report([], [])
        logging.info("Merge reports: %s", ", ".join(self.loaders.keys()))
        for name, loader in self.loaders.items():
            logging.info("Loading %s report", name)
            try:
                report.extend(loader.load())
            except LoadingError as err:
                logging.warning("%s report not loaded: %s", name, err)
        logging.info("Loaded %d issue(s) from %d tools(s)", len(report.issues), len(report.tools))
        # Set metadata fields
        hash_fields = select_fields(self.config["hash"] or HASH_FIELDS)
        for issue in report.issues:
            issue.meta = Meta(self.meta_config["product"], self.meta_config["version"],
                              self.meta_config["organization"], self.meta_config["client"],
                              self.meta_config["audit_date"])
            issue.hash = issue.compute_hash(hash_fields)
        return report

    def _export(self, report: Report):
        """
        Export a list of issues to a report file.
        :param report: Report with issues to export
        """
        # File
        output_dir: str = path.realpath(self.config["output_dir"])
        if not path.exists(output_dir) or not path.isdir(output_dir):
            raise AppError("Invalid output directory {}".format(output_dir))

        # Fields (intersection between all fields and selected fields)
        only_fields = self.config["fields"].lower()
        fields = FLAT_FIELDS if only_fields == "all" else select_fields(only_fields)

        # Exporter
        for output_format in self.config["formats"].split(","):
            output_file_path = path.join(output_dir, "reportmix." + output_format)
            logging.debug("Exporting merged report (format: %s, fields: [%s])",
                          output_format, ", ".join(fields))
            self.exporters[output_format].export(report, output_file_path, fields)
            logging.info("Merged report exported: %s", output_file_path)
