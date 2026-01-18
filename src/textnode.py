from enum import Enum

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

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode:
    def __init__(self, block_type, content):
        self.block_type = block_type
        self.content = content

    def __eq__(self, other) -> bool:
        return self.block_type == other.block_type and self.content == other.content

    def __repr__(self) -> str:
        return f"BlockNode({self.block_type}, {self.content}"
