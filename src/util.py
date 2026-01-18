import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
    tag = None
    value = text_node.text
    props = {}
    match text_node.text_type:
        case TextType.PLAIN:
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
