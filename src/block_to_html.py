from htmlnode import HTMLNode, LeafNode, ParentNode
from split_blocks import markdown_to_blocks
from blocktype import BlockType,block_to_block_type
from text_to_textnodes import text_to_textnodes
from text_to_html import text_node_to_html_node
from textnode import TextNode,TextType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_split = block.split(" ", 1)
            count = 0
            for char in heading_split[0]:
                if char == "#":
                    count += 1
            html_nodes.append(LeafNode(f"h{count}", heading_split[1]))
        elif block_type == BlockType.PARAGRAPH:
            text = " ".join(line.strip() for line in block.split("\n"))
            inner_nodes = text_to_children(text)
            html_nodes.append(ParentNode("p",inner_nodes))
        elif block_type ==BlockType.QUOTE:
            line_nodes = []
            line_split = block.split("\n")
            for line in line_split:
                line = line[1:].strip()
                inner_nodes = text_to_children(line)
                line_nodes.extend(inner_nodes)
            html_nodes.append(ParentNode('blockquote',line_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            line_nodes = []
            line_split = block.split("\n")
            for line in line_split:
                line = line[2:]
                inner_nodes = text_to_children(line)
                line_nodes.append(ParentNode("li",inner_nodes))
            html_nodes.append(ParentNode("ul",line_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            line_nodes = []
            line_split = block.split("\n")
            for line in line_split:
                line = line[3:]
                inner_nodes = text_to_children(line)
                line_nodes.append(ParentNode("li",inner_nodes))
            html_nodes.append(ParentNode("ol",line_nodes))
        elif block_type == BlockType.CODE:
            nodes = []
            lines = block.split("\n")[1:-1]
            lines = [line.lstrip() for line in lines]
            text = "\n".join(lines) + "\n"
            text_node = TextNode(text,TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            nodes.append(html_node)
            html_nodes.append(ParentNode("pre",nodes))
    return ParentNode("div",html_nodes)




def text_to_children(text):
    text_nodes = []
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

