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

if __name__ == "__main__":
    unittest.main()