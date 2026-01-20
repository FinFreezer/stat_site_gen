from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
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
        if node.text_type == TextType.TEXT:
            if node.text.count(delimiter) != 2:
                raise Exception("Missing closing/starting delimiter.")

            blocks = node.text.split(delimiter)
            if blocks[0] == "":
                if node.text[0] == delimiter:
                    new_nodes.extend([
                        TextNode(blocks[1], text_type),
                        TextNode(blocks[2], TextType.TEXT)])
                else:
                    new_nodes.extend([
                        TextNode(blocks[1], TextType.TEXT),
                        TextNode(blocks[2], text_type)])
            elif blocks[2] == "":
                if node.text[0] == delimiter:
                    new_nodes.extend([
                        TextNode(blocks[0], text_type),
                        TextNode(blocks[1], TextType.TEXT)])
                else:
                    new_nodes.extend([
                        TextNode(blocks[0], TextType.TEXT),
                        TextNode(blocks[1], text_type)])
            else:
                new_nodes.extend( [
                (TextNode(blocks[0], TextType.TEXT)),
                (TextNode(blocks[1], text_type)),
                (TextNode(blocks[2], TextType.TEXT))])

        else:
            new_nodes.extend([node])
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
    end = -1
    start = 0
    parts = []
    result = []
    for node in old_nodes:
        text = node.text
        while True:
            found_links = extract_markdown_images(text)
            num_found_links = len(found_links)
            if len == 0:
                return [node]
            
            for i in range(num_found_links):
                end = text.rfind( ("(" + found_links[i][1] + ")") ) + len("(" + found_links[i][1] + ")")
                start = text.find( "![" + found_links[i][0] + "]")
                parts.append(text[:end].rsplit('!', 1))
                parts[i][1] = "!" + parts[i][1]
                text = text[end:]
            break
    
    cells = len(parts)
    for i in range(cells):
        result.append( TextNode(parts[i][0], TextType.TEXT) )
        result.append( TextNode(found_links[i][0], TextType.IMAGE, found_links[i][1]) )
    
    return result

def split_nodes_link(old_nodes):
    end = -1
    start = 0
    parts = []
    result = []
    for node in old_nodes:
        text = node.text
        while True:
            found_links = extract_markdown_links(text)
            num_found_links = len(found_links)
            if len == 0:
                return [node]
            
            for i in range(num_found_links):
                end = text.rfind( ("(" + found_links[i][1] + ")") ) + len("(" + found_links[i][1] + ")")
                start = text.find( "[" + found_links[i][0] + "]")
                parts.append(text[:end].rsplit('[', 1))
                parts[i][1] = "[" + parts[i][1]
                text = text[end:]
            break
    
    cells = len(parts)
    for i in range(cells):
        result.append( TextNode(parts[i][0], TextType.TEXT) )
        result.append( TextNode(found_links[i][0], TextType.LINK, found_links[i][1]) )
    
    return result