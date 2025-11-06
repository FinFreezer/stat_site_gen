class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method unfinished")

    def props_to_html(self):
        if self.props is None:
            return ""
            
        end_str = ""
        keys = self.props.keys()

        for key in keys:
            end_str += f" {key}=\"{self.props[key]}\""
        return end_str
    
    def __repr__(self):
        props_str = self.props_to_html()
        return f"Node attributes are: tag: {self.tag}, value: {self.value}, children: {self.children}, props: {props_str}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf must include a value.")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        full_html = f"<{self.tag}>"
        if self.tag == None:
            raise ValueError("Tag required.")
        if self.children == None:
            raise ValueError("Child nodes required.")
        for child in self.children:
            full_html += child.to_html()
        return full_html + f"</{self.tag}>"