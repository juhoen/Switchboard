"""Exceptions module"""

class SwitchboardException(Exception):
    """Switchboard base exception"""


class SwitchboardMissingFieldException(SwitchboardException):
    """Missing field exception"""


class SwitchboardCordException(SwitchboardException):
    """Base Cord exception"""


class SwitchboardCordValidationException(SwitchboardCordException):
    """Cord validation exception"""
