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
        """node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png). " +
        "And a third for ![good measure](https://i.imgur.com/fthagn123.png). And some filler.",
                TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])"""
main()
