from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from conversions import *
from build_page import markdown_to_html_node

def main():
        
        md = """
# Header One

This is a **bold** and _italic_ paragraph with `code` inside.

> This is a quote
> that spans **two** lines

1. First ordered item with **bold**
2. Second ordered item with `code`
3. Third ordered item with _italics_

- Unordered **one**
- Unordered _two_
- Unordered `three`

```
Code block _with_ **markdown** that should stay the same
And another line
```
"""

        node = markdown_to_html_node(md)

        print(node.to_html())
main()
