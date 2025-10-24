class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if not self.props:
            return string 
        for key, value in self.props.items():
            string += " "
            string += f'{key}="{value}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        void_tags = {
            "area","base","br","col","embed","hr","img","input",
            "link","meta","param","source","track","wbr"
        }

        # Pure text node (no tag)
        if not self.tag:
            if self.value is None:
                raise ValueError("Leaf text nodes must have a value")
            return self.value

        # Void elements: no inner text and no closing tag
        if self.tag in void_tags:
            return f"<{self.tag}{self.props_to_html()}>"

        # Non-void: require a (possibly empty) value
        if self.value is None:
            raise ValueError("All non-void leaf nodes must have a value")

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Node must have a tag")
        if not self.children:
            raise ValueError("Parent Node must have children")
        else:
            string = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                string += child.to_html()
            string += f"</{self.tag}>"
            return string
