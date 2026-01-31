from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from conversions import *
from build_page import markdown_to_html_node, generate_pages_recursive, generate_page
import os
import shutil

LOG_FILE = ""

def copy_contents(source, destination):
        global LOG_FILE
        contents = os.listdir(source)
        files = []
        subdirs = []
        for part in contents:
                path = os.path.join(source, part)
                if os.path.isdir(path):
                        subdirs.append(part)
                elif os.path.isfile(path):
                        files.append(part)
        for file in files:
                src = os.path.join(source, file)
                dst = os.path.join(destination, file)
                if os.path.exists(dst):
                        continue
                shutil.copy(src, dst)
                LOG_FILE += f"Copied file to {dst}\n"
        for sdir in subdirs:
                src = os.path.join(source, sdir)
                dst = os.path.join(destination, sdir)
                if not os.path.exists(dst):
                        os.mkdir(dst)
                        LOG_FILE += f"Created folder {dst}\n"
                copy_contents(src, dst)
        return

def initialize_public(source, destination):
        global LOG_FILE
        if os.path.exists(destination):
                shutil.rmtree(destination)
        os.mkdir(destination)
        copy_contents(source, destination)
        #print(LOG_FILE)
        return

def main():
        source_path = "./static"
        dest_path = "./public"
        initialize_public(source_path, dest_path)
        source_file = "./content/index.md"
        template_file = "template.html"
        destination_file = "./public/index.html"
        #generate_page(source_file, template_file, destination_file)
        generate_pages_recursive("./content", "template.html", "./public")

main()

if __name__ == "__main__":
        main()