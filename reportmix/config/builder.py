"""
Configuration and CLI management.
"""

import argparse
import configparser
import logging
from os.path import exists, realpath
from typing import Dict

from reportmix.config.property import ConfigProperty
from reportmix.errors import AppError
from reportmix.loaders import dependency_check, sonarqube, npm_audit
from reportmix.models import meta

# Configuration global group name (for global configuration properties)
GLOBAL_CONFIG = "global"

# Global configuration properties
PROPERTIES = [
    ConfigProperty("output_dir", "the location to write the report", True, "./"),
    ConfigProperty("config_file", "the path to the configuration file", True, ".reportmix"),
    ConfigProperty("formats", "Report formats to be generated (csv, html, json)",
                   True, "html", "^((F),)*(F)$".replace("F", "csv|html|json")),
    ConfigProperty("fields", "fields to include in the output report (CSV and HTML only)",
                   True, "all", "^((\\w+),)*(\\w+)$"),
    ConfigProperty("logo", "the URL to the company logo to display on the HTML report", False)
]


class ConfigBuilder:
    """
    Build the configuration from the configuration file and command-line arguments.
    """

    def __init__(self, version: str):
        """
        Initialize the configuration builder.
        :param version: Application version number
        """

        # Configuration properties
        self.properties = {
            GLOBAL_CONFIG: PROPERTIES,
            "meta": meta.PROPERTIES,
            "dependency_check": dependency_check.PROPERTIES,
            "npm_audit": npm_audit.PROPERTIES,
            "sonarqube": sonarqube.PROPERTIES
        }

        # Initialize the command-line argument parser
        self.parser = argparse.ArgumentParser(
            description='Merge reports from multiple tools into one single file.')
        self.parser.add_argument("-V", "--version", action="version",
                                 version="ReportMix " + version)
        self.parser.add_argument("-v", "--verbose", action="store_true",
                                 help="run verbosely (display DEBUG logging)")

        for group, props in self.properties.items():
            for prop in props:
                # Name
                if group == GLOBAL_CONFIG:
                    name = "--" + prop.name
                else:
                    name = "--" + group + "." + prop.name
                # Description
                description = prop.description
                if prop.default:
                    description += " (default: {})".format(prop.default)
                # Argument
                self.parser.add_argument(name, type=str, metavar=prop.name.upper(),
                                         default=argparse.SUPPRESS, help=description)

    def build(self) -> Dict[str, Dict[str, str]]:
        """
        Build configuration from CLI, file and default values.
        :return: Loaded configuration
        """

        # Build default configuration
        config = {}
        for group, props in self.properties.items():
            for prop in props:
                config.setdefault(group, {})[prop.name] = prop.default

        # Load configuration from command-line
        console_config = vars(self.parser.parse_args())

        # Configure logging
        logging_level = logging.DEBUG if console_config["verbose"] else logging.INFO
        logging.basicConfig(format='%(levelname)s\t| %(message)s', level=logging_level)

        # Load configuration from file
        logging.debug("Load configuration from file")
        if "config_file" in console_config:
            config_file_name = console_config["config_file"]
        else:
            config_file_name = config[GLOBAL_CONFIG]["config_file"]
        config_path = realpath(config_file_name)
        if exists(config_path):
            logging.debug("Load configuration from %s", config_path)
            parser = configparser.ConfigParser()
            parser.read(config_path)
            # Update configuration with file configuration values
            for group, props in self.properties.items():
                for prop in props:
                    if parser.has_option(group, prop.name):
                        config.setdefault(group, {})[prop.name] = parser[group][prop.name]

        # Append/override values from command-line
        logging.debug("Update configuration with command-line arguments")
        for group, props in self.properties.items():
            for prop in props:
                name = prop.name if group == GLOBAL_CONFIG else group + "." + prop.name
                if name in console_config:
                    config.setdefault(group, {})[prop.name] = console_config[name]

        # Check configuration properties
        err_count = 0
        for group, props in self.properties.items():
            for prop in props:
                name = prop.name if group == GLOBAL_CONFIG else group + "." + prop.name
                if prop.mandatory and not config[group][prop.name]:
                    logging.error("Property '%s' is required", name)
                    err_count += 1
                elif not prop.is_valid(config[group][prop.name]):
                    logging.error("Value of property '%s' is invalid", name)
                    err_count += 1
        if err_count > 0:
            logging.error("Configuration is incorrect, fix previous issues and run again")
            raise AppError()

        logging.debug("Configuration: %s", str(config))
        return config
