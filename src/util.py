import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
    tag = None
    value = text_node.text
    props = {}
    match text_node.text_type:
        case TextType.PLAIN | TextType.TEXT:
            pass
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props["href"] = text_node.url
        case TextType.IMAGE:
            tag = "img"
            value = ""
            props = {
                "src": text_node.url,
                "alt": text_node.text
            }
        case _:
            raise ValueError("text_node type not supported")
    return LeafNode(tag=tag, value=value, props=props)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        __nodes = node.text.split(delimiter)
        if len(__nodes) % 2 == 0:
            raise ValueError("Markdown syntax error. Delimeter left unclosed")
        for i in range(len(__nodes)):
            if i % 2 == 0:
                if __nodes[i] == "":
                    continue
                new_nodes.append(
                    TextNode(
                        __nodes[i],
                        TextType.PLAIN
                    )
                )
            else:
                new_nodes.append(
                    TextNode(
                        __nodes[i],
                        text_type,
                    )
                )
    return new_nodes

def extract_markdown_images(text):
    regex = r"\!\[([^\]]+)\]\(([^\)]+)\)"
    return re.findall(regex, text)

def extract_markdown_links(text):
    regex = r"\[([^\]]+)\]\(([^\)]+)\)"
    return re.findall(regex, text)

def split_markdown_images(text):
    regex = re.compile(r"\!\[([^\]]+)\]\(([^\)]+)\)")
    results = []
    last = 0
    for m in regex.finditer(text):
        if m.start() > last:
            results.append(("text", text[last:m.start()]))
        results.append( ("image", m.group(1), m.group(2) ) )
        last = m.end()

    if last < len(text):
        results.append(("text", text[last:]))
    return results

def text_to_textnodes(text):
    TOKEN_REGEX = re.compile(
        r"""
        (?P<image>!\[([^\]]+)\]\(([^\)]+)\)) |
        (?P<link>\[([^\]]+)\]\(([^\)]+)\)) |
        (?P<bold>\*\*([^*]+)\*\*) |
        (?P<italic>_([^_]+)_) |
        (?P<code>`([^`]+)`)
        """,
        re.VERBOSE
    )
    tokens = []
    last = 0

    for m in TOKEN_REGEX.finditer(text):
        if m.start() > last:
            tokens.append(
                TextNode(
                    text[last:m.start()],
                    TextType.TEXT,
                )
            )
        kind = m.lastgroup
        if kind == "image":
            tokens.append(TextNode(text = m.group(2), text_type=TextType.IMAGE, url=m.group(3)))

        elif kind == "link":
            tokens.append(TextNode(text=m.group(5), text_type=TextType.LINK, url=m.group(6)))

        elif kind == "bold":
            tokens.append(TextNode(text=m.group(8), text_type=TextType.BOLD))

        elif kind == "italic":
            tokens.append(TextNode(text=m.group(10), text_type=TextType.ITALIC))

        elif kind == "code":
            tokens.append(TextNode(text=m.group(12), text_type=TextType.CODE))

        last = m.end()

    if last < len(text):
        tokens.append(TextNode(text=text[last:], text_type=TextType.TEXT))

    return tokens

def markdown_to_blocks(text):
    return [block.strip() for block in text.split("\n\n")]

def block_to_blocktype(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.split(". ")[0].isdigit():
        return BlockType.ORDERED_LIST
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
