import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block import BlockType, Block
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

        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png). This is text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(". This is text.", TextType.TEXT),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with no image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image.", TextType.TEXT),
            ],
            new_nodes,
        )

        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png). This one starts with an image, and includes another one ![different image](https://i.imgur.com/ftaghn.jpg). With some text at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(". This one starts with an image, and includes another one ", TextType.TEXT),
                TextNode("different image", TextType.IMAGE, "https://i.imgur.com/ftaghn.jpg"),
                TextNode(". With some text at the end.", TextType.TEXT)
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

        node = TextNode(
            "[to imgur](https://i.imgur.com). This is text.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to imgur", TextType.LINK, "https://i.imgur.com"),
                TextNode(". This is text.", TextType.TEXT),
            ],
            new_nodes,
        )

        node = TextNode(
            "This is text with no link.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link.", TextType.TEXT),
            ],
            new_nodes,
        )

        node = TextNode(
            "[reddit](www.reddit.com). This one starts with a link, and includes another one [boot dot dev](https://www.boot.dev). With some text at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("reddit", TextType.LINK, "www.reddit.com"),
                TextNode(". This one starts with a link, and includes another one ", TextType.TEXT),
                TextNode("boot dot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(". With some text at the end.", TextType.TEXT)
            ],
            new_nodes,
        )

        node = TextNode(
            "This one starts with text. [reddit](www.reddit.com). Includes a second link: [boot dot dev](https://www.boot.dev). And a third link: [YTP](ytb.com/qdEFWEF).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This one starts with text. ", TextType.TEXT),
                TextNode("reddit", TextType.LINK, "www.reddit.com"),
                TextNode(". Includes a second link: ", TextType.TEXT),
                TextNode("boot dot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(". And a third link: ", TextType.TEXT),
                TextNode("YTP", TextType.LINK, "ytb.com/qdEFWEF"),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes,
        )

class TestTotalConversion(unittest.TestCase):
    def test_full_line(self):
        #node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
        result = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertEqual( (
            [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
            ), result)
    
    def test_markdown_to_blocks(self):
        md = """
#This is a header

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


One more paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "#This is a header",
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "One more paragraph."
            ],
        )
    
        md = """

# Heading with extra newlines above


This paragraph has some text.

- List item 1
- List item 2


Another paragraph here.
It continues on the next line.



Yet another block after many newlines.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with extra newlines above",
                "This paragraph has some text.",
                "- List item 1\n- List item 2",
                "Another paragraph here.\nIt continues on the next line.",
                "Yet another block after many newlines."
            ],
        )

    def test_block_to_block_type(self):
        block = "###This is a header"
        b1 = Block(block)
        self.assertEqual(b1.block_to_block_type(), "heading")

        block = """```
This is code
```"""
        b2 = Block(block)
        self.assertEqual(b2.block_to_block_type(), "code")

        block = """1. First line
2. Second line
3. Third line."""
        b3 = Block(block)
        self.assertEqual(b3.block_to_block_type(), "ordered_list")

        block ="""3. First Line
4. Second line
5. Third line."""
        b4 = Block(block)
        self.assertEqual(b4.block_to_block_type(), "ordered_list")

        block = """7. First line
8. Second line
4. Third line"""
        b5 = Block(block)
        self.assertEqual(b5.block_to_block_type(), "paragraph")

        block = "> This is a quote"
        b6 = Block(block)
        self.assertEqual(b6.block_to_block_type(), "quote")

        block = "#######This is a header"
        b7 = Block(block)
        self.assertNotEqual(b7.block_to_block_type(), "heading")

        block = "- This is an\n- Unordered list\n- With some data"
        b8 = Block(block)
        self.assertEqual(b8.block_to_block_type(), "unordered_list")
