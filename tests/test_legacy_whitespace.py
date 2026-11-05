import json
import unittest

import simplicity


class LegacyWhitespaceTests(unittest.TestCase):
    blank_lines = ("", " ", "    ", "\t", " \t ")

    def parse(self, text):
        with self.assertWarns(DeprecationWarning):
            return json.loads(simplicity.rst_to_json(text))

    def test_blank_line_before_first_field(self):
        for blank in self.blank_lines:
            with self.subTest(blank=repr(blank)):
                text = "Title\n=====\n{}\n:field: value\n".format(blank)
                self.assertEqual(self.parse(text), [{"title": "Title", "field": "value"}])

    def test_blank_line_before_title(self):
        for blank in self.blank_lines:
            with self.subTest(blank=repr(blank)):
                text = "{}\nTitle\n=====\n:field: value\n".format(blank)
                self.assertEqual(self.parse(text), [{"title": "Title", "field": "value"}])

    def test_blank_line_before_field_in_new_section(self):
        for blank in self.blank_lines:
            with self.subTest(blank=repr(blank)):
                text = (
                    "First\n=====\n:field: one\n"
                    "Second\n======\n{}\n:other: two\n"
                ).format(blank)
                self.assertEqual(
                    self.parse(text),
                    [
                        {"title": "First", "field": "one"},
                        {"title": "Second", "other": "two"},
                    ],
                )

    def test_blank_line_preserves_multiline_paragraph_break(self):
        for blank in self.blank_lines:
            with self.subTest(blank=repr(blank)):
                text = "Title\n=====\n:field: first\n{}\n    second\n".format(blank)
                self.assertEqual(
                    self.parse(text), [{"title": "Title", "field": "first\n\nsecond"}]
                )

    def test_blank_line_after_numeric_field(self):
        for blank in self.blank_lines:
            with self.subTest(blank=repr(blank)):
                text = "Title\n=====\n:age: 22\n{}\n:field: value\n".format(blank)
                self.assertEqual(
                    self.parse(text), [{"title": "Title", "age": 22, "field": "value"}]
                )

    def test_directive_content_remains_ignored(self):
        for blank in self.blank_lines:
            with self.subTest(blank=repr(blank)):
                text = (
                    "Title\n=====\n.. image:: image.png\n"
                    "    :target: example.invalid\n{}\n:field: value\n"
                ).format(blank)
                self.assertEqual(self.parse(text), [{"title": "Title", "field": "value"}])

    def test_nonblank_continuation_remains_a_single_line_break(self):
        text = "Title\n=====\n:field: first\n    second\n"
        self.assertEqual(
            self.parse(text), [{"title": "Title", "field": "first\nsecond"}]
        )

    def test_nonblank_numeric_continuation_remains_ignored(self):
        text = "Title\n=====\n:age: 22\n    ignored\n"
        self.assertEqual(self.parse(text), [{"title": "Title", "age": 22}])


if __name__ == "__main__":
    unittest.main()
