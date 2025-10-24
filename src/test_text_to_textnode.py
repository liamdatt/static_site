import unittest
from text_to_textnodes import text_to_textnodes
from textnode import TextType, TextNode

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes_basic(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        result = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(result, expected)

    def test_text_to_textnodes_no_formatting(self):
        text = "This is plain text."
        result = text_to_textnodes(text)
        expected = [TextNode("This is plain text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_only_bold(self):
        text = "**bold only**"
        result = text_to_textnodes(text)
        expected = [TextNode("bold only", TextType.BOLD)]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
