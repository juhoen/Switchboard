"""Switchboard module"""
# pylint: disable=too-few-public-methods
from .cords import Cord
from .diggable import Diggable
from .exceptions import SwitchboardMissingFieldException


class Switchboard:
    """Switchboard objects helps converting JSON schemas.
    Switchboard consists of cords that can define how data
    list moved from schema to schema.
    """

    OPTIONS_CLASS = "Meta"

    # Missing data options
    EXCLUDE = "EXCLUDE"
    INCLUDE = "INCLUDE"
    RAISE = "RAISE"

    # Attributes
    _options = None
    _many = None

    def __init__(self, many=False):
        self._many = many
        self._options = {"missing": self.INCLUDE, **self._get_options()}

    def _get_options(self):
        _options = {}
        _meta = getattr(self, self.OPTIONS_CLASS, None)

        for attr_name in dir(_meta):
            if not attr_name.startswith("__"):
                _options[attr_name] = getattr(_meta, attr_name)

        return _options

    def _get_cords(self):
        _cords = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Cord):
                _cords[attr_name] = attr
        return _cords

    def _apply_for_object(self, data):
        new_data = {}
        diggable = Diggable(data)

        for cord_name, cord_inst in self._get_cords().items():
            value, is_found = cord_inst.apply(diggable)

            if not is_found and self._options["missing"] is self.EXCLUDE:
                continue

            if not is_found and self._options["missing"] is self.RAISE:
                raise SwitchboardMissingFieldException(
                    f'Field "{cord_name}" is missing'
                )

            new_data[cord_name] = value

        return new_data

    def apply(self, data):
        """Switchboard is applied via this method.
        """

        if self._many:
            return list(map(self._apply_for_object, data))

        return self._apply_for_object(data)
