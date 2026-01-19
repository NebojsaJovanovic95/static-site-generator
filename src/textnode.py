from enum import Enum
import re

from htmlnode import ParentNode, LeafNode


class TextType(Enum):
    PLAIN = "plain"
    TEXT = "TEXT"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: str = None
    ):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html(self):
        tag = None
        value = self.text
        props = {}
        match self.text_type:
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
                    "src": self.url,
                    "alt": self.text
                }
            case _:
                raise ValueError("text_node type not supported")
        return LeafNode(tag=tag, value=value, props=props)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    LIST_ITEM = "list_item"

headings = {
    "#": "h1",
    "##": "h2",
    "###": "h3",
    "####": "h4",
    "#####": "h5",
    "######": "h6",
}
block_type_to_tag = {
    "paragraph": "p",
    "code": "code",
    "quote": "quote",
    "list_item": "li",
}

class BlockNode:
    def __init__(self, block_type, content):
        self.block_type = block_type
        if self.block_type == BlockType.CODE:
            self.content = [TextNode(content[4:-3], TextType.CODE)]
        elif self.block_type in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
            self.conent = [BlockNode(BlockType.LIST_ITEM, list_item.split(" ", 1)[1]) for list_item in content.split("\n")]
        else:
            self.content = self.text_to_textnodes(content)

    def __eq__(self, other) -> bool:
        return self.block_type == other.block_type and self.content == other.content

    def __repr__(self) -> str:
        return f"BlockNode({self.block_type}, {self.content}"

    def to_html(self):
        if self.block_type == BlockType.HEADING:
            heading = headings[self.content.split(" ", 1)[0]]
            return ParentNode(heading, [item.to_html() in self.content])
        elif self.block_type == BlockType.UNORDERED_LIST:
            return ParentNode("ul", [item.to_html() in self.content])
        elif self.block_type == BlockType.ORDERED_LIST:
            return ParentNode("ol", [item.to_html() in self.content])
        elif self.block_type == BlockType.CODE:
            return self.content[0].to_html()
        else:
            return ParentNode(block_type_to_tag[self.block_type.value], [item.to_html() for item in self.content])

    def text_to_textnodes(self, text):
        text = text.rstrip("\n")
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
