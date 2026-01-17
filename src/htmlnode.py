

class HtmlNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: str = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def props_to_html(self) -> str:
        props = ""
        if self.props:
            for key, value in self.props.items():
                props += f" {key}={value}"
        return props

    def to_html(self) -> str:
        raise NotImplementedError("method not implemented for this html node")

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children=[{self.children}], props=[{self.props_to_html()}])"


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
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, props=[{self.props_to_html()}])"


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: dict = None
    ):
        super().__init__(
            tag = tag,
            children = children,
            props = props
        )

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag must exist for a parent node")
        if self.children is None:
            raise ValueError("Parent node must have children")
        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += f"{child.to_html()}"
        html += f"</{self.tag}>"
        return html

