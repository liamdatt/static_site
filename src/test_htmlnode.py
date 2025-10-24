import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
        output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), output)

    def test_no_props(self):
        node = HTMLNode()
        output = ""
        self.assertEqual(node.props_to_html(), output)

    def test_repr(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank",})
        output = f"HTMLNode(None, None, None, {node.props})"
        self.assertEqual(node.__repr__(), output)
            
      



if __name__ == "__main__":
    unittest.main()
