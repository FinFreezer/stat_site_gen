from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block import BlockType, Block
from conversions import *

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	block_objects = [ ]
	for block in blocks:
		block_object = Block(block)
		block_object.block_to_block_type()
		block_object.add_tag()
		block_objects.append(block_object)

	for block in block_objects:
		block.parts.extend(
			text_to_textnodes(block.get_text())
			)

	for block in block_objects:
		block.parts = [text_node_to_html_node(node) for node in block.parts]

	Page = ParentNode("div", block_objects)
	return Page