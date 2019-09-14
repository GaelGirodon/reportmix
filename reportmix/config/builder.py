import argparse
import configparser
import logging
import re
from os.path import exists, realpath
from typing import Union, Dict

from reportmix.config.property import ConfigProperty
from reportmix.errors import AppError
from reportmix.loaders import dependency_check, sonarqube, npm_audit

# Configuration global group name (for global configuration properties)
GLOBAL_CONFIG = "global"


class ConfigBuilder:
    """
    Build the configuration from the configuration file and command-line arguments.
    """

    def __init__(self):
        # Configuration properties
        self.properties = {
            GLOBAL_CONFIG: [
                ConfigProperty("output_dir", "the location to write the report", True, "./"),
                ConfigProperty("config_file", "the path to the configuration file", True, ".reportmix"),
                ConfigProperty("formats", "Report formats to be generated (csv, html, json)", True, "html",
                               "^((F),)*(F)$".replace("F", "csv|html|json")),
                ConfigProperty("fields", "fields to include in the output report (CSV and HTML only)", True, "all",
                               "^((\\w+),)*(\\w+)$"),
                ConfigProperty("logo", "the URL to the company logo to display on the HTML report", False)
            ],
            "dependency_check": dependency_check.properties,
            "npm_audit": npm_audit.properties,
            "sonarqube": sonarqube.properties
        }

        # Initialize the command-line argument parser
        self.parser = argparse.ArgumentParser(description='Merge reports from multiple tools into one single file.')
        self.parser.add_argument("-v", "--verbose", action="store_true", help="run verbosely (display DEBUG logging)")

        for group, props in self.properties.items():
            for p in props:
                name = "--" + p.name if group == GLOBAL_CONFIG else "--" + group + "." + p.name
                description = p.description if not p.default else "%s (default: %s)" % (p.description, p.default)
                self.parser.add_argument(name, type=str, metavar=p.name.upper(),
                                         default=argparse.SUPPRESS, help=description)

    def build(self) -> Dict[str, Union[str, Dict[str, str]]]:
        # Build default configuration
        config = {}
        for group, props in self.properties.items():
            for p in props:
                config.setdefault(group, {})[p.name] = p.default

        # Load configuration from command-line
        console_config = vars(self.parser.parse_args())

        # Configure logging
        logging_level = logging.DEBUG if console_config["verbose"] else logging.INFO
        logging.basicConfig(format='%(levelname)s\t| %(message)s', level=logging_level)

        # Load configuration from file
        logging.debug("Load configuration from file")
        config_file_name = console_config["config_file"] if "config_file" in console_config else config[GLOBAL_CONFIG][
            "config_file"]
        config_path = realpath(config_file_name)
        if exists(config_path):
            logging.debug("Load configuration from %s", config_path)
            cp = configparser.ConfigParser()
            cp.read(config_path)
            # Update configuration with file configuration values
            for group, props in self.properties.items():
                for p in props:
                    if cp.has_option(group, p.name):
                        config.setdefault(group, {})[p.name] = cp[group][p.name]

        # Append/override values from command-line
        logging.debug("Update configuration with command-line arguments")
        for group, props in self.properties.items():
            for p in props:
                name = p.name if group == GLOBAL_CONFIG else group + "." + p.name
                if name in console_config:
                    config.setdefault(group, {})[p.name] = console_config[name]

        # Check configuration properties
        err_count = 0
        for group, props in self.properties.items():
            for p in props:
                name = p.name if group == GLOBAL_CONFIG else group + "." + p.name
                if p.mandatory and not config[group][p.name]:
                    logging.error("Property '%s' is required", name)
                    err_count += 1
                elif p.pattern and not re.match(p.pattern, config[group][p.name]):
                    logging.error("Value of property '%s' is invalid", name)
                    err_count += 1
        if err_count > 0:
            logging.error("Configuration is incorrect, fix previous issues and run ReportMix again")
            raise AppError()

        logging.debug("Configuration: %s", str(config))
        return config
