# TODO

- [ ] Improve loaders
  - [ ] Support more tools / report formats (Checkmarx, ...)
  - [ ] Improve existing loaders (mapping)
  - [ ] Allow to enable only some tools (`--tools "dependency_check,sonarqube"`)
  - [ ] Dependency Check:
    - [ ] Use JSON report instead of CSV
  - [ ] SonarQube:
    - [ ] Improve API call (page size, etc.)
    - [ ] Default `project_key` to `<groupId>:<artifactId>` for Maven projects
- [ ] Improve export formats
   - [ ] Allow exporting to multiple formats at once (`--format "csv,html,json"`)
   - [ ] Allow to override the value of some fields (e.g. `version`, `application`, ...)
   - [ ] Add a header with a summary table in the HTML report
- [ ] Improve configuration and CLI
  - [ ] Validate properties (required, format, etc.)
- [ ] Improve documentation and testing
- [ ] Release and publish to PyPI
