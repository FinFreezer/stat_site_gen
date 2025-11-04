import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, "https://oldschool.runescape.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://oldschool.runescape.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):

        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, "https://oldschool.runescape.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, "https://oldschool.runescape.com")
        node2 = TextNode("This is a text node", TextType.CODE, "https://oldschool.runescape.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()