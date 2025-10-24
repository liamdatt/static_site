import unittest
from split_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_basic_split(self):
        markdown = "# Heading\n\nThis is a paragraph."
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["# Heading", "This is a paragraph."])

    def test_trailing_newlines(self):
        markdown = "# Heading\n\nParagraph\n\n\n\n"
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["# Heading", "Paragraph"])

    def test_multiple_blocks(self):
        markdown = "# Title\n\npara 1\n\n- item 1\n- item 2"
        result = markdown_to_blocks(markdown)
        expected = ["# Title", "para 1", "- item 1\n- item 2"]
        self.assertEqual(result, expected)

    def test_whitespace(self):
        markdown = "   # Title   \n\n   paragraph with spaces   "
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, ["# Title", "paragraph with spaces"])

    def test_empty_input(self):
        markdown = ""
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, [])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()
