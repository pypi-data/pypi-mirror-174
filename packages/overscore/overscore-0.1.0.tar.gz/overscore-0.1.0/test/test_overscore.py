import unittest
import sphinxter.unittest

import overscore


class TestOverscore(sphinxter.unittest.TestCase):

    maxDiff = None

    def test_parse(self):

        self.assertEqual(overscore.parse("1"), [1])
        self.assertEqual(overscore.parse("_1"), [-1])
        self.assertEqual(overscore.parse("__1"), ['1'])
        self.assertEqual(overscore.parse("___1"), ['-1'])
        self.assertEqual(overscore.parse("_order"), ['_order'])
        self.assertEqual(overscore.parse("a__0___1____2_____3"), ["a", 0, -1, "2", "-3"])

        self.assertSphinxter(overscore.parse)

    def test_compile(self):

        self.assertEqual(overscore.compile([1]), "1")
        self.assertEqual(overscore.compile([-1]), "_1")
        self.assertEqual(overscore.compile(['1']), "__1")
        self.assertEqual(overscore.compile(['-1']), "___1")
        self.assertEqual(overscore.compile(['_order']), "_order")
        self.assertEqual(overscore.compile(["a", 0, -1, "2", "-3"]), "a__0___1____2_____3")

        self.assertRaisesRegex(overscore.OverscoreError, "cannot compile -nope", overscore.compile, ['-nope'])

        self.assertSphinxter(overscore.compile)

    def test_get(self):

        self.assertEqual(overscore.get({"things": {"a":{"b": [{"1": "yep"}]}}}, "things__a__b__0____1"), "yep")
        self.assertEqual(overscore.get({}, "things__a__b__0____1"), None)
        self.assertEqual(overscore.get({"things": {"a":{"b": [{"1": "yep"}]}}}, "things__a__b___2"), None)

        self.assertIsNone(overscore.get({"stuff": {"a": []}}, "stuff__a__b"))
        self.assertIsNone(overscore.get({"stuff": {"a": {}}}, "stuff__a__1"))

        self.assertSphinxter(overscore.get)

    def test_set(self):

        values = {}
        overscore.set(values, "things__a__b___2____1", "yep")
        self.assertEqual(values, {"things": {"a":{"b": [{"1": "yep"}, None]}}})

        overscore.set(values, "things__a__b___2____1", "nope")
        self.assertEqual(values, {"things": {"a":{"b": [{"1": "nope"}, None]}}})

        self.assertRaisesRegex(overscore.OverscoreError, "key b invalid for list \[\]", overscore.set, {"stuff": {"a": []}}, "stuff__a__b", "c")
        self.assertRaisesRegex(overscore.OverscoreError, "index 1 invalid for dict \{\}", overscore.set, {"stuff": {"a": {}}}, "stuff__a__1", 2)

        self.assertSphinxter(overscore.set)
