from textnode import TextNode, TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from conversions import *
from build_page import markdown_to_html_node, generate_pages_recursive
import os
import shutil
import sys

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
        if len(sys.argv) == 2:
                basepath = sys.argv[1]
        else:
                basepath = "/"
        source_path = "static"
        dest_path = "docs"
        initialize_public(source_path, dest_path)
        """
        source_file = "./content/index.md"
        template_file = "template.html"
        destination_file = "./docs/index.html"
        """
        source_path = "content"
        #generate_page(source_file, template_file, destination_file)
        #generate_pages_recursive("./content", "template.html", "./public")
        generate_pages_recursive(source_path, "template.html", dest_path, basepath)

main()

if __name__ == "__main__":
        main()