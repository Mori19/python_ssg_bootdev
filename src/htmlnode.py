from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    def __eq__(self, other):
        return all([self.tag == other.tag, self.value == other.value, self.children == other.children, self.props == other.props])


    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None: return ""
        res = [""]
        for key in self.props.keys():
            res.append(f'{key}="{self.props[key]}"')
        return " ".join(res)


class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None: 
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)

    def __repr__(self):
        return f"ParentNode({self.tag},{self.children},{self.props})"


    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent cannot have no tag")
        if self.children == None:
            raise ValueError("Cant have a parent with no children!")
        return f"<{self.tag}>" + reduce(lambda a, b: a + b.to_html(), self.children, "") + f"</{self.tag}>"
