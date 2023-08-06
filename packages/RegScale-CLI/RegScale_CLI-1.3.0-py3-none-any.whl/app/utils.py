#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
import os
import re
from datetime import datetime

from app.application import Application
from app.login import is_licensed
from exceptions.license_exception import LicenseException


def check_license():
    """Check RegScale License

    Raises:
        LicenseException: Custom Exception

    Returns:
        Application: application instance
    """
    app = Application()
    if not is_licensed(app):
        raise LicenseException(
            "This feature is limited to RegScale Enterprise, please check RegScale license."
        )
    return app


def validate_mac_address(mac_address: str) -> bool:
    """Simple validation of a mac address input

    Args:
        mac_address (str): mac address

    """
    if re.match(
        "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()
    ):
        return True
    return False


def str_to_date(date_str: str) -> datetime:
    """
    function to convert string into a date object
    """
    # replace the T with a space and create list of result
    date_str = date_str.replace("T", " ").split(" ")

    # convert the first part of the date list into a date
    date = datetime.strptime(date_str[0], "%Y-%m-%d")

    # return date result
    return date


def uncamel_case(camel_str: str) -> str:
    """
    function to convert camelCase strings to Title Case
    """
    # check to see if a string with data was passed
    if camel_str != "":
        # split at any uppercase letters
        result = re.sub("([A-Z])", r" \1", camel_str)

        # use title to Title Case the string
        result = result.title()
        return result
    return ""


def get_css(file_path: str) -> str:
    """
    function to load the css properties from the given file_path
    """
    # create variable to store the string and return
    css = ""

    # check if the filepath exists before trying to open it
    if os.path.exists(file_path):
        # file exists so open the file
        with open(file_path, "r", encoding="utf-8") as file:
            # store the contents of the file in the css str variable
            css = file.read()
    # return the css variable
    return css


def send_email(api, domain: str, payload: dict) -> bool:
    """
    function to use the RegScale email API
    """
    # use the api to post the dict payload passed
    response = api.post(url=f"{domain}/api/email", json=payload)
    # see if api call was successful and return boolean
    return response.status_code == 200


def epoch_to_datetime(epoch: str, format="%Y-%m-%d %H:%M:%S"):
    """Return datetime from unix epoch.

    Args:
        epoch (str): unix epoch
        format (str): datetime string format
    Returns:
        datetime string

    """
    return datetime.fromtimestamp(int(epoch)).strftime(format)


def get_current_datetime(format="%Y-%m-%d %H:%M:%S"):
    """Return current datetime.

    Args:
        format : datetime string format
    Returns:
        datetime string

    """
    return datetime.now().strftime(format)
