"""
Main class.
"""

import logging
from os import path
from typing import Dict, Union, List

from reportmix.config.builder import GLOBAL_CONFIG
from reportmix.errors import AppError
from reportmix.exporters.csv import CsvExporter
from reportmix.exporters.html import HtmlExporter
from reportmix.exporters.json import JsonExporter
from reportmix.loaders.dependency_check import DependencyCheckLoader
from reportmix.loaders.npm_audit import NpmAuditLoader
from reportmix.loaders.sonarqube import SonarQubeLoader
from reportmix.models.issue import FLAT_FIELDS, Issue
from reportmix.models.meta import Meta


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
        self.meta_config = config["meta"]
        self.loaders = {
            "dependency_check": DependencyCheckLoader(config["dependency_check"]),
            "npm_audit": NpmAuditLoader(config["npm_audit"]),
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
        issues = self._load()
        if not issues:
            logging.warning("No issues to export, exiting")
            raise AppError()
        # Export
        self._export(issues)

    def _load(self) -> List[Issue]:
        """
        Load and merge issues from all loaders.
        Set metadata fields from configuration.
        :return: List of issues
        """
        # Load and merge
        issues = []
        logging.info("Merge reports: %s", ", ".join(self.loaders.keys()))
        for name, loader in self.loaders.items():
            logging.info("Loading %s report", name)
            issues.extend(loader.load())
        logging.info("Loaded %d issue(s)", len(issues))
        # Set metadata fields
        meta = Meta(self.meta_config["product"], self.meta_config["version"],
                    self.meta_config["organization"], self.meta_config["client"],
                    self.meta_config["audit_date"])
        for issue in issues:
            issue.meta = meta
        return issues

    def _export(self, issues: List[Issue]):
        """
        Export a list of issues to a report file.
        """
        # File
        output_dir: str = path.realpath(self.config["output_dir"])
        if not path.exists(output_dir) or not path.isdir(output_dir):
            logging.error("Invalid output directory %s", output_dir)
            raise AppError()

        # Fields (intersection between all fields and selected fields)
        fields = FLAT_FIELDS
        only_fields = self.config["fields"].lower()
        if only_fields and only_fields != "all":
            only_fields_list = map(lambda f: f.strip(), self.config["fields"].split(","))
            fields = [f for f in only_fields_list if f in fields]

        # Exporter
        for output_format in self.config["formats"].split(","):
            output_file_path = path.join(output_dir, "reportmix." + output_format)
            logging.debug("Exporting merged report (format: %s, fields: [%s])",
                          output_format, ", ".join(fields))
            self.exporters[output_format].export(output_file_path, issues, fields)
            logging.info("Merged report exported: %s", output_file_path)
