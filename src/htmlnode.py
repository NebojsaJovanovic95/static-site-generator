

class HtmlNode:
    def __init__(
        self,
        tag: Tag = None,
        value: str = None,
        children: str = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def __props_to_html(self) -> str:
        props = ""
        for key, value in kwargs.item():
            props += f" {key}={value}"
        return props

    def to_html(self) -> str:
        raise NotImplementedError("method not implemented for this html node")

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children=[{self.children}], props=[{self.__props_to_html()}])"


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict = None
    ):
        super().__init__(
            tag = tag,
            value = value,
            props = props
        )

    def to_html(self):
        if self.value is None:
            raise ValueError("value is None")
        if tag is None:
            return self.value
        return f"<{self.tag}{self.__props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, props=[{self.__props_to_html()}])"



