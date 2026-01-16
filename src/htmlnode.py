class Tag:
    def __init__(self, tag):
        self.tag = tag
    
    def to_html(self, close = False, **kwargs) -> str:
        if self.tag:
            tag += "<"
            if close:
                tag += "/"
            tag += self.tag
        for key, value in kwargs.item():
            tag += f"{key}={value}"
        if self.tag:
            tag += ">"
        return tag


class HtmlNode:
    def __init__(
        self,
        tag: Tag = None,
        value: str = None,
        children: str = None,
        props: str = None,
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
        return f"{self.tag.to_html(self.props)}\n{self.value}\n{self.children}\n{self.tag.to_html(close = True)}"

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children=[{self.children}], props=[{self.__props_to_html()])"
