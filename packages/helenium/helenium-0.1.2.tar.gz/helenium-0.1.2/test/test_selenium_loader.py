import platform

import pytest

from src.selenium_loader import SeleniumLoader


@pytest.mark.parametrize(
    "os,machine,zip_filename,driver_filename",
    [
        ("Linux", None, "chromedriver_linux64.zip", "chromedriver"),
        ("Darwin", "x86_64", "chromedriver_mac64.zip", "chromedriver"),
        ("Darwin", "arm64", "chromedriver_mac64_m1.zip", "chromedriver"),
        ("Windows", None, "chromedriver_win32.zip", "chromedriver.exe"),
    ],
)
def test_get_driver_path(mocker, os, machine, zip_filename, driver_filename):
    mocker.patch.object(SeleniumLoader, "__init__", return_value=None)
    selenium_loader = SeleniumLoader()
    mocker.patch.object(platform, "system", return_value=os)
    mocker.patch.object(platform, "machine", return_value=machine)
    selenium_loader._get_driver_path()

    assert selenium_loader.zip_filename == zip_filename
    assert selenium_loader.driver_filename == driver_filename
