# To-Do

- [ ] Improve loaders
  - [ ] Support more tools / report formats (Checkmarx, ...)
  - [ ] Improve existing loaders (mapping)
  - [ ] Allow to enable only some tools (`--tools "dependency_check,sonarqube"`)
  - [ ] Dependency Check:
    - [ ] Use JSON report only (instead of CSV)
  - [ ] SonarQube:
    - [ ] Load rules and get security hotspots severity from them
    - [ ] Default `project_key` to `<groupId>:<artifactId>` for Maven projects
- [ ] Improve export formats
  - [ ] Add field names customization
  - [ ] Add a header with a summary table in the HTML report
  - [ ] Improve metadata fields
- [ ] Improve configuration and CLI
- [ ] Improve documentation and testing
- [ ] Release and publish to PyPI
