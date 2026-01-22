from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from conversions import *
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


def main():
        
        #text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        """node = TextNode(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png). " +
        "And a third for [good measure](https://i.imgur.com/fthagn123.png). And some filler.",
                TextType.TEXT,
        )
        node2 = TextNode("This is another text with a [great](https://i.imgur.com/node2.png) link and another [amazing](https://photobucket.com/3elNhQu.png). " +
        "And a third just in case [lmao](rddt.com/fthagn123.png) with text.", TextType.TEXT)
        new_nodes = split_nodes_link([node, node2])"""
        #text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
main()
