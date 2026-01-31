from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block import BlockType, Block
from conversions import *
import os
import shutil

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

def extract_title(markdown):
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		block = Block(block)
		block.block_to_block_type()
		block.add_tag()
		if block.get_tag() == "h1":
			return block.get_text()
	raise Exception("Header H1 required.")

def generate_page(from_path, template_path, dest_path):
	print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}")
	markdown = read_file(from_path)
	template = read_file(template_path)

	page = markdown_to_html_node(markdown)
	html = page.to_html()
	title = extract_title(markdown)

	changes = [("{{ Title }}", title), ("{{ Content }}", html)]
	for change in changes:
		template = template.replace(change[0], change[1])
	if not os.path.exists(os.path.dirname(dest_path)):
		os.makedirs(os.path.dirname(dest_path))
	write_file(dest_path, template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	print(f"\nReading content from {dir_path_content} to {dest_dir_path} with {template_path}")
	contents = os.listdir(dir_path_content)
	for part in contents:
		path = os.path.join(dir_path_content, part)
		if os.path.isdir(path):
			generate_pages_recursive(path, template_path, os.path.join(dest_dir_path, part))
		elif os.path.isfile(path):
			generate_page(path, template_path, os.path.join(dest_dir_path, "index.html"))

def read_file(filepath):
	try:
		with open(filepath) as file:
			content = file.read()
			return content
	except:
		raise Exception("File not found.")

def write_file(filepath, content):
	if not os.path.exists(os.path.dirname(filepath)):
		raise Exception("Failed to initialize destination folder.")
	try:
		with open(filepath, 'w') as file:
			file.write(content)
			return
	except:
		raise Exception("Cannot write to file.")