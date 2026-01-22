from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from conversions import *
from build_page import markdown_to_html_node

def main():
        
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)

        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
main()
