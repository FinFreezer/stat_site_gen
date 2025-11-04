from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
	print("hello world")
	new_node = TextNode("Test string", TextType.ITALIC, "https://oldschool.runescape.com")
	print(new_node)
main()
