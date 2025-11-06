import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "A whole new world.", {"href":"https://oldschool.runecape.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://oldschool.runecape.com\">A whole new world.</a>")
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_no_false_positives(self):
        node = LeafNode("p", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_to_html_plaintext(self):
        node = LeafNode(None, "Goodbye World")
        self.assertEqual(node.to_html(), "Goodbye World")