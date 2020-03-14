# Generate Allure report docker action
This action generates [Allure](http://allure.qatools.ru/) report.

## Inputs

### `data-location`

**Required** location of the Allure data. This path must be relative to the one from GITHUB_WORKSPACE variable.

### `report-location`

**Required** location where generated Allure report will be stored. This path must be relative to the one from GITHUB_WORKSPACE variable. The folder won't be cleared before the generation.

### `allure-location`

Optional location (URL) to download zip archive for Allure commandline. Please, use download links from [Allure releases](https://github.com/allure-framework/allure2/releases).

## Example usage

Given a step to generate allure data

```
name: Execute test cases
run: py.test tests --alluredir allure/data --clean-alluredir
```

One can use allure directory (allure/data in this case) to generate a report

```
name: Build allure report
if: always()
uses: KillAChicken/generate-allure-report@v1
with:
    data-location: allure/data
    report-location: allure/report
```

See workflows of this repository for more examples.
