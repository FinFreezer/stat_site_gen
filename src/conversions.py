from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from block import BlockType, Block
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Not a known type.")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = [ ]
    if not old_nodes:
        raise Exception("No nodes found.")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        delims = [match.start() for match in re.finditer(re.escape(delimiter), node.text)]
        delim_amount = len(delims)
        if delim_amount == 0:
            new_nodes.append(node)
            continue

        if delim_amount % 2 != 0:
            raise Exception("Missing closing/starting delimiter")

        parts = node.text.split(delimiter)
        indexes = len(parts)
        for i in range(indexes):
            if parts[i] == "":
                continue
            elif (i % 2 == 0):
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
        
    return new_nodes

def extract_markdown_images(text):
    results = []
    matches_alt_text = re.findall(r"!\[(.*?)\]", text)
    matches_URLs = re.findall(r"\(([^\(\)]*)\)", text)
    matches = len(matches_alt_text)
    for i in range(matches):
        results.append( (matches_alt_text[i], matches_URLs[i]) )
        i += 1
    return results
            
def extract_markdown_links(text):
    results = []
    matches_anchor_text = re.findall(r"\[(.*?)\]", text)
    matches_URLs = re.findall(r"\(([^\(\)]*)\)", text)
    matches = len(matches_anchor_text)
    for i in range(matches):
        results.append( (matches_anchor_text[i], matches_URLs[i]) )
        i += 1
    return results

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        found_links = extract_markdown_images(node.text)
        num_found_links = len(found_links)
        if num_found_links == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for i in range(num_found_links):
            splits = (text.split(f"![{found_links[i][0]}]({found_links[i][1]})"))
            if len(splits) != 2:
                raise Exception("Invalid markdown: image section not closed.")
            if splits[0] != "":
                new_nodes.append( TextNode(splits[0], TextType.TEXT) )
            new_nodes.append(TextNode(found_links[i][0], TextType.IMAGE, found_links[i][1]))
            text = splits[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        found_links = extract_markdown_links(node.text)
        num_found_links = len(found_links)
        if num_found_links == 0:
            new_nodes.append(node)
            continue
        
        text = node.text
        for i in range(num_found_links):
            splits = (text.split(f"[{found_links[i][0]}]({found_links[i][1]})"))
            if len(splits) != 2:
                raise Exception("Invalid markdown: image section not closed.")
            if splits[0] != "":
                new_nodes.append( TextNode(splits[0], TextType.TEXT) )
            new_nodes.append(TextNode(found_links[i][0], TextType.LINK, found_links[i][1]))
            text = splits[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    Node = TextNode(text, TextType.TEXT)
    results = (
        split_nodes_delimiter( [Node], "`", TextType.CODE) )
    
    results = (
        split_nodes_delimiter( results, "**", TextType.BOLD) )
    
    results = (
        split_nodes_delimiter( results, "_", TextType.ITALIC) )
    
    results = (
        split_nodes_image(results)
    )
    
    results = (
        split_nodes_link(results)
    )
    
    return results

def markdown_to_blocks(markdown):
    parts = markdown.split("\n\n")
    results = []
    for part in parts:
        if part != '':
            results.append("\n".join(part.strip().split("\n")))
        else:
            del part
    return results