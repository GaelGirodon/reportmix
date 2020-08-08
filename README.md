# ReportMix

[![PyPI](https://img.shields.io/pypi/v/reportmix?style=flat-square)](https://pypi.org/project/reportmix/)
[![License](https://img.shields.io/github/license/GaelGirodon/reportmix?color=informational&style=flat-square)](https://github.com/GaelGirodon/reportmix/blob/master/LICENSE)
[![Python version](https://img.shields.io/pypi/pyversions/reportmix?style=flat-square)](https://pypi.org/project/reportmix/)
[![Build](https://img.shields.io/azure-devops/build/gaelgirodon/reportmix/10?style=flat-square)](https://dev.azure.com/gaelgirodon/reportmix)
[![Tests](https://img.shields.io/azure-devops/tests/gaelgirodon/reportmix/10?style=flat-square)](https://dev.azure.com/gaelgirodon/reportmix)
[![Pylint](https://img.shields.io/badge/pylint-9.45-success?style=flat-square)](tasks.yml#L28)

Merge reports from [multiple tools](#supported-reports) into a single file.

## Install

Install **ReportMix** from [PyPI](https://pypi.org/project/reportmix/):

```shell
pip install reportmix
```

## Usage

Merge reports using the command-line interface:

```shell
reportmix
```

### Arguments

| Argument                    | Description                                                    |
| --------------------------- | -------------------------------------------------------------- |
| `-h`, `--help`              | Show the help message and exit                                 |
| `-V`, `--version`           | Show program's version number and exit                         |
| `-v`, `--verbose`           | Run verbosely (display `DEBUG` logging)                        |
| `--output_dir OUTPUT_DIR`   | The location to write the report                               |
| `--config_file CONFIG_FILE` | The path to the configuration file                             |
| `--formats FORMATS`         | Report formats to be generated (`csv`, `json`, `html`)         |
| `--fields FIELDS`           | Fields to include in the output report (CSV and HTML only)     |
| `--hash HASH`               | Fields to use for hash generation                              |
| `--title TITLE`             | The HTML report title                                          |
| `--logo LOGO`               | The URL to the organization logo to display on the HTML report |
| `--meta.*`                  | User-defined metadata fields                                   |

Run `reportmix --help` to show the full help message.

Some properties (`formats`, `fields`, `hash`, ...) support a single value
or a comma-separated list of items (e.g. `--formats "csv,html,json"`).

Tool-specific configuration arguments are documented in the help message
and [below](#supported-reports).

## Configuration

Configure the merging process using **command-line arguments**
or create a **configuration file** `.reportmix` in the working directory:

```ini
[global]
output_dir=target
formats=html,csv,json
fields=tool_name,tool_version,meta_organization,name,description,type,severity,subject_name
title=Analysis report
logo=http://acme.com/img/logo.png

[meta]
organization=Acme Corporation

[dependency_check]
report_file=target/dependency-check-report.csv

[npm_audit]
report_file=web-app/npm-audit.json

[sonarqube]
host_url=http://sonarqube.acme.corp
project_key=acme:myproject

[reportmix]
report_file=sub-project/reportmix.csv
```

This configuration can also be passed as **command-line arguments**:

```shell
reportmix --output_dir target --formats "html,csv,json" \
    --fields [...] --title "Analysis report" --logo "http://acme.com/img/logo.png" \
    --meta.organization "Acme Corporation" \
    --dependency_check.report_file "target/dependency-check-report.csv" \
    --npm_audit.report_file "web-app/npm-audit.json" \
    --sonarqube.host_url "http://sonarqube.acme.corp" --sonarqube.project_key "acme:myproject" \
    --reportmix.report_file "sub-project/reportmix.csv"
```

### Metadata fields

Metadata fields allow to define some fields for each issue in the configuration:

| Name           | Description           | Default value |
| -------------- | --------------------- | ------------- |
| `product`      | The product name      |               |
| `version`      | The product version   |               |
| `organization` | The organization name |               |
| `client`       | The client name       |               |
| `audit_date`   | The audit date        | _`now()`_     |

### Hash

`hash` is a special field. It is not extracted from the reports data but
computed using some of the issue fields to create a stable unique identifier.
If multiple issues, in a single merged report or in different reports,
generated at different times, have the same `hash` value, we can consider
they are the same, so solving one of them will solve the others. It can be
especially useful for computing a delta between multiple reports, tracking
issues fixes, etc.

## Supported reports

Reports produced by the following tools are currently supported:

- [**Dependency-Check**](#dependency-check-loader):
  load a vulnerability report generated by OWASP dependency check
  (CSV required, JSON optional), version 5.x is recommended
- [**npm audit**](#npm-audit-loader):
  load a security audit generated by npm-audit CLI command
  (JSON format only), npm@6 is required
- [**SonarQube**](#sonarqube-loader):
  load code quality analysis results from a SonarQube instance,
  version 7.x is required
- [**ReportMix**](#reportmix-loader):
  load a report (CSV format) generated by ReportMix or manually created

> Contributions to improve existing [report loaders](reportmix/loaders)
> or add new ones are welcome!

### Dependency-Check loader

- **Run** a Dependency-Check scan (cf. [Maven plugin](https://jeremylong.github.io/DependencyCheck/dependency-check-maven/))
  - The `CSV` report is required, the `JSON` report is optional
    (cf. `format` property in the plugin configuration)
- **Move** `dependency-check-report.*` files in the working directory
  or **configure** ReportMix (`dependency_check.report_file`) to look for the file somewhere else
- :heavy_check_mark: **Run ReportMix**

> → [Dependency-Check loader](reportmix/loaders/dependency_check.py)

### npm audit loader

- **Run** a security audit using the [npm-audit](https://docs.npmjs.com/cli/audit) CLI command
  - Get the detailed audit report in JSON format, e.g.: `npm audit --json > npm-audit.json`
- **Move** the `npm-audit.json` file in the working directory
  or **configure** ReportMix (`npm_audit.report_file`) to look for the file somewhere else
- :heavy_check_mark: **Run ReportMix**

> → [npm audit loader](reportmix/loaders/npm_audit.py)

### SonarQube loader

- **Run** a SonarQube analysis (cf. [Analyzing Source Code](https://docs.sonarqube.org/latest/analysis/overview/))
- **Configure** the instance URL (`sonarqube.host_url`), the project key (`sonarqube.project_key`),
  and [authentication](https://docs.sonarqube.org/latest/extend/web-api/) settings
- :heavy_check_mark: **Run ReportMix**

> → [SonarQube loader](reportmix/loaders/sonarqube.py)

### ReportMix loader

- **Run** ReportMix (e.g. in another project) to generate a report (`csv` format
  required) or **create it manually** using the ReportMix output format (e.g. to
  include vulnerabilities from a manual security audit). A spreadsheet can be
  used to easily create or edit a CSV report.
- **Configure** the path to the CSV report file (`reportmix.report_file`)
- :heavy_check_mark: **Run ReportMix**

> → [ReportMix loader](reportmix/loaders/reportmix.py)

## License

**ReportMix** is licensed under the GNU General Public License.
