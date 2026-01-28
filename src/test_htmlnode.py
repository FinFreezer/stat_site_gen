import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from build_page import markdown_to_html_node

class TestTextNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )
        
    def test_eq(self):
        props1 = {
        "href": "https://www.google.com",
        "target": "_blank",
        "href": "https:oldschool.runescape.com",
        "target": "_empty",
        }
        props2 = {
        "a": "b",
        "fish": "friend",
        "Eowyn": "!man",
        "chocolate?" : "chocolate!",
        }

        html_node1 = HTMLNode("p", "Hello World", [], props1)
        html_node2 = HTMLNode("p", "Hello World", [], props1)
        s1 = repr(html_node1)
        s2 = repr(html_node2)
        self.assertEqual(s1, s2)

        html_node1 = HTMLNode("a", "Hello World", [], props2)
        html_node2 = HTMLNode("a", "Hello World", [], props2)
        s1 = repr(html_node1)
        s2 = repr(html_node2)
        self.assertEqual(s1, s2)

    def test_not_eq(self):
        props1 = {
        "href": "https://www.google.com",
        "target": "_blank",
        "href": "https://oldschool.runescape.com",
        "target": "_nothing",
        }

        props2 = {
        "a": "b",
        "fish": "friend",
        "Eowyn": "!man",
        "chocolate?" : "chocolate!",
        }

        html_node1 = HTMLNode("p", "Hello World", [], props1)
        html_node2 = HTMLNode("p", "Hello World", [], props2)
        s1 = repr(html_node1)
        s2 = repr(html_node2)
        self.assertNotEqual(s1, s2)

        html_node1 = HTMLNode("p", "Goodbye World", [], props1)
        html_node2 = HTMLNode("p", "Hello World", [], props1)
        s1 = repr(html_node1)
        s2 = repr(html_node2)
        self.assertNotEqual(s1, s2)

        html_node1 = HTMLNode("p", "Hello World", [], props1)
        html_node2 = HTMLNode("a", "Hello World", [], props1)
        s1 = repr(html_node1)
        s2 = repr(html_node2)
        self.assertNotEqual(s1, s2)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_large_block(self):
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

        result = """<div><h1>Header One</h1><p>This is a <b>bold</b> and <i>italic</i> paragraph with <code>code</code> inside.</p><blockquote><p>This is a quote that spans <b>two</b> lines</p></blockquote><ol><li>First ordered item with <b>bold</b></li><li>Second ordered item with <code>code</code></li><li>Third ordered item with <i>italics</i></li></ol><ul><li>Unordered <b>one</b></li><li>Unordered <i>two</i></li><li>Unordered <code>three</code></li></ul><pre><code>Code block _with_ **markdown** that should stay the same
And another line
</code></pre></div>"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            result,
        )

if __name__ == "__main__":
    unittest.main()
    