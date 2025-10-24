import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_urldefault(self):
        node = TextNode("This is a test node", TextType.TEXT)
        self.assertEqual(node.url, None)

    def test_equrl(self):
        node = TextNode("some alt text", TextType.LINK)
        node2 = TextNode("some alt text", TextType.LINK, "https://floproja.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
