import unittest
from blocktype import BlockType,block_to_block_type

class test_block_to_block_type(unittest.TestCase):
    def test_h1_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_h6_heading(self):
        block = "###### Level 6 Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_too_many_hashes(self):
        block = "####### Invalid Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_missing_space_after_hashes(self):
        block = "###Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_with_leading_spaces(self):
        block = "   ### Spaced heading"
        self.assertEqual(block_to_block_type(block.strip()), BlockType.HEADING)

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_inline_backticks(self):
        block = "`inline code`"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unclosed_code_block(self):
        block = "```\nprint('oops')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multiple_lines(self):
        block = "> line 1\n> line 2\n> line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_mixed_quote_invalid(self):
        block = "> valid\nnot valid"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_basic(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed_invalid(self):
        block = "- item 1\n* item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_with_extra_space(self):
        block = "-  double space"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_valid(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_not_starting_at_one(self):
        block = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_out_of_order(self):
        block = "1. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        block = "1. only one"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    
    def test_plain_paragraph(self):
        block = "This is a plain paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        block = "This is line one.\nThis is line two."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_string(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()
