from wires import BaseWire
from exceptions import SwitchboardMissingFieldException
from diggable import Diggable

EXCLUDE = 0
INCLUDE = 1
RAISE = 2


class Switchboard:
    OPTIONS_CLASS = "Meta"
    _options = None

    def __init__(self):
        self._options = {"missing": INCLUDE, **self._get_options()}

    def _get_options(self):
        _options = {}
        _meta = getattr(self, self.OPTIONS_CLASS)

        for attr_name in dir(_meta):
            if not attr_name.startswith("__"):
                _options[attr_name] = getattr(_meta, attr_name)

        return _options

    def _get_wires(self):
        _wires = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, BaseWire):
                _wires[attr_name] = attr
        return _wires

    def apply(self, data):
        new_data = {}
        diggable = Diggable(data)

        for wire_name, wire_inst in self._get_wires().items():
            value, is_found = wire_inst.dig(diggable)

            if not is_found and self._options["missing"] is EXCLUDE:
                continue

            if not is_found and self._options["missing"] is RAISE:
                raise SwitchboardMissingFieldException(
                    f'Field "{wire_name}" is missing'
                )

            new_data[wire_name] = value

        return new_data
