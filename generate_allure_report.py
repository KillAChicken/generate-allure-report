"""Module to build allure report."""

import os
import os.path
import stat
import glob
import tempfile
import logging
import argparse
import zipfile
import json
from urllib.request import urlopen, urlretrieve
import subprocess


ALLURE_COMMANDLINE_RELEASES_URL = (
    "https://api.github.com/repos/allure-framework/allure2/releases/latest"
)


def get_allure_location():
    """Get location of the latest allure commandline.

    :returns: URL for zip archive with the latest version of allure commandline.
    """
    logger = logging.getLogger(__name__)

    logger.debug("Try to get the latest release version from '%s'", ALLURE_COMMANDLINE_RELEASES_URL)
    response = urlopen("https://api.github.com/repos/allure-framework/allure2/releases/latest")
    encoding = response.info().get_param("charset", "utf-8")
    response_json = json.loads(response.read().decode(encoding))
    version = response_json["tag_name"]
    logger.debug("Got the version '%s'", version)

    location = "https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/{version}/allure-commandline-{version}.zip".format(version=version)
    logger.info("Created allure location is '%s'", location)

    return location


def download_allure_commandline(url):
    """Download allure commandline.

    :param url: URL of zip archive with allure commandline.
    :returns: path to the allure executable.
    """
    logger = logging.getLogger(__name__)

    logger.debug("Try to download allure commandline from '%s'", url)
    allure_directory = tempfile.mkdtemp()
    archive_path = os.path.join(allure_directory, "archive.zip")
    urlretrieve(url, archive_path)
    logger.debug("Downloaded archive to '%s'", archive_path)

    unzipped_directory = os.path.join(allure_directory, "unzipped")
    logger.debug("Try to unzip allure archive to '%s'", unzipped_directory)
    with zipfile.ZipFile(archive_path, "r") as archive_file:
        archive_file.extractall(unzipped_directory)
    logger.debug("Unzipped archive to '%s'", unzipped_directory)

    glob_pattern = os.path.join(unzipped_directory, "allure-*", "bin", "allure")
    logger.debug("Try to find allure binary with glob pattern '%s'", glob_pattern)
    allure_commandline = glob.glob(glob_pattern)[0]
    logger.info("Found allure binary '%s'", allure_commandline)

    return allure_commandline


def _configure_logging():
    """Configure loggers."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)


def _parse_arguments():
    """Parse commandline arguments.

    :returns: argparse.Namespace with arguments.
    """
    parser = argparse.ArgumentParser(description="Generate allure report.")
    parser.add_argument(
        "--data-location", dest="data_location", default="data",
        help="Location of the allure data",
    )
    parser.add_argument(
        "--report-location", dest="report_location", default="report",
        help="Location where report should be stored",
    )
    parser.add_argument(
        "--allure-location", dest="allure_location",
        help=" ".join((
            "Location where allure commandline can be found.",
            "Zip archive of the latest release will be used if empty string is specified",
        )),
    )
    return parser.parse_args()


def _run():
    """Entrypoint for a script."""
    _configure_logging()
    arguments = _parse_arguments()

    allure_location = arguments.allure_location
    if not allure_location:
        allure_location = get_allure_location()

    allure_executable = download_allure_commandline(allure_location)

    current_mode = os.stat(allure_executable).st_mode
    os.chmod(allure_executable, current_mode | stat.S_IEXEC)

    command = "{allure} generate -o {report_location} {data_location}".format(
        allure=allure_executable,
        report_location=arguments.report_location,
        data_location=arguments.data_location,
    )
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    _run()
