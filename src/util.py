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
