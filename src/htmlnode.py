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