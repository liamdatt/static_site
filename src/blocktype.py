from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):

    if not block.strip():
        return BlockType.PARAGRAPH
    heading_prefix= block.split(" ")
    if all(char == "#" for char in heading_prefix[0]) and len(heading_prefix[0]) <= 6:
        return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{num+1}. ") for num, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
        

