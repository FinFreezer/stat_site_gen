import unittest

from build_page import *

class TestPage(unittest.TestCase):
    def test_extract_title(self):
        node = """
# Hello

A new paragraph block.
"""
        self.assertEqual(extract_title(node), "Hello")

        node = "## Hello"
        self.assertRaisesRegex(Exception, "Header H1 required.", extract_title, node)

        node = "# Title with some text and a random # after."
        self.assertEqual(extract_title(node), "Title with some text and a random # after.")
    
    def test_generate_page(self):
        from_path = "./content/index.md"
        template_path = "template.html"
        dest_path = "./public/index.html"
        generate_page(from_path, template_path, dest_path)