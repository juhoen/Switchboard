"""Diggable main module"""
import json


class DiggableFieldNotFoundException(Exception):
    """Field not found exception"""


class Diggable:
    """Diggable object. Wrapping dictionaries and JSON objects inside
    Diggable objects makes then queryable"""

    def __init__(self, diggable):
        self.diggable = diggable
        self._errors = []

    @staticmethod
    def _get_path_string(path):
        return json.dumps(path)

    @classmethod
    def _query_dict(cls, key, query, path):
        path_name = cls._get_path_string(path)

        def _query(_diggable):
            try:
                return query(_diggable)[key]
            except (KeyError, IndexError):
                raise DiggableFieldNotFoundException(
                    "Diggable object has no path %s" % path_name
                )

        return _query

    @classmethod
    def build_query(cls, keys):
        """Method build a query that can be applied to any
        json object (dict/list or combination of them)"""
        query = lambda diggable: diggable
        query_path = []

        for key in keys:
            query_path.append(key)
            query = cls._query_dict(key, query, query_path)

        return query

    def dig(self, *keys):
        """Query method"""

        query = self.build_query(keys)
        return query(self.diggable)
