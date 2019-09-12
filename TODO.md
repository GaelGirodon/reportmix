# TODO

- [ ] Improve loaders
  - [ ] Support more tools / report formats
  - [ ] Improve existing loaders (mapping)
  - [ ] Allow to enable only some tools (`--tools "dependency_check,sonarqube"`)
  - [ ] Dependency Check:
    - [ ] Use JSON report instead of CSV
  - [ ] SonarQube:
    - [ ] Default `project_key` to `<groupId>:<artifactId>` for Maven projects
    - [ ] Improve API call (page size, etc.)
- [ ] Improve export formats
- [ ] Improve configuration and CLI
  - [ ] Validate properties (required, format, etc.)
- [ ] Improve documentation and testing
- [ ] Release and publish to PyPI
