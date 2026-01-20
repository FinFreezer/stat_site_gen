import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from conversions import *

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is also a node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is also a node</b>")
    
    def test_italic(self):
        node = TextNode("This is also a node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is also a node</i>")
    
    def test_code(self):
        node = TextNode("This is also a node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is also a node</code>")
    
    def test_link(self):
        node = TextNode("This is also a node", TextType.LINK, "oldschool.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is also a node")
        self.assertTrue("href" in html_node.props)
        self.assertEqual(html_node.to_html(), "<a href=\"oldschool.com\">This is also a node</a>")

class TestSplitNodes(unittest.TestCase):
    def test_bold(self):
        tn1 = TextNode("This is a text with a ", TextType.TEXT)
        tn2 = TextNode("bold block", TextType.BOLD)
        tn3 = TextNode(" word", TextType.TEXT)
        node5 = TextNode("This is a text with a **bold block** word", TextType.TEXT)
        self.assertEqual( ([tn1, tn2, tn3]), split_nodes_delimiter([node5], "**", TextType.BOLD))
    
    def test_code(self):
        tn1 = TextNode("This is text with a ", TextType.TEXT)
        tn2 = TextNode("code block", TextType.CODE)
        tn3 = TextNode(" word", TextType.TEXT)
        tn4 = TextNode("This is text with a ", TextType.TEXT)
        tn5 = TextNode("code block", TextType.CODE)
        tn6 = TextNode(" word as well", TextType.TEXT)
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a `code block` word as well", TextType.TEXT)
        self.assertEqual( ([tn1, tn2, tn3, tn4, tn5, tn6]), split_nodes_delimiter([node, node2], "`", TextType.CODE))
    
    def test_two_block_code(self):
        tn1 = TextNode("And ", TextType.TEXT)
        tn2 = TextNode("Another one", TextType.CODE)
        tn3 = TextNode("One more", TextType.CODE)
        tn4 = TextNode(" for the road", TextType.TEXT)
        node3 = TextNode("And `Another one`", TextType.TEXT)
        node4 = TextNode("`One more` for the road", TextType.TEXT)
        self.assertEqual( 
            [tn1, tn2, tn3, tn4], split_nodes_delimiter( [node3, node4], "`", TextType.CODE ) 
        )
    
    def test_italics_nodes(self):
        tn1 = TextNode("_This is a fully italic node_", TextType.ITALIC)
        tn2 = TextNode("This is a text with a ", TextType.TEXT)
        tn3 = TextNode("italic block", TextType.ITALIC)
        tn4 = TextNode(" word.", TextType.TEXT)
        node6 = TextNode("_This is a fully italic node_", TextType.ITALIC)
        node7 = TextNode("This is a text with a _italic block_ word.", TextType.TEXT)

        self.assertEqual(
            [tn1], split_nodes_delimiter( [node6], "_", TextType.ITALIC )
        )
        self.assertEqual(
            [tn2, tn3, tn4], split_nodes_delimiter( [node7], "_", TextType.ITALIC )
        )
        
    
class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images(
            "Second text with a different ![picture](photobucket.com/zzfkwe.webp)"
        )
        self.assertListEqual([("picture", "photobucket.com/zzfkwe.webp")], matches)

        matches = extract_markdown_images(
            "This is text with an !(image)[https://i.imgur.com/zjjcJKZ.png]"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with a [anchor text](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("anchor text", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links(
            "This is a text with a [cat picture](bit.ly/cute_cat%123A.webp)"
        )
        self.assertListEqual([("cat picture", "bit.ly/cute_cat%123A.webp")], matches)

        matches = extract_markdown_links(
            "This is a text with a (bad formatting)[boot.dev]"
        )
        self.assertNotEqual([("bad formatting", "boot.dev")], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode( 
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )