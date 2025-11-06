import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_without_children(self):
        with self.assertRaises(Exception) as context:
            parent_node = ParentNode("img", None)
            parent_node.to_html()
        
        self.assertTrue("Child nodes required" in str(context.exception))

    def test_to_html_without_tag(self):
        with self.assertRaises(Exception) as context:
            child1 = LeafNode("span", "child")
            child2 = LeafNode("b", "child2")
            parent_node = ParentNode(None, [child1, child2])
            parent_node.to_html()
        
        self.assertTrue("Tag required" in str(context.exception))
        
    def test_incompatible_child(self):
        with self.assertRaises(Exception) as context:
            child1 = LeafNode("span", None)
            child2 = LeafNode("b", "child2")
            parent_node = ParentNode("img", [child1, child2])
            s = parent_node.to_html()
        
        self.assertTrue("Leaf must include" in str(context.exception))