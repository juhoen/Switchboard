# pylint: disable=all
import unittest

from switchboard import Cord, Switchboard, SwitchboardMissingFieldException


class TestSwitchboard(unittest.TestCase):
    def test_one_level(self):
        class TestSwitchboard(Switchboard):
            new = Cord(source="old")

        old = {"old": 1}
        sb = TestSwitchboard()
        new = sb.apply(old)

        self.assertNotEqual(old, new)
        self.assertEqual(old["old"], 1)
        self.assertEqual(new["new"], 1)

    def test_two_levels(self):
        class TestSwitchboard(Switchboard):
            new = Cord(source=["old", "location"])

        old = {"old": {"location": "test"}}
        sb = TestSwitchboard()
        new = sb.apply(old)

        self.assertNotEqual(old, new)
        self.assertEqual(old["old"]["location"], "test")
        self.assertEqual(new["new"], "test")

    def test_nested_list(self):
        class TestSwitchboard(Switchboard):
            name = Cord(source=["pets", 0, "pet_name"])

        old = {"pets": [{"pet_name": "Fluffy"}]}
        sb = TestSwitchboard()
        new = sb.apply(old)

        self.assertNotEqual(old, new)
        self.assertEqual(old["pets"][0]["pet_name"], "Fluffy")
        self.assertEqual(new["name"], "Fluffy")

    def test_missing_include(self):
        class TestSwitchboard(Switchboard):
            class Meta:
                missing = Switchboard.INCLUDE

            name = Cord("pet_name")

        old = {}
        sb = TestSwitchboard()
        new = sb.apply(old)

        self.assertEqual(new["name"], None)

    def test_missing_exclude(self):
        class TestSwitchboard(Switchboard):
            class Meta:
                missing = Switchboard.EXCLUDE

            name = Cord("pet_name")

        old = {}
        sb = TestSwitchboard()
        new = sb.apply(old)

        self.assertTrue("name" not in new)

    def test_missing_raise(self):
        class TestSwitchboard(Switchboard):
            class Meta:
                missing = Switchboard.RAISE

            name = Cord("pet_name")

        with self.assertRaises(SwitchboardMissingFieldException):
            sb = TestSwitchboard()
            sb.apply({})
