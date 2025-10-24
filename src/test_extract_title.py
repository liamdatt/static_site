import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_h1_with_spaces(self):
        markdown = "   #   My Title   "
        self.assertEqual(extract_title(markdown), "My Title")

    def test_no_header_raises(self):
        markdown = "This file has no headers."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_only_h2_should_fail(self):
        markdown = "## Subheading"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_multiple_lines_first_header_used(self):
        markdown = "Some intro\n# First Title\n## Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    def test_header_with_extra_hashes_but_space(self):
        markdown = "# Hashes in text ## not heading"
        self.assertEqual(extract_title(markdown), "Hashes in text ## not heading")

    def test_hash_no_space_not_valid(self):
        markdown = "#Title"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
