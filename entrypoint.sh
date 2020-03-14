#!/bin/sh -l

python /generate_allure_report.py --data-location "$GITHUB_WORKSPACE/$1" --report-location "$GITHUB_WORKSPACE/$2" --allure-location "$3"
