class SwitchboardException(Exception):
    pass


class SwitchboardMissingFieldException(SwitchboardException):
    pass


class SwitchboardWireException(SwitchboardException):
    pass


class SwitchboardWireValidationException(SwitchboardWireException):
    pass
