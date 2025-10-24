from textnode import TextType,TextNode
from htmlnode import HTMLNode,LeafNode,ParentNode

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None,value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b",text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a",text_node.text,{"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img",None,{"src":text_node.url,"alt":text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
