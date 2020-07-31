# pylint: disable=too-few-public-methods
"""Cord module"""

from .diggable import DiggableFieldNotFoundException
from .exceptions import SwitchboardCordValidationException


class Cord:
    """Schema fields can be linked using Cord objects"""

    _source = None
    _default = None
    _required = None

    def __init__(self, source, default=None, required=False):
        self._source = source if isinstance(source, list) else [source]
        self._default = default
        self._required = required

    def apply(self, diggable):
        """Cord is applied via this method.
        """

        try:
            result = diggable.dig(*self._source)
            return result, True

        except DiggableFieldNotFoundException:

            if self._required:
                raise SwitchboardCordValidationException(
                    f'Required field "{self._source}" is missing'
                )

            return self._default, False
