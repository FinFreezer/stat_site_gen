from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
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
	node1 = LeafNode("b", "Hello, world!")
	node2 = LeafNode("a", "A whole new world.", {"href":"https://oldschool.runecape.com"})
	node3 = LeafNode("p", "Hello, world!")
	node = ParentNode("i", [node1, node2, node3], props2)
	s = node.to_html()
	print(s)
	node2 = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
	)
	s2 = node2.to_html()
	print(s2)
main()
