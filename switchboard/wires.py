from exceptions import SwitchboardWireValidationException
from diggable import DiggableFieldNotFoundException

class BaseWire:
    _source = None
    _default = None
    _required = None

    def __init__(self, source, default=None, required=False):
        self._source = source if isinstance(source, list) else [source]
        self._default = default
        self._required = required

    def dig(self, diggable):

        try:
            result = diggable.dig(*self._source)
            return result, True

        except DiggableFieldNotFoundException:

            if self._required:
                raise SwitchboardWireValidationException(
                    f'Required field "{self._source}" is missing'
                )

            return self._default, False


class StreamWire(BaseWire):
    pass
