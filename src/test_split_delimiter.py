import unittest
from textnode import TextType,TextNode
from split_delimiter import split_nodes_delimiter,split_nodes_link,split_nodes_image

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_no_delimiter(self):
        """Should return the same node when no delimiter exists."""
        node = TextNode("This has no formatting", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This has no formatting")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_single_delimited_text(self):
        """Should split correctly around one pair of delimiters."""
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_multiple_delimiters(self):
        """Should handle multiple inline formatted segments."""
        node = TextNode("This **one** and **two**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        texts = [n.text for n in new_nodes]
        types = [n.text_type for n in new_nodes]
        self.assertEqual(texts, ["This ", "one", " and ", "two"])
        self.assertEqual(types, [TextType.TEXT, TextType.BOLD, TextType.TEXT, TextType.BOLD])

    def test_mixed_text_and_nontext_nodes(self):
        """Should skip non-text nodes and only split text nodes."""
        text_node = TextNode("Normal *italic* text", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([text_node, bold_node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "Normal ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        # Ensure the bold node was left untouched
        self.assertIn(bold_node, new_nodes)

    def test_empty_segments(self):
        """Should skip empty parts if delimiters are consecutive."""
        node = TextNode("This has ``empty``code blocks``", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # the empty string between double backticks should be ignored
        self.assertTrue(all(n.text != "" for n in new_nodes))

    def test_unmatched_delimiter(self):
        """Should treat everything after the first delimiter as formatted."""
        node = TextNode("This is *broken", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        # no closing delimiter means we get two nodes: before and after
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This has an ![alt text](https://img.com/a.png) inside",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This has an ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt text")
        self.assertEqual(result[1].text_type, TextType.IMAGE)
        self.assertEqual(result[1].url, "https://img.com/a.png")
        self.assertEqual(result[2].text, " inside")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_images(self):
        node = TextNode(
            "Hello ![one](a.png) middle ![two](b.png) end",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        texts = [n.text for n in result]
        types = [n.text_type for n in result]
        urls = [n.url for n in result if n.text_type == TextType.IMAGE]
        self.assertEqual(
            texts,
            ["Hello ", "one", " middle ", "two", " end"]
        )
        self.assertEqual(
            types,
            [TextType.TEXT, TextType.IMAGE, TextType.TEXT, TextType.IMAGE, TextType.TEXT]
        )
        self.assertEqual(
            urls,
            ["a.png", "b.png"]
        )

    def test_no_images(self):
        node = TextNode("No images here", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_skip_non_text_nodes(self):
        img_node = TextNode("alt", TextType.IMAGE, "url.com")
        text_node = TextNode("![alt](url.com)", TextType.TEXT)
        result = split_nodes_image([img_node, text_node])
        self.assertIn(img_node, result)
        self.assertTrue(any(n.text_type == TextType.IMAGE for n in result))


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "Go to [Boot.dev](https://www.boot.dev) now",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Go to ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "Boot.dev")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://www.boot.dev")
        self.assertEqual(result[2].text, " now")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_links(self):
        node = TextNode(
            "Here’s [one](a.com) and [two](b.com) links",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        texts = [n.text for n in result]
        types = [n.text_type for n in result]
        urls = [n.url for n in result if n.text_type == TextType.LINK]
        self.assertEqual(
            texts,
            ["Here’s ", "one", " and ", "two", " links"]
        )
        self.assertEqual(
            types,
            [TextType.TEXT, TextType.LINK, TextType.TEXT, TextType.LINK, TextType.TEXT]
        )
        self.assertEqual(
            urls,
            ["a.com", "b.com"]
        )

    def test_no_links(self):
        node = TextNode("Nothing to link here", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_skip_non_text_nodes(self):
        link_node = TextNode("already link", TextType.LINK, "url.com")
        text_node = TextNode("[Boot.dev](https://www.boot.dev)", TextType.TEXT)
        result = split_nodes_link([link_node, text_node])
        self.assertIn(link_node, result)
        self.assertTrue(any(n.text_type == TextType.LINK for n in result))


if __name__ == "__main__":
    unittest.main()
