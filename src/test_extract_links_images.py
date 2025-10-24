import unittest
from extract_images_links import extract_markdown_images,extract_markdown_links


class TestExtractLinksImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_single_image(self):
        text = "Here is an image ![alt text](https://example.com/image.png)"
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text = (
            "Multiple ![one](https://imgur.com/1.png) "
            "and ![two](https://imgur.com/2.png)"
        )
        result = extract_markdown_images(text)
        expected = [
            ("one", "https://imgur.com/1.png"),
            ("two", "https://imgur.com/2.png")
        ]
        self.assertEqual(result, expected)

    def test_single_link(self):
        text = "Check [this site](https://example.com)"
        result = extract_markdown_links(text)
        expected = [("this site", "https://example.com")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text = (
            "Links to [Google](https://google.com) and "
            "[Boot.dev](https://www.boot.dev)"
        )
        result = extract_markdown_links(text)
        expected = [
            ("Google", "https://google.com"),
            ("Boot.dev", "https://www.boot.dev")
        ]
        self.assertEqual(result, expected)

    def test_mixed_links_and_images(self):
        text = (
            "Text with ![alt](https://img.com/x.png) and "
            "[a link](https://link.com)"
        )
        img_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        self.assertEqual(img_result, [("alt", "https://img.com/x.png")])
        self.assertEqual(link_result, [("a link", "https://link.com")])

    def test_no_markdown(self):
        text = "Plain text, no markdown here."
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_malformed_markdown(self):
        text = "Broken ![missing](https://ok.com"
        result = extract_markdown_images(text)
        # Missing closing parenthesis should not match
        self.assertEqual(result, [])

    def test_nested_brackets(self):
        """Should stop at the first closing bracket due to non-greedy (.*?)"""
        text = "![weird [nested] alt](https://example.com/img.png)"
        result = extract_markdown_images(text)
        expected = [("weird [nested] alt", "https://example.com/img.png")]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
