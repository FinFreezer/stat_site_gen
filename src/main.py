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
	split_to_substrings("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and a text at the end.")
	split_to_substrings("[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)")
	split_to_substrings("This one contains no links.")
main()
