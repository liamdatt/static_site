from textnode import TextType, TextNode
from extract_images_links import extract_markdown_images,extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
            continue
        if delimiter not in node.text:
            node_list.append(node)
            continue
        
        split_parts = node.text.split(delimiter)
        for i, part in enumerate(split_parts):
            if part == "":
                continue
            if i%2 == 0:
                node_list.append(TextNode(part, TextType.TEXT))
            else:
                node_list.append(TextNode(part, text_type))
    return node_list
            
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        image = extract_markdown_images(node.text)
        if len(image) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for alt, url in image:
            markdown = f"![{alt}]({url})"
            parts = text.split(markdown,1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0],TextType.TEXT))
            new_nodes.append(TextNode(alt,TextType.IMAGE,url))
            text = parts[1] if len(parts) > 1 else ""
        if text:
            new_nodes.append(TextNode(text,TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        text = node.text
        for anchor,url in links:
            markdown = f"[{anchor}]({url})"
            parts = text.split(markdown,1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor,TextType.LINK,url))
            text = parts[1] if len(parts) > 1 else ""
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
